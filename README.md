# WhisperPyannote

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) 
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

Script Python pour transcrire et diariser automatiquement des fichiers audio ou vidéo, en utilisant [OpenAI Whisper](https://github.com/openai/whisper) et [pyannote-audio](https://github.com/pyannote/pyannote-audio).

---

## ✨ Fonctionnalités

- Extraction automatique de l'audio depuis une vidéo.
- Conversion au format 16kHz mono pour Whisper et Pyannote.
- Transcription de haute qualité avec OpenAI Whisper.
- Diarisation des locuteurs avec Pyannote 3.0.
- Résumé du temps de parole par speaker.
- Fichier texte de sortie lisible et horodaté.
- Barre de progression (`tqdm`) pour visualiser l'avancement.

---

## 🚀 Installation

Cloner ce dépôt :
```bash
git clone https://github.com/nantaidsl95/whisperpyannote.git
cd whisperpyannote
```

Installer les dépendances :
```bash
pip install -r requirements.txt
```

Prérequis :
- Python 3.8 ou supérieur
- `ffmpeg` installé sur votre système
- Un compte Hugging Face valide (pour pyannote)

---

## 🔑 Autoriser l'accès Hugging Face

Le script utilise le modèle `pyannote/speaker-diarization-3.0` hébergé sur Hugging Face, qui nécessite un accès spécifique.

Avant la première utilisation :

1. Allez sur [https://huggingface.co/pyannote/speaker-diarization-3.0](https://huggingface.co/pyannote/speaker-diarization-3.0) et cliquez sur **"Agree and access"** pour accepter les conditions d'utilisation.
2. Créez un token Hugging Face personnel ici : [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
3. Dans votre terminal, exportez votre token :

```bash
export HUGGINGFACE_TOKEN="votre_token_ici"
```

Vous êtes maintenant prêt à utiliser le script.

---

## 🛠️ Utilisation

Commande de base :
```bash
python transcribe_and_diarize.py input_audio_or_video.mp4 output.txt
```

Options disponibles :
- `--whisper_model` : choisir le modèle Whisper (`tiny`, `base`, `small`, `medium`, `large`, `turbo`) — par défaut `turbo`
- `--keep_temp` : conserver les fichiers temporaires générés

Exemple complet :
```bash
python transcribe_and_diarize.py interview.mp4 transcription.txt --whisper_model medium --keep_temp
```

---

## 📂 Architecture du projet

```
whisperpyannote/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── setup.py
├── transcribe_and_diarize.py
├── whisperpyannote/
│   ├── __init__.py
│   ├── main.py
│   ├── utils.py
│   ├── transcription.py
│   └── diarization.py
└── examples/
    └── (fichiers audio/vidéo exemples)
```

---

## 🧩 Technologies utilisées

Ce projet utilise :

- [OpenAI Whisper](https://github.com/openai/whisper) (licence MIT)
- [pyannote-audio](https://github.com/pyannote/pyannote-audio) développé par l'Université de Lorraine (licence MIT)

Merci aux équipes respectives pour leurs travaux exceptionnels !

---

## 🤝 Contribuer

Les contributions sont les bienvenues !

Merci de suivre ces étapes :
1. Forker ce dépôt.
2. Créer une branche (`git checkout -b feature/AmazingFeature`).
3. Commiter vos modifications (`git commit -m 'Add some AmazingFeature'`).
4. Pousser vers la branche (`git push origin feature/AmazingFeature`).
5. Créer une Pull Request.

---

## 📄 Licence

Ce projet est sous licence MIT.  
Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 🙌 Auteur

Projet développé par [Marc Delage](https://github.com/nantaidsl95).
