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

- 🎥 Automatic audio extraction from videos  
- 🔄 Conversion to mono 16 kHz  
- 📝 Whisper transcription  
- 🗣️ Pyannote diarization  
- 🧠 Smart merging of segments  
- ⏳ Speaking time per speaker  
- 📜 Clean final transcript  
- 📈 Progress bars with tqdm  

---

# 🎙️ Recording with OBS (recommended)

Steps:

1. Install OBS: https://obsproject.com/  
2. Add **Display Capture** or **Window Capture**  
3. Add **Audio Input Capture** (microphone)  
4. Optional: capture system audio  
   - macOS → install **BlackHole** (https://existential.audio/blackhole/)  
   - Windows → enable **Stereo Mix** or use **VB-Cable**  
5. Record in MP4 or MKV  
6. Use the recorded file with `whisperpyannote`

OBS recordings (.mp4, .mov, .mkv) work perfectly.

---

## 🚀 Installation

### 1️⃣ Clone the repository
```bash
git clone https://github.com/nantaidsl95/whisperpyannote.git
cd whisperpyannote
```

### 2️⃣ Install FFmpeg  

### 3️⃣ Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 4️⃣ Install Python dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 Hugging Face Token (required for Pyannote)

1. Request access: https://huggingface.co/pyannote/speaker-diarization-community-1  
2. Create a token: https://huggingface.co/settings/tokens  
3. Export it:

```bash
export HUGGINGFACE_TOKEN="your_token"
```

---

# 🛠️ Full CLI Options

### Required arguments

| Argument | Description |
|---------|-------------|
| `input_path` | Audio/video file to process |
| `output_file` | Output text file |

---

### Transcription & diarization options

| Option | Description | Values |
|--------|-------------|--------|
| `--whisper_model` | Whisper model | tiny, base, small, medium, large, turbo |
| `--language` | Force transcription language | en, fr, de… |

---

### Exclusive modes

| Option | Description |
|--------|-------------|
| `--transcription_only` | Only transcription |
| `--diarization_only` | Only diarization |

---

### Token management

| Option | Description |
|--------|-------------|
| `--hf_token` | Provide HF token directly |
| `--ask_token` | Force interactive prompt |

Also detected automatically:
- `HF_TOKEN`
- `HUGGINGFACE_TOKEN`

---

### Temporary files

| Option | Description |
|--------|-------------|
| `--keep_temp` | Keep temporary WAV files |

---

# 🚀 Usage Examples

```bash
python whisperpyannote.py input.mp4 output.txt
python whisperpyannote.py audio.wav output.txt --transcription_only
python whisperpyannote.py audio.wav output.txt --whisper_model medium
python whisperpyannote.py audio.wav output.txt --language fr
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

This project is distributed under the MIT License.  
See the [LICENSE](./LICENSE) file for details.

---

## 👤 Author

Developed by **Marc Delage**  
GitHub → https://github.com/nantaidsl95
