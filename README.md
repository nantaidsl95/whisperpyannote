# 🎧 whisperpyannote — Transcription & Diarisation Audio/Vidéo

**whisperpyannote** est un script Python de **transcription automatique** et de **diarisation (séparation des voix)** à partir de fichiers **audio ou vidéo**, combinant la puissance de [OpenAI Whisper](https://github.com/openai/whisper) et [Pyannote Audio 3.0](https://github.com/pyannote/pyannote-audio).

> Ce projet s’appuie sur [OpenAI Whisper](https://github.com/openai/whisper) pour la transcription et sur [Pyannote Audio](https://github.com/pyannote/pyannote-audio) pour la diarisation des locuteurs.  
> Merci aux auteurs de ces deux projets open source pour leur travail.

---

## ✨ Fonctionnalités

- 🎥 Extraction automatique de l’audio depuis les vidéos (via **FFmpeg**)  
- 🔄 Conversion en **mono 16 kHz** pour une compatibilité optimale  
- 📝 Transcription haute qualité avec **Whisper (OpenAI)**  
- 🗣️ Diarisation précise des locuteurs avec **Pyannote 3.0**  
- ⏳ Résumé du temps de parole par speaker  
- 📜 Fusion propre des segments par locuteur  
- 📊 Statistiques globales (durée totale, nombre de speakers, moyenne)  
- 📂 Export `.txt` avec horodatage + speakers  
- 📈 Suivi en temps réel via `tqdm`

---

## 🎙️ Outils recommandés pour la capture audio et vidéo

Pour enregistrer vos conversations, réunions ou appels avant transcription :

### 🟣 [OBS Studio](https://obsproject.com/)
Logiciel gratuit et open source pour **capturer la vidéo et l’audio** de votre écran, webcam ou applications.  
Il permet d’enregistrer des visioconférences, des interviews, des streams, etc.  
Les fichiers générés (`.mp4`, `.mkv`, `.mov`) sont directement compatibles avec **whisperpyannote**.

### ⚫ [BlackHole (macOS uniquement)](https://existential.audio/blackhole/)
Pilote audio virtuel gratuit pour **capturer l’audio interne du système** (sons de l’ordinateur).  
Idéal pour enregistrer le son d’une visioconférence, d’une vidéo YouTube ou d’une réunion Zoom.  
Peut être sélectionné comme source audio dans OBS pour combiner le **micro** et le **son du système**.

💡 *Avec OBS + BlackHole, vous pouvez enregistrer simultanément votre voix et le son du système, puis passer le fichier résultant à `whisperpyannote` pour transcription et diarisation.*

---

## 🚀 Installation

### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/nantaidsl95/whisperpyannote.git
cd whisperpyannote
```

### 2️⃣ Installer FFmpeg

FFmpeg est indispensable pour extraire et convertir l’audio.

**Linux (Ubuntu/Debian)**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS (Homebrew)**
```bash
brew install ffmpeg
```

**Windows**
1. Téléchargez une version sur [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)  
2. Ajoutez le dossier `bin/` à votre variable d’environnement **PATH**  
3. Vérifiez :
   ```powershell
   ffmpeg -version
   ```

✅ Vous devez pouvoir exécuter `ffmpeg` depuis le terminal avant de lancer le script.

---

### 3️⃣ Créer un environnement virtuel (recommandé)
```bash
python3 -m venv venv
source venv/bin/activate
```
*(Sous Windows)* :
```powershell
venv\Scripts\activate
```

### 4️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

**Principaux packages :**
- `whisper`  
- `pyannote.audio`  
- `tqdm`  
- `ffmpeg-python`  
- `torch`  
- `numpy`

---

## 🔑 Accès Hugging Face (obligatoire pour Pyannote)

Le modèle `pyannote/speaker-diarization-3.0` nécessite un **jeton d’accès personnel**.

1. Connectez-vous sur [https://huggingface.co/](https://huggingface.co/)  
2. Ouvrez la page du modèle :  
   👉 [https://huggingface.co/pyannote/speaker-diarization-3.0](https://huggingface.co/pyannote/speaker-diarization-3.0)  
3. Cliquez sur **“Access request”** et acceptez les conditions.  
4. Créez un token ici : [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)  
5. Exportez-le dans votre terminal :

```bash
export HUGGINGFACE_TOKEN="votre_token_ici"
```
Sous PowerShell :
```powershell
$env:HUGGINGFACE_TOKEN="votre_token_ici"
```

⚠️ Sans ce jeton, la partie **diarisation** échouera avec une erreur `403 Unauthorized`.

---

## 🛠️ Utilisation

### Commande de base :
```bash
python whisperpyannote.py input_audio_or_video.mp4 output.txt
```

### Options disponibles :

| Option | Description | Défaut |
|:--|:--|:--|
| `input_path` | Fichier audio ou vidéo à traiter | *obligatoire* |
| `output_file` | Fichier texte de sortie | *obligatoire* |
| `--whisper_model` | Modèle Whisper à utiliser : `tiny`, `base`, `small`, `medium`, `large`, `turbo` | `turbo` |
| `--keep_temp` | Conserve les fichiers audio temporaires | *désactivé* |

---

### 💡 Exemples

#### 🎙️ Transcription d’un fichier audio
```bash
python whisperpyannote.py podcast.wav transcription.txt
```

#### 🎥 Transcription d’une vidéo avec conservation de l’audio temporaire
```bash
python whisperpyannote.py interview.mp4 transcription.txt --keep_temp
```

---

## 📜 Exemple de sortie

```
⏳ Temps de parole par speaker :
🗣️ Speaker A: 00:12:34
🗣️ Speaker B: 00:08:45

[00:00:01 - 00:00:05] 🗣️ Speaker A: Bonjour à tous !
[00:00:06 - 00:00:10] 🗣️ Speaker B: Salut, comment ça va ?
[00:00:11 - 00:00:18] 🗣️ Speaker A: Très bien, merci. On commence ?
...
```

Et dans la console :
```
📊 Résumé global :
- Durée totale analysée : 00:21:19
- Nombre de speakers : 2
- Durée moyenne par speaker : 00:10:39
```

---

## 🧰 Dépannage

| Problème | Solution |
|:--|:--|
| `ffmpeg not found` | Installez FFmpeg et ajoutez-le au PATH |
| `403 Unauthorized` (Pyannote) | Votre token n’a pas accès au modèle — demandez l’accès sur Hugging Face |
| Transcription lente | Essayez un modèle plus petit : `--whisper_model small` |
| Pas de GPU détecté | Whisper utilisera automatiquement le CPU |

---

## 📁 Structure du projet

```
whisperpyannote/
├── whisperpyannote.py
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

---

## 🧩 Technologies utilisées

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Pyannote Audio 3.0](https://github.com/pyannote/pyannote-audio)
- [FFmpeg](https://ffmpeg.org/)
- [tqdm](https://github.com/tqdm/tqdm)
- [OBS Studio](https://obsproject.com/)
- [BlackHole (macOS)](https://existential.audio/blackhole/)

---

## 📄 Licence

Projet sous licence **MIT** — voir [LICENSE](./LICENSE).

---

## 👤 Auteur

Projet développé par **Marc Delage**  
GitHub → [nantaidsl95](https://github.com/nantaidsl95)
