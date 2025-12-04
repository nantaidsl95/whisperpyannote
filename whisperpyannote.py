#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de transcription et diarisation audio/vidéo
Auteur : marcdelage
"""

import os
import sys
import subprocess
import datetime
import wave
import tempfile
import argparse
import re

import whisper
from tqdm import tqdm
from pyannote.audio import Pipeline
import torchaudio

# AJOUT pour le problème torch / safe globals
import torch
from torch.serialization import add_safe_globals
from pyannote.audio.core.task import Specifications, Problem, Resolution


# =========================
#   Fonctions utilitaires
# =========================

def run_command(command):
    """Exécute une commande système et quitte en cas d'erreur."""
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'exécution de la commande : {e}")
        sys.exit(1)


def is_video(file_path: str) -> bool:
    """Détermine si le fichier est une vidéo via son extension."""
    return file_path.lower().endswith((
        ".mp4", ".mkv", ".mov", ".avi", ".flv", ".webm"
    ))


def extract_audio(video_path: str) -> str:
    """Extrait l'audio d'une vidéo en mono 16kHz vers un fichier WAV temporaire."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        audio_output = tmpfile.name

    print("🎥 Extraction audio depuis la vidéo...")
    run_command([
        "ffmpeg", "-i", video_path,
        "-ac", "1", "-ar", "16000",
        "-vn", "-y",
        audio_output
    ])
    print(f"✅ Audio extrait : {audio_output}")
    return audio_output


def is_valid_audio(file_path: str) -> bool:
    """Vérifie que l'audio est bien au format 16kHz mono (sinon conversion)."""
    try:
        with wave.open(file_path, 'rb') as audio:
            return audio.getframerate() == 16000 and audio.getnchannels() == 1
    except (wave.Error, FileNotFoundError, IOError):
        return False


def convert_audio(audio_path: str) -> str:
    """Convertit un fichier audio en WAV mono 16kHz temporaire."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        converted_audio = tmpfile.name

    print("🔄 Conversion de l'audio au format 16kHz mono...")
    run_command([
        "ffmpeg", "-i", audio_path,
        "-ac", "1", "-ar", "16000",
        "-y",
        converted_audio
    ])
    print(f"✅ Audio converti : {converted_audio}")
    return converted_audio


def format_time(seconds: float) -> str:
    """Formate un temps en secondes en HH:MM:SS."""
    return str(datetime.timedelta(seconds=int(seconds)))


def segment_score(t_segment, s_segment) -> float:
    """
    Calcule le score de recouvrement entre :
      - un segment transcription Whisper t_segment
      - un segment speaker Pyannote s_segment
    Retourne la fraction de t_segment qui chevauche s_segment.
    """
    ts, te = t_segment["start"], t_segment["end"]
    ss, se = s_segment["start"], s_segment["end"]
    overlap = min(te, se) - max(ts, ss)
    return max(0, overlap / (te - ts)) if (te - ts) else 0.0


def _smart_join(a: str, b: str) -> str:
    """Fusionne proprement deux bouts de texte en évitant les doubles espaces et espaces avant la ponctuation."""
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
    """
    Fusionne des segments consécutifs qui appartiennent au même speaker.
    segments: liste de dicts {"start", "end", "speaker", "text"}
    """
    if not segments:
        return []

    # Tri par temps
    segments = sorted(segments, key=lambda s: (s["start"], s["end"]))
    merged = []
    cur = dict(segments[0])

    for seg in segments[1:]:
        if seg["speaker"] == cur["speaker"]:
            # Extension du segment courant
            cur["end"] = max(cur["end"], float(seg["end"]))
            cur["text"] = _smart_join(cur.get("text", ""), seg.get("text", ""))
        else:
            if cur.get("text", "").strip():
                merged.append(cur)
            cur = dict(seg)

    if cur.get("text", "").strip():
        merged.append(cur)

    return merged


def hhmmss(t: float) -> str:
    """Formate un temps en HH:MM:SS (>= 0)."""
    return str(datetime.timedelta(seconds=int(max(0, t))))


def get_audio_duration_seconds(audio_path: str) -> float:
    """Retourne la durée de l'audio (en secondes) à partir du fichier WAV."""
    try:
        with wave.open(audio_path, 'rb') as audio:
            frames = audio.getnframes()
            rate = audio.getframerate()
            return frames / float(rate) if rate > 0 else 0.0
    except Exception:
        return 0.0


# =============================
#   Gestion du token HF
# =============================

