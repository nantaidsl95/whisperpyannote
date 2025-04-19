import whisper

def transcribe(audio_path, model_size="turbo"):
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_path)
    return result["segments"]
