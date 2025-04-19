import argparse
from whisperpyannote.transcription import transcribe
from whisperpyannote.diarization import diarize
from whisperpyannote.utils import prepare_audio, format_output, save_output, clean_temp

def run():
    parser = argparse.ArgumentParser(description="Transcrire et diariser un fichier audio ou vidéo.")
    parser.add_argument("input_path", help="Chemin du fichier audio ou vidéo à traiter")
    parser.add_argument("output_file", help="Chemin du fichier texte de sortie")
    parser.add_argument("--whisper_model", default="turbo", help="Modèle Whisper à utiliser")
    parser.add_argument("--keep_temp", action="store_true", help="Conserver les fichiers temporaires")
    args = parser.parse_args()

    audio_path = prepare_audio(args.input_path)
    transcripts = transcribe(audio_path, args.whisper_model)
    speakers = diarize(audio_path)
    formatted = format_output(transcripts, speakers)
    save_output(args.output_file, formatted)

    if not args.keep_temp:
        clean_temp(audio_path)