def get_hf_token(args) -> str:
    """
    Récupère le token Hugging Face via :
      1) variable d'environnement HF_TOKEN ou HUGGINGFACE_TOKEN
      2) paramètre CLI --hf_token
      3) saisie interactive (si terminal) si rien n'a été trouvé
    """
    # 1) Variables d'environnement
    env_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if env_token:
        return env_token.strip()

    # 2) Paramètre CLI
    if args.hf_token:
        return args.hf_token.strip()

    # 3) Optionnellement, l'utilisateur peut forcer la demande via --ask_token
    if args.ask_token and not sys.stdin.isatty():
        print("❌ --ask_token demandé mais impossible de lire depuis stdin (mode non interactif).")
        sys.exit(1)

    # 4) Si on est dans un terminal interactif, on propose toujours la saisie
    if sys.stdin.isatty():
        try:
            token = input("🔑 Aucun token Hugging Face détecté. Entrez votre token : ").strip()
        except EOFError:
            token = ""
        if token:
            return token
        print("❌ Aucun token saisi.")
        sys.exit(1)

    # 5) Mode non interactif sans token
    print("🔎 Aucun token Hugging Face disponible (ni variable d'environnement, ni CLI, ni saisie interactive possible).")
    print("   Veuillez définir HF_TOKEN ou HUGGINGFACE_TOKEN, ou utiliser --hf_token.")
    sys.exit(1)


# =============================
#   Transcription Whisper
# =============================

def load_whisper_model(whisper_model_choice: str):
    """Charge le modèle Whisper demandé."""
    print(f"\n🎙️ Chargement du modèle Whisper '{whisper_model_choice}'...")
    model = whisper.load_model(whisper_model_choice)
    return model


def run_whisper_transcription(model, audio_path: str, language: str = None):
    """Lance la transcription Whisper sur le fichier audio donné."""
    print("📝 Transcription en cours... (cela peut prendre un moment)")
    transcribe_kwargs = {}
    if language:
        transcribe_kwargs["language"] = language
        print(f"🌐 Langue forcée pour Whisper : {language}")

    result = model.transcribe(audio_path, **transcribe_kwargs)
    return result


# =============================
#   Diarisation Pyannote
# =============================

def prepare_safe_globals():
    """Ajoute Specifications/Problem/Resolution aux safe_globals si possible."""
    try:
        add_safe_globals([Specifications, Problem, Resolution])
    except Exception as e:
        print("⚠️ Impossible d'ajouter Specifications/Problem/Resolution aux safe_globals :", e)


def run_diarization(audio_path: str, hf_token: str):
    """
    Lance la diarisation Pyannote sur l'audio donné.
    Retourne : speaker_segments (liste), waveform, sample_rate
    """
    print("\n🗣️ Diarisation avec Pyannote en cours...")

    prepare_safe_globals()

    try:
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-community-1",
            token=hf_token,
        )
    except Exception as e:
        print("❌ Erreur lors du chargement de la pipeline pyannote/speaker-diarization-community-1 :")
        print(e)
        sys.exit(1)

    try:
        waveform, sample_rate = torchaudio.load(audio_path)
    except Exception as e:
        print("❌ Erreur lors du chargement audio avec torchaudio :")
        print(e)
        sys.exit(1)

    diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate})

    speaker_segments = []

    # Compatible Annotation directe OU attribut .speaker_diarization
    annotation = getattr(diarization, "speaker_diarization", diarization)

    for segment, _, speaker in annotation.itertracks(yield_label=True):
        speaker_segments.append({
            "speaker": speaker,
            "start": segment.start,
            "end": segment.end,
        })

    print(f"✅ {len(speaker_segments)} segments de speakers détectés.")
    return speaker_segments, waveform, sample_rate


# =============================
#   Parsing des arguments
# =============================

def parse_args():
    parser = argparse.ArgumentParser(
        description="Transcrire et/ou diariser un fichier audio ou vidéo."
    )
    parser.add_argument("input_path", help="Chemin du fichier audio ou vidéo à traiter")
    parser.add_argument("output_file", help="Chemin du fichier texte de sortie")

    parser.add_argument(
        "--whisper_model",
        default="turbo",
        choices=["tiny", "base", "small", "medium", "large", "turbo"],
        help="Modèle Whisper à utiliser (par défaut : turbo)"
    )
    parser.add_argument(
        "--keep_temp",
        action="store_true",
        help="Ne pas supprimer les fichiers temporaires"
    )
    parser.add_argument(
        "--hf_token",
        help="Token Hugging Face passé directement en ligne de commande"
    )
    parser.add_argument(
        "--ask_token",
        action="store_true",
        help="Forcer la demande interactive du token Hugging Face si absent"
    )
    parser.add_argument(
        "--language",
        help="Forcer la langue pour Whisper (ex: fr, en, de). Si omis, Whisper auto-détecte."
    )

    # Modes exclusifs : transcription seule / diarisation seule / par défaut les deux
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--transcription_only",
        action="store_true",
        help="Ne faire que la transcription (pas de diarisation)."
    )
    mode_group.add_argument(
        "--diarization_only",
        action="store_true",
        help="Ne faire que la diarisation (pas de transcription Whisper)."
    )

    return parser.parse_args()


