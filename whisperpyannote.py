#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import subprocess
import datetime
import wave
import tempfile
import whisper
import argparse
from tqdm import tqdm
from pyannote.audio import Pipeline

# --- Argument parser ---
parser = argparse.ArgumentParser(description="Transcrire et diariser un fichier audio ou vidéo.")
parser.add_argument("input_path", help="Chemin du fichier audio ou vidéo à traiter")
parser.add_argument("output_file", help="Chemin du fichier texte de sortie")
parser.add_argument("--whisper_model", default="turbo", choices=["tiny", "base", "small", "medium", "large", "turbo"],
                    help="Modèle Whisper à utiliser (par défaut : turbo)")
parser.add_argument("--keep_temp", action="store_true",
                    help="Ne pas supprimer les fichiers temporaires")
args = parser.parse_args()

input_path = args.input_path
output_file = args.output_file
whisper_model_choice = args.whisper_model
keep_temp = args.keep_temp

# --- Fonctions utilitaires ---
def run_command(command):
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur : {e}")
        sys.exit(1)

def is_video(file_path):
    return file_path.lower().endswith(('.mp4', '.mkv', '.mov', '.avi', '.flv', '.webm'))

def extract_audio(video_path):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        audio_output = tmpfile.name
    print("🎥 Extraction audio depuis la vidéo...")
    run_command([
        "ffmpeg", "-i", video_path, "-ac", "1", "-ar", "16000", "-vn", "-y", audio_output
    ])
    print(f"✅ Audio extrait : {audio_output}")
    return audio_output

def is_valid_audio(file_path):
    try:
        with wave.open(file_path, 'rb') as audio:
            return audio.getframerate() == 16000 and audio.getnchannels() == 1
    except (wave.Error, FileNotFoundError, IOError):
        return False

def convert_audio(audio_path):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        converted_audio = tmpfile.name
    print("🔄 Conversion de l'audio au format 16kHz mono...")
    run_command([
        "ffmpeg", "-i", audio_path, "-ac", "1", "-ar", "16000", "-y", converted_audio
    ])
    print(f"✅ Audio converti : {converted_audio}")
    return converted_audio

def format_time(seconds):
    return str(datetime.timedelta(seconds=int(seconds)))

def segment_score(t_segment, s_segment):
    ts, te = t_segment["start"], t_segment["end"]
    ss, se = s_segment["start"], s_segment["end"]
    overlap = min(te, se) - max(ts, ss)
    return max(0, overlap / (te - ts)) if (te - ts) else 0

# --- Préparation du fichier ---
if not os.path.exists(input_path):
    print(f"⚠️ Fichier introuvable : {input_path}")
    sys.exit(1)

original_input_path = input_path  # pour savoir après s'il faut le supprimer

if is_video(input_path):
    input_path = extract_audio(input_path)

if not is_valid_audio(input_path):
    input_path = convert_audio(input_path)

# --- Transcription Whisper ---
print(f"\n🎙️ Chargement du modèle Whisper '{whisper_model_choice}'...")
model = whisper.load_model(whisper_model_choice)
print("📝 Transcription en cours... (cela peut prendre un moment)")
result = model.transcribe(input_path)
transcript_segments = result["segments"]

# --- Diarisation Pyannote ---
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
if not HF_TOKEN:
    HF_TOKEN = input("🔑 Merci d'entrer votre HUGGINGFACE_TOKEN : ").strip()
    if not HF_TOKEN:
        print("❌ Token manquant. Arrêt du script.")
        sys.exit(1)

print("\n🗣️ Diarisation avec Pyannote en cours...")
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.0",
    use_auth_token=HF_TOKEN
)
diarization = pipeline(input_path)

# --- Traitement des segments ---
speaker_segments = []
for turn, track, speaker in diarization.itertracks(yield_label=True):
    speaker_segments.append({
        "speaker": speaker,
        "start": turn.start,
        "end": turn.end
    })

print(f"✅ {len(speaker_segments)} segments de speakers détectés.")

# --- Association transcription <-> speaker avec barre de progression ---
formatted_output = []
assigned_speakers = []  # AJOUT : liste pour stocker le speaker de chaque segment
OVERLAP_THRESHOLD = 0.01  # 🔽 seuil réduit pour inclure plus de correspondances

