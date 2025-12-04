# 🎧 whisperpyannote — Audio & Video Transcription + Speaker Diarization

**whisperpyannote** is a Python script that performs:

- 📝 automatic speech transcription
- 🗣️ speaker diarization (who speaks when)
- 🎥 on both audio and video files

It combines the power of **Whisper (OpenAI)** for transcription and **Pyannote** for speaker identification.

---

## 🙏 Acknowledgements

This project relies on two major open‑source technologies:

- **Whisper (OpenAI)** — automatic speech transcription  
- **Pyannote Audio** and the community model **speaker-diarization-community-1** — speaker diarization  

Thanks to the developers, maintainers, and the Pyannote community for providing high‑quality open models accessible to everyone.

---

## ✨ Features

- 🎥 Automatic audio extraction from videos (FFmpeg)
- 🔄 Auto‑conversion to **mono 16 kHz**
- 📝 High‑quality Whisper transcription
- 🗣️ Accurate Pyannote speaker diarization
- 🧠 Smart merging of consecutive segments per speaker
- ⏳ Automatic speaking‑time calculation
- 📜 Clean TXT export with timestamps + speakers
- 📈 Progress bars (tqdm)
- 🔧 Modes: transcription only, diarization only, or both

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/nantaidsl95/whisperpyannote.git
cd whisperpyannote
```

### 2. Install FFmpeg  
Required for audio extraction and conversion.

### 3. Create a virtual environment (optional)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Hugging Face Token (required for Pyannote)

1. Open the model page: https://huggingface.co/pyannote/speaker-diarization-community-1  
2. Request access  
3. Create your HF token: https://huggingface.co/settings/tokens  
4. Export it:

```bash
export HUGGINGFACE_TOKEN="your_token"
```

Without this token, diarization will fail with **403 Unauthorized**.

---

# 🛠️ Full CLI Options

## Required arguments

| Argument | Description |
|---------|-------------|
| `input_path` | Audio/video file to process |
| `output_file` | Output TXT file |

---

## Transcription & Diarization options

| Option | Description | Values |
|--------|-------------|--------|
| `--whisper_model` | Whisper model | tiny, base, small, medium, large, turbo |
| `--language` | Force Whisper language | e.g., en, fr, de |

---

## Mutually exclusive modes

| Option | Description |
|--------|-------------|
| `--transcription_only` | Only run Whisper transcription |
| `--diarization_only` | Only run Pyannote diarization |

---

## Hugging Face token management

| Option | Description |
|--------|-------------|
| `--hf_token` | Provide token directly |
| `--ask_token` | Force interactive prompt |

Environment variables also supported:
- `HF_TOKEN`
- `HUGGINGFACE_TOKEN`

---

## Temporary file handling

| Option | Description |
|--------|-------------|
| `--keep_temp` | Keep extracted/converted WAV files |

---

# 🚀 Usage Examples

## Full transcription + diarization
```bash
python whisperpyannote.py input.mp4 output.txt
```

## Transcription only
```bash
python whisperpyannote.py audio.wav output.txt --transcription_only
```

## Diarization only
```bash
python whisperpyannote.py audio.wav output.txt --diarization_only
```

## Force model
```bash
python whisperpyannote.py audio.wav output.txt --whisper_model medium
```

## Provide token
```bash
python whisperpyannote.py audio.wav output.txt --hf_token "hf_xxx"
```

---

## 📜 Example Output

```
⏳ Speaking time per speaker:
SPEAKER_00: 00:12:34
SPEAKER_01: 00:08:45

[00:00:01–00:00:05] SPEAKER_00: Hello everyone!
[00:00:06–00:00:10] SPEAKER_01: Hi, how are you?
...
```

---

## 📁 Project Structure

```
whisperpyannote/
├── whisperpyannote.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## 📄 License

# 🎧 whisperpyannote — Audio & Video Transcription + Speaker Diarization

**whisperpyannote** is a Python script that performs:

