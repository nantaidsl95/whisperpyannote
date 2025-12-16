# 🖥️ WhisperPyannote GUI

WhisperPyannote includes a **desktop graphical user interface (GUI)** built with **PySide6**, allowing you to run transcription and speaker diarization without using the command line.

The GUI acts as a **thin wrapper around the existing CLI script** (`whisperpyannote.py`).  
No transcription or diarization logic is duplicated, ensuring full compatibility with future CLI updates.

---

## ✨ Features

- 📂 Audio / video file selection (or drag & drop)
- 📝 Processing modes:
  - Transcription + diarization
  - Transcription only
  - Diarization only
- 🧠 Whisper model selection
- 🌍 Language selection (auto-detect or forced)
- 🔑 Hugging Face token management
- 📄 Output formats:
  - TXT (always generated)
  - JSON
  - SRT
  - VTT
- 🗣️ Option to generate subtitles without speaker labels
- 🪵 Real-time console output (CLI logs)
- ⏹️ Start / stop processing
- 💾 Automatic persistence of user preferences

---

## ▶️ Launching the GUI

Activate your virtual environment and run:

```bash
python whisperpyannote_gui.py
```

> **Important:**  
> The file `whisperpyannote.py` must be located in the **same directory** as `whisperpyannote_gui.py`.

---

## 📦 Requirements

### Python dependencies

In addition to the CLI dependencies, the GUI requires **PySide6**:

```bash
pip install -r requirements-gui.txt
```

---

## 🔐 Hugging Face Token

Speaker diarization requires a Hugging Face access token.

The token can be provided in one of the following ways:
- via the `HF_TOKEN` environment variable (**recommended**)
- via the **HF token** input field in the GUI

Token handling and behavior are strictly identical to the CLI version.

---

## 📝 Notes

- The GUI automatically detects which CLI options are supported by the installed script version
- JSON / SRT / VTT files are generated **in addition to** the main `.txt` output
- User settings (model, language, export options, token, etc.) are saved between sessions

---

## 📄 License

This GUI is distributed under the same **MIT License** as the main WhisperPyannote project.
