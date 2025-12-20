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
import json
import whisper
from tqdm import tqdm
from pyannote.audio import Pipeline
import torchaudio
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
        print(f"ERREUR lors de l'execution de la commande : {e}")
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

    print("Extraction audio depuis la video...")
    run_command([
        "ffmpeg", "-i", video_path,
        "-ac", "1", "-ar", "16000",
        "-vn", "-y",
        audio_output
    ])
    print(f"OK Audio extrait : {audio_output}")
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

    print("Conversion de l'audio au format 16kHz mono...")
    run_command([
        "ffmpeg", "-i", audio_path,
        "-ac", "1", "-ar", "16000",
        "-y",
        converted_audio
    ])
    print(f"OK Audio converti : {converted_audio}")
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
    sep = "" if a.endswith(("—", "-", "...", ":", "(", "[", "{", "/")) else " "
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

    segments = sorted(segments, key=lambda s: (s["start"], s["end"]))
    merged = []
    cur = dict(segments[0])

    for seg in segments[1:]:
        if seg["speaker"] == cur["speaker"]:
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


# =========================
#   Sorties JSON / SRT / VTT
# =========================

def json_path_for_output(output_file: str) -> str:
    if output_file.lower().endswith(".json"):
        return output_file
    return output_file + ".json"


def write_json_if_requested(args, output_file: str, payload: dict):
    if not getattr(args, "json", False):
        return
    out_json = json_path_for_output(output_file)
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
    print(f"\nOK JSON sauvegarde dans : {out_json}")


def replace_ext(path: str, new_ext: str) -> str:
    root, _ = os.path.splitext(path)
    if not new_ext.startswith("."):
        new_ext = "." + new_ext
    return root + new_ext


def _clamp_time(t: float) -> float:
    try:
        return max(0.0, float(t))
    except Exception:
        return 0.0


def format_srt_timestamp(seconds: float) -> str:
    """HH:MM:SS,mmm"""
    seconds = _clamp_time(seconds)
    ms_total = int(round(seconds * 1000.0))
    s_total = ms_total // 1000
    ms = ms_total % 1000
    hh = s_total // 3600
    mm = (s_total % 3600) // 60
    ss = s_total % 60
    return f"{hh:02d}:{mm:02d}:{ss:02d},{ms:03d}"


def format_vtt_timestamp(seconds: float) -> str:
    """HH:MM:SS.mmm"""
    seconds = _clamp_time(seconds)
    ms_total = int(round(seconds * 1000.0))
    s_total = ms_total // 1000
    ms = ms_total % 1000
    hh = s_total // 3600
    mm = (s_total % 3600) // 60
    ss = s_total % 60
    return f"{hh:02d}:{mm:02d}:{ss:02d}.{ms:03d}"


def write_srt(segments, out_path: str, include_speaker: bool = True):
    """
    segments: liste de dicts {"start","end","text", "speaker"?}
    """
    with open(out_path, "w", encoding="utf-8") as f:
        idx = 1
        for seg in segments:
            text = (seg.get("text", "") or "").strip()
            if not text:
                continue
            start = format_srt_timestamp(seg.get("start", 0.0))
            end = format_srt_timestamp(seg.get("end", 0.0))
            if include_speaker and seg.get("speaker") not in (None, "", "inconnu"):
                text = f"{seg['speaker']}: {text}"
            f.write(f"{idx}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")
            idx += 1
    print(f"\nOK SRT sauvegarde dans : {out_path}")


def write_vtt(segments, out_path: str, include_speaker: bool = True):
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")
        for seg in segments:
            text = (seg.get("text", "") or "").strip()
            if not text:
                continue
            start = format_vtt_timestamp(seg.get("start", 0.0))
            end = format_vtt_timestamp(seg.get("end", 0.0))
            if include_speaker and seg.get("speaker") not in (None, "", "inconnu"):
                text = f"{seg['speaker']}: {text}"
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")
    print(f"\nOK VTT sauvegarde dans : {out_path}")