print("\n🔗 Association des segments transcription <-> speakers...")
for t_segment in tqdm(transcript_segments, desc="Matching segments"):
    best_speaker = "inconnu"
    best_score = 0

    for s_segment in speaker_segments:
        score = segment_score(t_segment, s_segment)
        if score > best_score and score > OVERLAP_THRESHOLD:
            best_score = score
            best_speaker = s_segment["speaker"]

    start_time = format_time(t_segment["start"])
    end_time = format_time(t_segment["end"])
    text = t_segment['text']

    formatted_output.append(f"[{start_time} - {end_time}] 🗣️ Speaker {best_speaker}: {text}")
    assigned_speakers.append(best_speaker)  # AJOUT : on garde le speaker associé


# --- Résumé temps de parole ---
speaker_durations = {}
for s in speaker_segments:
    speaker_durations[s["speaker"]] = speaker_durations.get(s["speaker"], 0) + (s["end"] - s["start"])

speaker_durations_formatted = {
    speaker: str(datetime.timedelta(seconds=int(duration)))
    for speaker, duration in speaker_durations.items()
}

# --- Résultats ---
print("\n⏳ Temps de parole par speaker :")
for speaker, duration in speaker_durations_formatted.items():
    print(f"🗣️ Speaker {speaker}: {duration}")

print("\n📜 Aperçu de la transcription :")
for line in formatted_output[:10]:
    print(line)
print("... (voir fichier pour le reste)")

# --- Sauvegarde dans le fichier ---
# Helpers locaux (uniquement pour le rendu fichier)
import re

def _smart_join(a: str, b: str) -> str:
    if not a:
        return (b or "").strip()
    if not b:
        return a.strip()
    sep = "" if a.endswith(("—", "-", "…", ":", "(", "[", "{", "/")) else " "
    j = (a.rstrip() + sep + b.lstrip())
    j = re.sub(r"\s+([,.?!;:])", r"\1", j)
    j = re.sub(r"\s{2,}", " ", j)
    return j.strip()

def merge_by_runs(segments):
    if not segments:
        return []
    segments = sorted(segments, key=lambda s: (s["start"], s["end"]))
    merged = []
    cur = dict(segments[0])
    for seg in segments[1:]:
        if seg["speaker"] == cur["speaker"]:
            cur["end"] = max(cur["end"], float(seg["end"]))
            cur["text"] = _smart_join(cur.get("text",""), seg.get("text",""))
        else:
            if cur.get("text","").strip():
                merged.append(cur)
            cur = dict(seg)
    if cur.get("text","").strip():
        merged.append(cur)
    return merged

def hhmmss(t):
    return str(datetime.timedelta(seconds=int(max(0, t))))

# 1) Construire la liste structurée à partir des segments Whisper + attribution speaker
segments = []
for t, spk in zip(transcript_segments, assigned_speakers):
    segments.append({
        "start": float(t["start"]),
        "end": float(t["end"]),
        "speaker": spk,
        "text": t.get("text", "")
    })

# 2) Fusion stricte par speaker (jusqu’au changement d’intervenant)
segments_merged = merge_by_runs(segments)

# 3) Écrire UNIQUEMENT la version fusionnée dans le fichier (les consoles restent inchangées)
with open(output_file, "w", encoding="utf-8") as f:
    f.write("⏳ Temps de parole par speaker :\n")
    for speaker, duration in speaker_durations_formatted.items():
        f.write(f"🗣️ Speaker {speaker}: {duration}\n")
    f.write("\n📜 Transcription fusionnée par speaker :\n\n")
    for s in segments_merged:
        f.write(f"[{hhmmss(s['start'])}–{hhmmss(s['end'])}] {s['speaker']}: {s['text'].strip()}\n")

print(f"\n✅ Transcription complète sauvegardée dans : {output_file}")

# --- Résumé final ---
total_duration = sum(speaker_durations.values())
average_duration = total_duration / len(speaker_durations) if speaker_durations else 0

print(f"\n📊 Résumé global :")
print(f"- Durée totale analysée : {str(datetime.timedelta(seconds=int(total_duration)))}")
print(f"- Nombre de speakers : {len(speaker_durations)}")
print(f"- Durée moyenne par speaker : {str(datetime.timedelta(seconds=int(average_duration)))}")

# --- Nettoyage fichiers temporaires ---
if not keep_temp and input_path != original_input_path and input_path.startswith(tempfile.gettempdir()):
    os.unlink(input_path)
    print("\n🧹 Fichier temporaire supprimé.")
elif keep_temp:
    print(f"\n📂 Fichier temporaire conservé : {input_path}")