- 📝 automatic speech transcription
- 🗣️ speaker diarization (who speaks when)
- 🎥 on both audio and video files

It combines the power of **Whisper (OpenAI)** for transcription and **Pyannote** for speaker identification.

---

## 🙏 Acknowledgements

This project relies on two major open‑source technologies:

- **Whisper (OpenAI)** — automatic speech transcription  
- **Pyannote Audio** and the community model **speaker-diarization-community-1** — speaker diarization  

Thanks to the developers, maintainers, and the Pyannote community for providing high‑quality open models accessible to everyone.

---

## ✨ Features

- 🎥 Automatic audio extraction from videos (FFmpeg)
- 🔄 Auto‑conversion to **mono 16 kHz**
- 📝 High‑quality Whisper transcription
- 🗣️ Accurate Pyannote speaker diarization
- 🧠 Smart merging of consecutive segments per speaker
- ⏳ Automatic speaking‑time calculation
- 📜 Clean TXT export with timestamps + speakers
- 📈 Progress bars (tqdm)
- 🔧 Modes: transcription only, diarization only, or both

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/nantaidsl95/whisperpyannote.git
cd whisperpyannote
```

### 2. Install FFmpeg  
Required for audio extraction and conversion.

### 3. Create a virtual environment (optional)
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Hugging Face Token (required for Pyannote)

1. Open the model page: https://huggingface.co/pyannote/speaker-diarization-community-1  
2. Request access  
3. Create your HF token: https://huggingface.co/settings/tokens  
4. Export it:

```bash
export HUGGINGFACE_TOKEN="your_token"
```

Without this token, diarization will fail with **403 Unauthorized**.

---

# 🛠️ Full CLI Options

## Required arguments

| Argument | Description |
|---------|-------------|
| `input_path` | Audio/video file to process |
| `output_file` | Output TXT file |

---

## Transcription & Diarization options

| Option | Description | Values |
|--------|-------------|--------|
| `--whisper_model` | Whisper model | tiny, base, small, medium, large, turbo |
| `--language` | Force Whisper language | e.g., en, fr, de |

---

## Mutually exclusive modes

| Option | Description |
|--------|-------------|
| `--transcription_only` | Only run Whisper transcription |
| `--diarization_only` | Only run Pyannote diarization |

---

## Hugging Face token management

| Option | Description |
|--------|-------------|
| `--hf_token` | Provide token directly |
| `--ask_token` | Force interactive prompt |

Environment variables also supported:
- `HF_TOKEN`
- `HUGGINGFACE_TOKEN`

---

## Temporary file handling

| Option | Description |
|--------|-------------|
| `--keep_temp` | Keep extracted/converted WAV files |

---

# 🚀 Usage Examples

## Full transcription + diarization
```bash
python whisperpyannote.py input.mp4 output.txt
```

## Transcription only
```bash
python whisperpyannote.py audio.wav output.txt --transcription_only
```

## Diarization only
```bash
python whisperpyannote.py audio.wav output.txt --diarization_only
```

## Force model
```bash
python whisperpyannote.py audio.wav output.txt --whisper_model medium
```

## Provide token
```bash
python whisperpyannote.py audio.wav output.txt --hf_token "hf_xxx"
```

---

## 📜 Example Output

```
⏳ Speaking time per speaker:
SPEAKER_00: 00:12:34
SPEAKER_01: 00:08:45

[00:00:01–00:00:05] SPEAKER_00: Hello everyone!
[00:00:06–00:00:10] SPEAKER_01: Hi, how are you?
...
```

---

## 📁 Project Structure

```
whisperpyannote/
├── whisperpyannote.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## 📄 License

This project is distributed under the [MIT License](./LICENSE).

---

## 👤 Author

Developed by **Marc Delage**  
GitHub → https://github.com/nantaidsl95


---

## 👤 Author

Developed by **Marc Delage**  
GitHub → https://github.com/nantaidsl95
