# 🎧 whisperpyannote — Audio & Video Transcription + Speaker Diarization

![License](https://img.shields.io/badge/License-MIT-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Whisper](https://img.shields.io/badge/Whisper-STT-orange)
![Pyannote](https://img.shields.io/badge/Pyannote-Diarization-purple)
![Status](https://img.shields.io/badge/Status-Active-success)
![PRs](https://img.shields.io/badge/PRs-Welcome-brightgreen)

**whisperpyannote** is a Python script that performs:

- 📝 Automatic speech transcription  
- 🗣️ Speaker diarization (who speaks when)  
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
- 🎬 Optional subtitle export (**SRT / VTT**)  
- 📄 Optional structured output (**JSON**)  

---

## 🖥️ Graphical User Interface

A desktop GUI is available.  
See 👉 [GUI.md](./GUI.md)

---

## ⚙️ System Requirement

**FFmpeg is required** and must be available in your system PATH.

The script relies on FFmpeg to:
- Extract audio from video files
- Convert audio to mono 16 kHz WAV

> Audio/video inputs are automatically converted when needed.

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

- **Windows (via terminal – winget)**
  ```
  winget install Gyan.FFmpeg
  ```
  Then restart your terminal and verify:
  ```
  ffmpeg -version
  ```
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
```
git clone https://github.com/nantaidsl95/whisperpyannote.git
cd whisperpyannote
```

### 2️⃣ Install FFmpeg (required)

### 3️⃣ Create a virtual environment

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows (PowerShell)**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```
> ⚠️ If you get a PowerShell execution policy error, run PowerShell **as Administrator** and execute:
> ```powershell
> Set-ExecutionPolicy RemoteSigned
> ```
> Then reopen your terminal and activate the virtual environment again.

**Windows (Command Prompt / cmd.exe)**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

### 4️⃣ Install Python dependencies
```
pip install -r requirements.txt
```

---

## 🔑 Hugging Face Token (required for Pyannote)

Diarization uses the model:

```
pyannote/speaker-diarization-community-1
```

Speaker diarization relies on the Hugging Face model:

- **pyannote/speaker-diarization-community-1**  
  https://huggingface.co/pyannote/speaker-diarization-community-1

To use this model, you must complete **all** of the following steps:

1. **Accept the model terms**  
   Visit the model page and accept its usage conditions:  
   https://huggingface.co/pyannote/speaker-diarization-community-1

2. **Create a Hugging Face access token**  
   Go to the token settings page:  
   https://huggingface.co/settings/tokens  

   Create a new token with **Read** permissions.

3. **Export the token as an environment variable (recommended)**  

   **macOS / Linux**
   ```
   export HF_TOKEN="your_token_here"
   ```

   **Windows (PowerShell)**
   ```
   $env:HF_TOKEN="your_token_here"
   ```

   Using an environment variable is the safest method and avoids exposing the token in command history or scripts.

4. **Alternative methods (supported but not recommended)**  
   The token can also be provided via:
   - the `--hf_token` CLI option  
   - the interactive prompt (`--ask_token`)  

   Exporting the token remains the preferred approach.
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

### Output formats

| Option | Description |
|--------|-------------|
| `--json` | Write a JSON file alongside the text output |
| `--srt` | Generate SRT subtitles |
| `--vtt` | Generate VTT subtitles |
| `--subs_no_speaker` | Do not prefix subtitles with speaker labels |

Subtitles behavior:
- Transcription only → Whisper-based subtitles
- Full mode → speaker-merged subtitles
- Diarization only → no subtitles (no text)

---

### Temporary files

| Option | Description |
|--------|-------------|
| `--keep_temp` | Keep temporary WAV files |

---

# 🚀 Usage Examples

```
python whisperpyannote.py input.mp4 output.txt
python whisperpyannote.py audio.wav output.txt --transcription_only
python whisperpyannote.py audio.wav output.txt --diarization_only
python whisperpyannote.py audio.wav output.txt --whisper_model medium
python whisperpyannote.py audio.wav output.txt --language fr
python whisperpyannote.py input.mp4 output.txt --srt --vtt
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

## ⚠️ Known Limitations

- Diarization accuracy may decrease with overlapping speakers
- Some segments may be assigned to an `unknown` speaker
- Whisper segmentation depends on the selected model

---

## 📁 Project Structure

```
whisperpyannote/
├── .gitignore
├── GUI.md
├── LICENSE
├── README.md
├── requirements.txt
├── requirements_gui.txt
├── whisperpyannote.py
└── whisperpyannote_gui.py
```
---

## 📄 License

This project is distributed under the MIT License.  
See the [LICENSE](./LICENSE) file for details.

---

## 👤 Author

Developed by **Marc Delage**  
GitHub → https://github.com/nantaidsl95