def write_subtitles_if_requested(args, output_file: str, segments, include_speaker: bool = True):
    """
    Génère .srt et/ou .vtt si demandé via CLI.
    """
    if getattr(args, "srt", False):
        out_srt = replace_ext(output_file, ".srt")
        write_srt(segments, out_srt, include_speaker=include_speaker)
    if getattr(args, "vtt", False):
        out_vtt = replace_ext(output_file, ".vtt")
        write_vtt(segments, out_vtt, include_speaker=include_speaker)


# =============================
#   Gestion du token HF
# =============================

def get_hf_token(args) -> str:
    env_token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGINGFACE_TOKEN")
    if env_token:
        return env_token.strip()

    if args.hf_token:
        return args.hf_token.strip()

    if args.ask_token and not sys.stdin.isatty():
        print("ERREUR --ask_token demande mais impossible de lire depuis stdin (mode non interactif).")
        sys.exit(1)

    if sys.stdin.isatty():
        try:
            token = input("Aucun token Hugging Face detecte. Entrez votre token : ").strip()
        except EOFError:
            token = ""
        if token:
            return token
        print("ERREUR Aucun token saisi.")
        sys.exit(1)

    print("INFO Aucun token Hugging Face disponible (ni variable d'environnement, ni CLI, ni saisie interactive possible).")
    print("     Veuillez definir HF_TOKEN ou HUGGINGFACE_TOKEN, ou utiliser --hf_token.")
    sys.exit(1)


# =============================
#   Transcription Whisper
# =============================

def load_whisper_model(whisper_model_choice: str):
    # Priorité: CUDA > MPS > CPU
    if torch.cuda.is_available():
        device = "cuda"
    elif getattr(torch.backends, "mps", None) is not None and torch.backends.mps.is_available():
        device = "mps"
    else:
        device = "cpu"

    print(f"\nChargement du modele Whisper '{whisper_model_choice}' (device={device})...")
    model = whisper.load_model(whisper_model_choice, device=device)
    return model, device


def run_whisper_transcription(model, audio_path: str, language: str = None, device: str = None):
    print("Transcription en cours... (cela peut prendre un moment)")
    transcribe_kwargs = {}
    if language:
        transcribe_kwargs["language"] = language
        print(f"Langue forcee pour Whisper : {language}")

    # Important: fp16 uniquement sur CUDA (plus stable sur CPU/MPS)
    if device is None:
        try:
            device = str(next(model.parameters()).device)
        except Exception:
            device = "cpu"
    transcribe_kwargs["fp16"] = (device == "cuda")

    result = model.transcribe(audio_path, **transcribe_kwargs)
    return result


# =============================
#   Diarisation Pyannote
# =============================

def prepare_safe_globals():
    try:
        add_safe_globals([Specifications, Problem, Resolution])
    except Exception as e:
        print("ATTENTION Impossible d'ajouter Specifications/Problem/Resolution aux safe_globals :", e)