# =============================
#   Fonction principale
# =============================

def main():
    args = parse_args()

    input_path = args.input_path
    output_file = args.output_file
    whisper_model_choice = args.whisper_model
    keep_temp = args.keep_temp
    language = args.language

    transcription_only = args.transcription_only
    diarization_only = args.diarization_only

    # --- Préparation du fichier ---
    if not os.path.exists(input_path):
        print(f"⚠️ Fichier introuvable : {input_path}")
        sys.exit(1)

    original_input_path = input_path  # pour savoir après s'il faut le supprimer

    # Si vidéo, on extrait l'audio
    if is_video(input_path):
        input_path = extract_audio(input_path)

    # Si audio non conforme 16kHz mono, on convertit
    if not is_valid_audio(input_path):
        input_path = convert_audio(input_path)

    # Durée totale de l'audio (pour le résumé final)
    audio_total_duration = get_audio_duration_seconds(input_path)

    transcript_segments = None
    speaker_segments = []
    waveform = None
    sample_rate = None

    # --- Transcription Whisper (sauf si diarisation seule) ---
    if not diarization_only:
        model = load_whisper_model(whisper_model_choice)
        result = run_whisper_transcription(model, input_path, language=language)
        transcript_segments = result["segments"]

    # --- Diarisation Pyannote (sauf si transcription seule) ---
    if not transcription_only:
        hf_token = get_hf_token(args)
        speaker_segments, waveform, sample_rate = run_diarization(input_path, hf_token)

    # =========================
    #   MODE TRANSCRIPTION SEULE
    # =========================
    if transcription_only and not diarization_only:
        print("\n📝 Mode : TRANSCRIPTION SEULE (pas de diarisation).")

        # Aperçu console
        print("\n📜 Aperçu de la transcription :")
        for seg in (transcript_segments or [])[:10]:
            print(f"[{format_time(seg['start'])} - {format_time(seg['end'])}] {seg['text']}")
        if transcript_segments and len(transcript_segments) > 10:
            print("... (voir fichier pour le reste)")

        # Écriture fichier
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("📜 Transcription (sans diarisation) :\n\n")
            if not transcript_segments:
                f.write("(Aucun segment de transcription.)\n")
            else:
                for t in transcript_segments:
                    f.write(f"[{hhmmss(float(t['start']))}–{hhmmss(float(t['end']))}] {t.get('text', '').strip()}\n")

        print(f"\n✅ Transcription sauvegardée dans : {output_file}")

        # Résumé
        print(f"\n📊 Résumé global :")
        print(f"- Durée totale de l'audio analysé : {str(datetime.timedelta(seconds=int(audio_total_duration)))}")
        print(f"- Nombre de segments de transcription : {len(transcript_segments) if transcript_segments else 0}")

    # =========================
    #   MODE DIARISATION SEULE
    # =========================
    elif diarization_only and not transcription_only:
        print("\n🗣️ Mode : DIARISATION SEULE (pas de transcription Whisper).")

        # Temps de parole par speaker
        speaker_durations = {}
        for s in speaker_segments:
            speaker_durations[s["speaker"]] = speaker_durations.get(s["speaker"], 0.0) + (s["end"] - s["start"])

        speaker_durations_formatted = {
            speaker: str(datetime.timedelta(seconds=int(duration)))
            for speaker, duration in speaker_durations.items()
        }

        print("\n⏳ Temps de parole par speaker :")
        for speaker, duration in speaker_durations_formatted.items():
            print(f"🗣️ Speaker {speaker}: {duration}")

        print("\n📜 Aperçu des segments de diarisation (sans texte) :")
        for seg in speaker_segments[:10]:
            print(f"[{hhmmss(seg['start'])}–{hhmmss(seg['end'])}] {seg['speaker']}")
        if len(speaker_segments) > 10:
            print("... (voir fichier pour le reste)")

        # Écriture fichier
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("⏳ Temps de parole par speaker :\n")
            for speaker, duration in speaker_durations_formatted.items():
                f.write(f"🗣️ Speaker {speaker}: {duration}\n")

            f.write("\n📜 Segments de diarisation (sans transcription) :\n\n")
            if not speaker_segments:
                f.write("(Aucun segment de diarisation.)\n")
            else:
                for s in speaker_segments:
                    f.write(f"[{hhmmss(s['start'])}–{hhmmss(s['end'])}] {s['speaker']}\n")

        print(f"\n✅ Diarisation sauvegardée dans : {output_file}")

        # Résumé
        total_speech_duration = sum(speaker_durations.values())
        average_duration = total_speech_duration / len(speaker_durations) if speaker_durations else 0.0

        print(f"\n📊 Résumé global :")
        print(f"- Durée totale de l'audio analysé : {str(datetime.timedelta(seconds=int(audio_total_duration)))}")
        print(f"- Somme des temps de parole (tous speakers cumulés) : {str(datetime.timedelta(seconds=int(total_speech_duration)))}")
        print(f"- Nombre de speakers : {len(speaker_durations)}")
        print(f"- Durée moyenne par speaker : {str(datetime.timedelta(seconds=int(average_duration)))}")

    # =========================
    #   MODE COMPLET TRANSCRIPTION + DIARISATION
    # =========================
    else:
        print("\n🔀 Mode : TRANSCRIPTION + DIARISATION.")

        # --- Association transcription <-> speaker ---
        formatted_output = []
        assigned_speakers = []

        OVERLAP_THRESHOLD = 0.01  # seuil pour une association valable

        print("\n🔗 Association des segments transcription <-> speakers...")
        for t_segment in tqdm(transcript_segments, desc="Matching segments"):
            best_speaker = "inconnu"
            best_score = 0.0

            for s_segment in speaker_segments:
                score = segment_score(t_segment, s_segment)
                if score > best_score and score > OVERLAP_THRESHOLD:
                    best_score = score
                    best_speaker = s_segment["speaker"]

            start_time = format_time(t_segment["start"])
            end_time = format_time(t_segment["end"])
            text = t_segment["text"]

            formatted_output.append(
                f"[{start_time} - {end_time}] 🗣️ Speaker {best_speaker}: {text}"
            )
            assigned_speakers.append(best_speaker)

        # --- Résumé temps de parole par speaker ---
        speaker_durations = {}
        for s in speaker_segments:
            speaker_durations[s["speaker"]] = speaker_durations.get(s["speaker"], 0.0) + (s["end"] - s["start"])

        speaker_durations_formatted = {
            speaker: str(datetime.timedelta(seconds=int(duration)))
            for speaker, duration in speaker_durations.items()
        }

        print("\n⏳ Temps de parole par speaker :")
        for speaker, duration in speaker_durations_formatted.items():
            print(f"🗣️ Speaker {speaker}: {duration}")

        print("\n📜 Aperçu de la transcription (non fusionnée) :")
        for line in formatted_output[:10]:
            print(line)
        if len(formatted_output) > 10:
            print("... (voir fichier pour le reste)")

        # --- Construction des segments fusionnés (pour le fichier de sortie) ---
        segments = []
        for t, spk in zip(transcript_segments, assigned_speakers):
            segments.append({
                "start": float(t["start"]),
                "end": float(t["end"]),
                "speaker": spk,
                "text": t.get("text", "")
            })

        segments_merged = merge_by_runs(segments)

        # --- Écriture dans le fichier ---
        with open(output_file, "w", encoding="utf-8") as f:
            f.write("⏳ Temps de parole par speaker :\n")
            for speaker, duration in speaker_durations_formatted.items():
                f.write(f"🗣️ Speaker {speaker}: {duration}\n")

            f.write("\n📜 Transcription fusionnée par speaker :\n\n")
            for s in segments_merged:
                f.write(f"[{hhmmss(s['start'])}–{hhmmss(s['end'])}] {s['speaker']}: {s['text'].strip()}\n")

        print(f"\n✅ Transcription complète sauvegardée dans : {output_file}")

        # --- Résumé final ---
        total_speech_duration = sum(speaker_durations.values())
        average_duration = total_speech_duration / len(speaker_durations) if speaker_durations else 0.0

        print(f"\n📊 Résumé global :")
        print(f"- Durée totale de l'audio analysé : {str(datetime.timedelta(seconds=int(audio_total_duration)))}")
        print(f"- Somme des temps de parole (tous speakers cumulés) : {str(datetime.timedelta(seconds=int(total_speech_duration)))}")
        print(f"- Nombre de speakers : {len(speaker_durations)}")
        print(f"- Durée moyenne par speaker : {str(datetime.timedelta(seconds=int(average_duration)))}")

    # --- Nettoyage fichiers temporaires ---
    if (not keep_temp
        and input_path != original_input_path
        and input_path.startswith(tempfile.gettempdir())):
        try:
            os.unlink(input_path)
            print("\n🧹 Fichier temporaire supprimé.")
        except OSError as e:
            print(f"\n⚠️ Impossible de supprimer le fichier temporaire : {e}")
    elif keep_temp:
        print(f"\n📂 Fichier temporaire conservé : {input_path}")


if __name__ == "__main__":
    main()
