import argparse
from whisperpyannote.transcription import transcribe
from whisperpyannote.diarization import diarize
from whisperpyannote.utils import prepare_audio, save_output, clean_temp
from whisperpyannote.output_formatter import format_output

def run():
    parser = argparse.ArgumentParser(description="Transcrire et diariser un fichier audio ou vidéo.")
    parser.add_argument("input_path", help="Chemin du fichier audio ou vidéo à traiter")
    parser.add_argument("output_file", help="Chemin du fichier texte de sortie")
    parser.add_argument("--whisper_model", default="turbo", help="Modèle Whisper à utiliser (tiny, base, small, medium, large, turbo)")
    parser.add_argument("--keep_temp", action="store_true", help="Conserver les fichiers temporaires générés")
    parser.add_argument("--language", default=None, help="Langue du contenu audio (ex: fr, en, es, etc.)")
    parser.add_argument("--output_style", default="markdown", choices=["simple", "markdown", "per_speaker"],
                        help="Style de sortie du fichier (simple, markdown, per_speaker)")

    args = parser.parse_args()

    # Préparation du fichier audio
    audio_path = prepare_audio(args.input_path)

    # Transcription
    transcripts = transcribe(audio_path, model_size=args.whisper_model, language=args.language)

    # Diarisation
    speakers = diarize(audio_path)

    # Formatage de la sortie selon le style choisi
    formatted = format_output(transcripts, speakers, style=args.output_style)

    # Sauvegarde dans le fichier de sortie
    save_output(args.output_file, formatted)

    # Nettoyage du fichier temporaire
    if not args.keep_temp:
        clean_temp(audio_path)
