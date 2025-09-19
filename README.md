# Transcription & Diarisation Audio/Vidéo

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)  
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

Python script for automatic audio/video **transcription** and **speaker diarization**, using [OpenAI Whisper](https://github.com/openai/whisper) and [pyannote-audio](https://github.com/pyannote/pyannote-audio).

---

## ✨ Features
- 🎥 Automatic audio extraction from video files (via **FFmpeg**)  
- 🔄 Conversion to **16kHz mono** audio for compatibility  
- 📝 High-quality transcription with OpenAI Whisper  
- 🗣️ Speaker diarization using Pyannote 3.0  
- ⏳ Per-speaker talk time summary  
- 📊 Global analysis (duration, number of speakers, averages)  
- 📂 Output as a clean `.txt` file (timestamps + speakers)  
- 📈 Progress bar with `tqdm`  

---

## 🚀 Installation

### 1. Clone this repository
```bash
git clone https://github.com/<your-username>/transcription-diarisation.git
cd transcription-diarisation
```

---

### 2. Install FFmpeg (required)

This project relies on **FFmpeg** to extract and convert audio.  

- **Linux (Debian/Ubuntu)**  
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

- **macOS (Homebrew)**  
  ```bash
  brew install ffmpeg
  ```

- **Windows**  
  1. Download the FFmpeg build: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)  
  2. Extract it and add the `bin/` folder to your **PATH**  
  3. Test installation:  
     ```powershell
     ffmpeg -version
     ```

✅ After this, `ffmpeg` should be accessible from the command line.

---

### 3. Create a Virtual Environment (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
```
(Windows users):  
```bash
venv\Scripts\activate
```

---

### 4. Install Python dependencies
```bash
pip install -r requirements.txt
```

Dependencies include:  
- `whisper`  
- `pyannote.audio`  
- `tqdm`  

---

## 🔑 Hugging Face Access Token

This script uses the `pyannote/speaker-diarization-3.0` model, which requires explicit access.  

1. Visit: [https://huggingface.co/pyannote/speaker-diarization-3.0](https://huggingface.co/pyannote/speaker-diarization-3.0)  
2. Click on **"Agree and access"**  
3. Create a token: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)  
4. Export it in your terminal:  

```bash
export HUGGINGFACE_TOKEN="your_token_here"
```
Windows (PowerShell):  
```powershell
$env:HUGGINGFACE_TOKEN="your_token_here"
```

⚠️ Without this step, diarization will fail with a `403 Unauthorized` error.  

---

## 🛠️ Usage

Basic command:
```bash
python transcribe_diarize.py input_audio_or_video.mp4 output.txt
```

Options:
- `--whisper_model`: `tiny`, `base`, `small`, `medium`, `large`, `turbo` (default: `turbo`)  
- `--keep_temp`: keep temporary audio files  

Example:
```bash
python transcribe_diarize.py interview.mp4 transcription.txt --whisper_model medium --keep_temp
```

---

## 📜 Example Output

After processing, you’ll get a text file like this:

```
⏳ Temps de parole par speaker :
🗣️ Speaker A: 00:12:34
🗣️ Speaker B: 00:08:45

[00:00:01 - 00:00:05] 🗣️ Speaker A: Bonjour à tous !
[00:00:06 - 00:00:10] 🗣️ Speaker B: Salut, comment ça va ?
[00:00:11 - 00:00:18] 🗣️ Speaker A: Très bien, merci. On commence ?
[00:00:19 - 00:00:25] 🗣️ Speaker B: Oui, allons-y.
...
```

And a global summary in the console:

```
📊 Résumé global :
- Durée totale analysée : 00:21:19
- Nombre de speakers : 2
- Durée moyenne par speaker : 00:10:39
```

---

## 📂 Project Structure
```
transcription-diarisation/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
└── transcribe_diarize.py
```

---

## 🧩 Technologies Used
- [OpenAI Whisper](https://github.com/openai/whisper)  
- [pyannote-audio](https://github.com/pyannote/pyannote-audio)  
- [FFmpeg](https://ffmpeg.org/)  

---

## 🤝 Contributing

Contributions are welcome!  

1. Fork this repository  
2. Create a branch (`git checkout -b feature/MyFeature`)  
3. Commit your changes (`git commit -m 'Add MyFeature'`)  
4. Push to the branch (`git push origin feature/MyFeature`)  
5. Open a Pull Request  

---

## 📄 License

This project is licensed under the MIT License.  
See the [LICENSE](./LICENSE) file for more details.  

---

## 🙌 Author

Project developed by **Marc Delage**.  
