import datetime

def format_time(seconds):
    return str(datetime.timedelta(seconds=int(seconds)))

def compute_speaker_durations(speaker_segments):
    speaker_durations = {}
    for s in speaker_segments:
        speaker_durations[s["speaker"]] = speaker_durations.get(s["speaker"], 0) + (s["end"] - s["start"])
    return speaker_durations

def format_output(transcripts, speakers, style="markdown"):
    """
    Formats the transcription and diarization output.

    Parameters:
    - transcripts: list of transcription segments
    - speakers: list of speaker diarization segments
    - style: output style ("simple" or "markdown")

    Returns:
    - formatted text output (str)
    """
    output_lines = []

    # Temps de parole
    speaker_durations = compute_speaker_durations(speakers)

    output_lines.append("⏳ Temps de parole par speaker :\n")
    for speaker, duration in speaker_durations.items():
        output_lines.append(f"- Speaker {speaker} : {format_time(duration)}")

    output_lines.append("\n---\n")

    # Texte par segments
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
        text = t_segment['text']

        if style == "markdown":
            output_lines.append(f"## Speaker {best_speaker}")
            output_lines.append(f"- **{start_time} - {end_time}** : {text}\n")
        else:
            output_lines.append(f"[{start_time} - {end_time}] Speaker {best_speaker}: {text}")

    return "\n".join(output_lines)
