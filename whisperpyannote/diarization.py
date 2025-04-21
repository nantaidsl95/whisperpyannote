from pyannote.audio import Pipeline
import os

def diarize(audio_path):
    HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
    if not HF_TOKEN:
        raise ValueError("Veuillez définir la variable d'environnement HUGGINGFACE_TOKEN.")
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.0", use_auth_token=HF_TOKEN)
    diarization = pipeline(audio_path)
    segments = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        segments.append({
            "speaker": speaker,
            "start": turn.start,
            "end": turn.end
        })
    return segments
