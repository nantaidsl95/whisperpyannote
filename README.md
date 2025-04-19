# WhisperPyannote

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) 
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

Script Python pour transcrire et diariser automatiquement des fichiers audio ou vidéo, en utilisant [OpenAI Whisper](https://github.com/openai/whisper) et [pyannote-audio](https://github.com/pyannote/pyannote-audio).

## Fonctionnalités

- Extraction automatique de l'audio depuis une vidéo.
- Conversion au format 16kHz mono pour Whisper et Pyannote.
- Transcription de haute qualité avec OpenAI Whisper.
- Diarisation des locuteurs avec Pyannote 3.0.
- Résumé du temps de parole par speaker.
- Fichier texte de sortie lisible et horodaté.
- Barre de progression (`tqdm`) pour visualiser l'avancement.

## Installation

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
- Un token HuggingFace valide pour la diarisation (`HUGGINGFACE_TOKEN`)

## Utilisation

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

## Token HuggingFace

Le script utilise `pyannote/speaker-diarization-3.0` qui nécessite une authentification.

Créer un token sur [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) et définir dans votre terminal :

```bash
export HUGGINGFACE_TOKEN="votre_token_ici"
```

## Architecture du projet

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
│   ├── utils.py
│   ├── transcription.py
│   ├── diarization.py
│   └── main.py
└── examples/
    └── (fichiers audio/vidéo exemples)
```

## Contribuer

Les contributions sont les bienvenues ! 

Merci de :
- Forker ce dépôt,
- Créer une branche (`git checkout -b feature/AmazingFeature`),
- Commiter vos modifications (`git commit -m 'Add some AmazingFeature'`),
- Pousser vers la branche (`git push origin feature/AmazingFeature`),
- Créer une Pull Request.

  
## Technologies utilisées

Ce projet utilise :

- [OpenAI Whisper](https://github.com/openai/whisper) (licence MIT)
- [pyannote-audio](https://github.com/pyannote/pyannote-audio) développé par l'Université de Lorraine (licence MIT)

Merci aux équipes respectives pour leurs travaux exceptionnels !

## Licence

Ce projet est sous licence MIT.  
Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## Auteur

Projet développé par [Marc Delage](https://github.com/nantaidsl95).
