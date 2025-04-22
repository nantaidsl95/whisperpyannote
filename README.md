# WhisperPyannote

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) 
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

Python script for automatic audio/video transcription and speaker diarization, using [OpenAI Whisper](https://github.com/openai/whisper) and [pyannote-audio](https://github.com/pyannote/pyannote-audio).

---

## ✨ Features

- Automatic audio extraction from video files.
- Conversion to 16kHz mono audio for Whisper and Pyannote compatibility.
- High-quality transcription using OpenAI Whisper.
- Speaker diarization using Pyannote 3.0.
- Speaker talk time summary.
- Multiple output styles (`simple`, `markdown`, `per_speaker`).
- Text files ready for Word, Docs, or Excel.
- Progress bar (`tqdm`) for real-time feedback.

---

## 🚀 Installation

Clone this repository:
```bash
git clone https://github.com/nantaidsl95/whisperpyannote.git
cd whisperpyannote
```

---

## 🧪 Create a Virtual Environment (Recommended)

To avoid system conflicts, it is **recommended to use a virtual environment**.

Create and activate a `venv`:

```bash
python3 -m venv venv
source venv/bin/activate
```

(Windows users:
```bash
venv\Scripts\activate
```
)

✅ Now you are inside an isolated Python environment!

---

## 📦 Install dependencies

After activating your virtual environment, install the required packages:

```bash
pip install -r requirements.txt
```

⚡ Using a virtual environment solves issues like "externally-managed-environment" errors on macOS and Linux.

---

## 🔑 Grant Access to Hugging Face Model

The script uses the `pyannote/speaker-diarization-3.0` model hosted on Hugging Face, which requires explicit access authorization.

**Before running the script, you must:**

1. Visit the model page: [https://huggingface.co/pyannote/speaker-diarization-3.0](https://huggingface.co/pyannote/speaker-diarization-3.0)
2. Click on **"Agree and access"** to accept the model's usage conditions.
3. Create a personal access token: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
4. Export your token as an environment variable in your terminal:

```bash
export HUGGINGFACE_TOKEN="your_token_here"
```

✅ After these steps, you will be able to use the diarization functionality without errors.

⚠️ **Important**: if you do not agree to the model's conditions and configure your token, you will encounter a `403 Unauthorized` error.

---

## 🛠️ Usage

Basic command:
```bash
whisperpyannote input_audio_or_video.mp4 output.txt
```

Available options:
- `--whisper_model`: choose Whisper model (`tiny`, `base`, `small`, `medium`, `large`, `turbo`) — default is `turbo`
- `--language`: force language detection (`fr`, `en`, `es`, etc.) — optional
- `--output_style`: select the output style (`simple`, `markdown`, `per_speaker`) — default is `markdown`
- `--keep_temp`: keep temporary audio files

Full example:
```bash
whisperpyannote interview.mp4 transcription.txt --whisper_model medium --language fr --output_style per_speaker
```

---

## 🖋️ Available Output Styles (`--output_style`)

| Style | Description | Use case |
|:--|:--|:--|
| `simple` | Raw text per segment with timestamps | Quick reading |
| `markdown` | Structured text with speaker titles and bold timestamps | Ideal for Word/Docs |
| `per_speaker` | All text grouped by speaker | Speaker-based analysis |

---

## 📂 Project Structure

```
whisperpyannote/
├── README.md
├── LICENSE
├── requirements.txt
├── setup.py
├── transcribe_and_diarize.py
├── whisperpyannote/
│   ├── __init__.py
│   ├── main.py
│   ├── utils.py
│   ├── transcription.py
│   ├── diarization.py
│   └── output_formatter.py
└── examples/
    └── (sample audio/video files)
```

---

## 🧩 Technologies Used

This project leverages:

- [OpenAI Whisper](https://github.com/openai/whisper) (MIT License)
- [pyannote-audio](https://github.com/pyannote/pyannote-audio) developed by Université de Lorraine (MIT License)

Thanks to the respective teams for their outstanding work!

---

## 🤝 Contributing

Contributions are welcome!

Please follow these steps:
1. Fork this repository.
2. Create a branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for more details.

---

## 🙌 Author

Project developed by [Marc Delage](https://github.com/nantaidsl95).
