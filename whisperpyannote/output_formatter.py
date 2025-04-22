import datetime

def format_time(seconds):
    return str(datetime.timedelta(seconds=int(seconds)))

def compute_speaker_durations(speaker_segments):
    speaker_durations = {}
    for s in speaker_segments:
        speaker_durations[s["speaker"]] = speaker_durations.get(s["speaker"], 0) + (s["end"] - s["start"])
    return speaker_durations

def assign_speakers(transcripts, speakers):
    assigned_segments = []
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

        assigned_segments.append({
            "speaker": best_speaker,
            "start": t_segment["start"],
            "end": t_segment["end"],
            "text": t_segment["text"]
        })
    return assigned_segments

def format_output(transcripts, speakers, style="markdown"):
    """
    Formats the transcription and diarization output.

    Parameters:
    - transcripts: list of transcription segments
    - speakers: list of speaker diarization segments
    - style: output style ("simple", "markdown", "per_speaker")

    Returns:
    - formatted text output (str)
    """
    output_lines = []

    # Résumé du temps de parole
    speaker_durations = compute_speaker_durations(speakers)

    output_lines.append("⏳ Temps de parole par speaker :\n")
    for speaker, duration in speaker_durations.items():
        output_lines.append(f"- Speaker {speaker} : {format_time(duration)}")

    output_lines.append("\n---\n")

    # Attribuer les speakers aux segments
    assigned_segments = assign_speakers(transcripts, speakers)

    if style == "markdown":
        for segment in assigned_segments:
            output_lines.append(f"## Speaker {segment['speaker']}")
            output_lines.append(f"- **{format_time(segment['start'])} - {format_time(segment['end'])}** : {segment['text']}\n")
    elif style == "simple":
        for segment in assigned_segments:
            output_lines.append(f"[{format_time(segment['start'])} - {format_time(segment['end'])}] Speaker {segment['speaker']}: {segment['text']}")
    elif style == "per_speaker":
        speakers_texts = {}
        for segment in assigned_segments:
            speakers_texts.setdefault(segment["speaker"], []).append(segment["text"])

        for speaker, texts in speakers_texts.items():
            output_lines.append(f"## Speaker {speaker}")
            for t in texts:
                output_lines.append(f"- {t}")
            output_lines.append("\n")
    else:
        # fallback par défaut
        for segment in assigned_segments:
            output_lines.append(f"[{format_time(segment['start'])} - {format_time(segment['end'])}] Speaker {segment['speaker']}: {segment['text']}")

    return "\n".join(output_lines)
