# 🎧 whisperpyannote — Audio & Video Transcription + Speaker Diarization

![License](https://img.shields.io/badge/License-MIT-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Whisper](https://img.shields.io/badge/Whisper-STT-orange)
![Pyannote](https://img.shields.io/badge/Pyannote-Diarization-purple)
![Status](https://img.shields.io/badge/Status-Active-success)
![PRs](https://img.shields.io/badge/PRs-Welcome-brightgreen)

**whisperpyannote** is a Python script that performs:

- 📝 automatic speech transcription  
- 🗣️ speaker diarization (who speaks when)  
- 🎥 on both audio and video files  

It combines **Whisper (OpenAI)** for transcription and **Pyannote Audio** for speaker identification.

🔗 Whisper → https://github.com/openai/whisper  
🔗 Pyannote community diarization model → https://huggingface.co/pyannote/speaker-diarization-community-1  

---

## 🙏 Acknowledgements

This project uses two major open-source components:

- **Whisper (OpenAI)** — MIT License  
- **Pyannote Audio** and the model **speaker-diarization-community-1** — MIT License  

Thanks to their authors, maintainers, and contributors for making high-quality open models available to everyone.

---

## ✨ Features

- 🎥 Automatic audio extraction from videos *(requires FFmpeg)*  
- 🔄 Conversion to mono 16 kHz *(requires FFmpeg)*  
- 📝 Whisper transcription  
- 🗣️ Pyannote diarization  
- 🧠 Smart merging of segments  
- ⏳ Speaking time per speaker  
- 📜 Clean final transcript  
- 📈 Progress bars with tqdm  
- 🎬 Optional subtitle generation (**SRT / VTT**)  
- 📄 Optional structured output (**JSON**)  

---

## ⚙️ System Requirement

**FFmpeg is required** and must be available in your system PATH.

The script relies on FFmpeg to:
- extract audio from video files
- convert audio to mono 16 kHz WAV

Audio/video inputs are automatically converted when needed.

### Install FFmpeg

- **macOS (Homebrew)**  
  ```
  brew install ffmpeg
  ```

- **Ubuntu / Debian**  
  ```
  sudo apt install ffmpeg
  ```

- **Windows**  
  Download from https://ffmpeg.org/download.html  
  and make sure `ffmpeg` is added to your PATH.

---

## 🔑 Hugging Face Token (required for Pyannote)

Diarization uses the model:

```
pyannote/speaker-diarization-community-1
```

Access to this model requires:
- accepting its conditions on Hugging Face
- a valid Hugging Face access token

The token can be provided in three ways:
- environment variables `HF_TOKEN` or `HUGGINGFACE_TOKEN`
- CLI option `--hf_token`
- interactive prompt (when running in a terminal)

---

## ⚠️ Known Limitations

- diarization accuracy may decrease with overlapping speakers
- some segments may be assigned to `unknown` speakers
- Whisper segmentation varies depending on the model
