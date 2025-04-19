import os
import tempfile
import subprocess
import wave
import datetime

def run_command(command):
    subprocess.run(command, check=True)

def is_video(file_path):
    return file_path.lower().endswith(('.mp4', '.mkv', '.mov', '.avi', '.flv', '.webm'))

def extract_audio(video_path):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        output = tmpfile.name
    run_command(["ffmpeg", "-i", video_path, "-ac", "1", "-ar", "16000", "-vn", "-y", output])
    return output

def convert_audio(audio_path):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        output = tmpfile.name
    run_command(["ffmpeg", "-i", audio_path, "-ac", "1", "-ar", "16000", "-y", output])
    return output

def is_valid_audio(file_path):
    try:
        with wave.open(file_path, 'rb') as audio:
            return audio.getframerate() == 16000 and audio.getnchannels() == 1
    except Exception:
        return False

def prepare_audio(input_path):
    if is_video(input_path):
        input_path = extract_audio(input_path)
    if not is_valid_audio(input_path):
        input_path = convert_audio(input_path)
    return input_path

def format_time(seconds):
    return str(datetime.timedelta(seconds=int(seconds)))

def format_output(transcripts, speakers):
    output_lines = []
    for t_segment in transcripts:
        best_speaker = "inconnu"
        best_score = 0
        for s_segment in speakers:
            overlap = min(t_segment["end"], s_segment["end"]) - max(t_segment["start"], s_segment["start"])
            if overlap > 0:
                score = overlap / (t_segment["end"] - t_segment["start"])
                if score > best_score:
                    best_score = score
                    best_speaker = s_segment["speaker"]

        start_time = format_time(t_segment["start"])
        end_time = format_time(t_segment["end"])
        output_lines.append(f"[{start_time} - {end_time}] Speaker {best_speaker}: {t_segment['text']}")
    return "\n".join(output_lines)

def save_output(output_file, content):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(content)

def clean_temp(path):
    if path.startswith(tempfile.gettempdir()):
        os.unlink(path)