def run_diarization(audio_path: str, hf_token: str):
    print("\nDiarisation avec Pyannote en cours...")

    prepare_safe_globals()

    try:
        pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization-community-1",
            token=hf_token,
        )
    except Exception as e:
        print("ERREUR lors du chargement de la pipeline pyannote/speaker-diarization-community-1 :")
        print(e)
        sys.exit(1)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    try:
        pipeline.to(device)
    except Exception:
        pass

    try:
        waveform, sample_rate = torchaudio.load(audio_path)
    except Exception as e:
        print("ERREUR lors du chargement audio avec torchaudio :")
        print(e)
        sys.exit(1)

    try:
        waveform = waveform.to(device)
    except Exception:
        pass

    diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate})

    speaker_segments = []

    annotation = getattr(diarization, "speaker_diarization", diarization)

    for segment, _, speaker in annotation.itertracks(yield_label=True):
        speaker_segments.append({
            "speaker": speaker,
            "start": segment.start,
            "end": segment.end,
        })

    print(f"OK {len(speaker_segments)} segments de speakers detectes.")
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

    parser.add_argument(
        "--json",
        action="store_true",
        help="Écrire en plus un fichier JSON à côté du fichier texte (output_file.json)."
    )

    # === AJOUT : options SRT / VTT ===
    parser.add_argument(
        "--srt",
        action="store_true",
        help="Écrire en plus un fichier .srt (même base que output_file)."
    )
    parser.add_argument(
        "--vtt",
        action="store_true",
        help="Écrire en plus un fichier .vtt (même base que output_file)."
    )
    parser.add_argument(
        "--subs_no_speaker",
        action="store_true",
        help="Ne pas préfixer les sous-titres avec le speaker (utile pour un SRT/VTT plus 'classique')."
    )

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

    execution_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    input_path = args.input_path
    output_file = args.output_file
    whisper_model_choice = args.whisper_model
    keep_temp = args.keep_temp
    language = args.language

    transcription_only = args.transcription_only
    diarization_only = args.diarization_only

    if not os.path.exists(input_path):
        print(f"ATTENTION Fichier introuvable : {input_path}")
        sys.exit(1)

    original_input_path = input_path
    temp_files = []

    source_name = os.path.basename(original_input_path)
    language_label = language if language else "auto-détection"
    header = (
        "Metadonnees de transcription\n"
        f"- Fichier source : {source_name}\n"
        f"- Modèle Whisper : {whisper_model_choice}\n"
        f"- Langue Whisper : {language_label}\n"
        f"- Date d'exécution : {execution_time}\n"
        "\n"
        "----------------------------------------\n\n"
    )

    json_meta = {
        "source_file": source_name,
        "source_path": original_input_path,
        "whisper_model": whisper_model_choice,
        "whisper_language": language_label,
        "execution_time": execution_time,
    }

    if is_video(input_path):
        input_path = extract_audio(input_path)
        temp_files.append(input_path)

    if not is_valid_audio(input_path):
        converted = convert_audio(input_path)
        temp_files.append(converted)
        input_path = converted

    audio_total_duration = get_audio_duration_seconds(input_path)

    transcript_segments = None
    speaker_segments = []
    waveform = None
    sample_rate = None

    if not diarization_only:
        model, whisper_device = load_whisper_model(whisper_model_choice)
        result = run_whisper_transcription(model, input_path, language=language, device=whisper_device)
        transcript_segments = result["segments"]

    if not transcription_only:
        hf_token = get_hf_token(args)
        speaker_segments, waveform, sample_rate = run_diarization(input_path, hf_token)

    include_speaker_in_subs = not args.subs_no_speaker

    # =========================
    #   MODE TRANSCRIPTION SEULE
    # =========================
    if transcription_only and not diarization_only:
        print("\nMode : TRANSCRIPTION SEULE (pas de diarisation).")

        print("\nApercu de la transcription :")
        for seg in (transcript_segments or [])[:10]:
            print(f"[{format_time(seg['start'])} - {format_time(seg['end'])}] {seg['text']}")
        if transcript_segments and len(transcript_segments) > 10:
            print("... (voir fichier pour le reste)")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(header)
            f.write("Transcription (sans diarisation) :\n\n")
            if not transcript_segments:
                f.write("(Aucun segment de transcription.)\n")
            else:
                for t in transcript_segments:
                    f.write(f"[{hhmmss(float(t['start']))}-{hhmmss(float(t['end']))}] {t.get('text', '').strip()}\n")

        print(f"\nOK Transcription sauvegardee dans : {output_file}")

        # Sous-titres (basés sur Whisper)
        subs_segments = [
            {"start": float(t["start"]), "end": float(t["end"]), "text": (t.get("text", "") or "").strip(), "speaker": None}
            for t in (transcript_segments or [])
        ]
        write_subtitles_if_requested(args, output_file, subs_segments, include_speaker=include_speaker_in_subs)

        json_payload = {
            "meta": {**json_meta, "mode": "transcription_only", "audio_duration_seconds": audio_total_duration},
            "transcription": [
                {
                    "start": float(t["start"]),
                    "end": float(t["end"]),
                    "start_hhmmss": hhmmss(float(t["start"])),
                    "end_hhmmss": hhmmss(float(t["end"])),
                    "text": (t.get("text", "") or "").strip(),
                }
                for t in (transcript_segments or [])
            ],
        }
        write_json_if_requested(args, output_file, json_payload)

        print(f"\nResume global :")
        print(f"- Duree totale de l'audio analyse : {str(datetime.timedelta(seconds=int(audio_total_duration)))}")
        print(f"- Nombre de segments de transcription : {len(transcript_segments) if transcript_segments else 0}")

    # =========================
    #   MODE DIARISATION SEULE
    # =========================
    elif diarization_only and not transcription_only:
        print("\nMode : DIARISATION SEULE (pas de transcription Whisper).")

        speaker_durations = {}
        for s in speaker_segments:
            speaker_durations[s["speaker"]] = speaker_durations.get(s["speaker"], 0.0) + (s["end"] - s["start"])

        speaker_durations_formatted = {
            speaker: str(datetime.timedelta(seconds=int(duration)))
            for speaker, duration in speaker_durations.items()
        }

        print("\nTemps de parole par speaker :")
        for speaker, duration in speaker_durations_formatted.items():
            print(f"Speaker {speaker}: {duration}")

        print("\nApercu des segments de diarisation (sans texte) :")
        for seg in speaker_segments[:10]:
            print(f"[{hhmmss(seg['start'])}-{hhmmss(seg['end'])}] {seg['speaker']}")
        if len(speaker_segments) > 10:
            print("... (voir fichier pour le reste)")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(header)
            f.write("Temps de parole par speaker :\n")
            for speaker, duration in speaker_durations_formatted.items():
                f.write(f"Speaker {speaker}: {duration}\n")

            f.write("\nSegments de diarisation (sans transcription) :\n\n")
            if not speaker_segments:
                f.write("(Aucun segment de diarisation.)\n")
            else:
                for s in speaker_segments:
                    f.write(f"[{hhmmss(s['start'])}-{hhmmss(s['end'])}] {s['speaker']}\n")

        print(f"\nOK Diarisation sauvegardee dans : {output_file}")

        # Pas de SRT/VTT possible ici (pas de texte)
        if args.srt or args.vtt:
            print("\nATTENTION SRT/VTT non generes en mode diarisation seule (pas de transcription/texte).")

        json_payload = {
            "meta": {**json_meta, "mode": "diarization_only", "audio_duration_seconds": audio_total_duration},
            "speakers": [
                {"speaker": spk, "duration_seconds": float(dur), "duration_hhmmss": speaker_durations_formatted[spk]}
                for spk, dur in speaker_durations.items()
            ],
            "segments": [
                {
                    "speaker": s["speaker"],
                    "start": float(s["start"]),
                    "end": float(s["end"]),
                    "start_hhmmss": hhmmss(float(s["start"])),
                    "end_hhmmss": hhmmss(float(s["end"])),
                }
                for s in (speaker_segments or [])
            ],
        }
        write_json_if_requested(args, output_file, json_payload)

        total_speech_duration = sum(speaker_durations.values())
        average_duration = total_speech_duration / len(speaker_durations) if speaker_durations else 0.0

        print(f"\nResume global :")
        print(f"- Duree totale de l'audio analyse : {str(datetime.timedelta(seconds=int(audio_total_duration)))}")
        print(f"- Somme des temps de parole (tous speakers cumules) : {str(datetime.timedelta(seconds=int(total_speech_duration)))}")
        print(f"- Nombre de speakers : {len(speaker_durations)}")
        print(f"- Duree moyenne par speaker : {str(datetime.timedelta(seconds=int(average_duration)))}")

    # =========================
    #   MODE COMPLET
    # =========================
    else:
        print("\nMode : TRANSCRIPTION + DIARISATION.")

        formatted_output = []
        assigned_speakers = []

        OVERLAP_THRESHOLD = 0.01

        print("\nAssociation des segments transcription <-> speakers...")
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
                f"[{start_time} - {end_time}] Speaker {best_speaker}: {text}"
            )
            assigned_speakers.append(best_speaker)

        speaker_durations = {}
        for s in speaker_segments:
            speaker_durations[s["speaker"]] = speaker_durations.get(s["speaker"], 0.0) + (s["end"] - s["start"])

        speaker_durations_formatted = {
            speaker: str(datetime.timedelta(seconds=int(duration)))
            for speaker, duration in speaker_durations.items()
        }

        print("\nTemps de parole par speaker :")
        for speaker, duration in speaker_durations_formatted.items():
            print(f"Speaker {speaker}: {duration}")

        print("\nApercu de la transcription (non fusionnee) :")
        for line in formatted_output[:10]:
            print(line)
        if len(formatted_output) > 10:
            print("... (voir fichier pour le reste)")

        segments = []
        for t, spk in zip(transcript_segments, assigned_speakers):
            segments.append({
                "start": float(t["start"]),
                "end": float(t["end"]),
                "speaker": spk,
                "text": t.get("text", "")
            })

        segments_merged = merge_by_runs(segments)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(header)
            f.write("Temps de parole par speaker :\n")
            for speaker, duration in speaker_durations_formatted.items():
                f.write(f"Speaker {speaker}: {duration}\n")

            f.write("\nTranscription fusionnee par speaker :\n\n")
            for s in segments_merged:
                f.write(f"[{hhmmss(s['start'])}-{hhmmss(s['end'])}] {s['speaker']}: {s['text'].strip()}\n")

        print(f"\nOK Transcription complete sauvegardee dans : {output_file}")

        # Sous-titres (basés sur segments fusionnés)
        subs_segments = [
            {"start": float(s["start"]), "end": float(s["end"]), "text": (s.get("text", "") or "").strip(), "speaker": s.get("speaker")}
            for s in (segments_merged or [])
        ]
        write_subtitles_if_requested(args, output_file, subs_segments, include_speaker=include_speaker_in_subs)

        json_payload = {
            "meta": {**json_meta, "mode": "transcription_and_diarization", "audio_duration_seconds": audio_total_duration},
            "speakers": [
                {"speaker": spk, "duration_seconds": float(dur), "duration_hhmmss": speaker_durations_formatted[spk]}
                for spk, dur in speaker_durations.items()
            ],
            "segments_merged": [
                {
                    "speaker": s["speaker"],
                    "start": float(s["start"]),
                    "end": float(s["end"]),
                    "start_hhmmss": hhmmss(float(s["start"])),
                    "end_hhmmss": hhmmss(float(s["end"])),
                    "text": (s.get("text", "") or "").strip(),
                }
                for s in (segments_merged or [])
            ],
        }
        write_json_if_requested(args, output_file, json_payload)

        total_speech_duration = sum(speaker_durations.values())
        average_duration = total_speech_duration / len(speaker_durations) if speaker_durations else 0.0

        print(f"\nResume global :")
        print(f"- Duree totale de l'audio analyse : {str(datetime.timedelta(seconds=int(audio_total_duration)))}")
        print(f"- Somme des temps de parole (tous speakers cumules) : {str(datetime.timedelta(seconds=int(total_speech_duration)))}")
        print(f"- Nombre de speakers : {len(speaker_durations)}")
        print(f"- Duree moyenne par speaker : {str(datetime.timedelta(seconds=int(average_duration)))}")

    # --- Nettoyage fichiers temporaires (TOUS) ---
    if keep_temp:
        for p in temp_files:
            print(f"\nFichier temporaire conserve : {p}")
    else:
        for p in temp_files:
            try:
                if p and os.path.exists(p) and p.startswith(tempfile.gettempdir()):
                    os.unlink(p)
                    print(f"\nFichier temporaire supprime : {p}")
            except OSError as e:
                print(f"\nATTENTION Impossible de supprimer le fichier temporaire {p} : {e}")


if __name__ == "__main__":
    main()
