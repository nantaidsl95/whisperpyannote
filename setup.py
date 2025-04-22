from setuptools import setup, find_packages

setup(
    name="whisperpyannote",
    version="0.1.0",
    description="Script Python pour la transcription et la diarisation automatique d'audio/vidéo avec Whisper et Pyannote.",
    author="Marc Delage",
    author_email="marc.delage@imt.fr",  
    url="https://github.com/nantaidsl95/whisperpyannote",
    packages=find_packages(),
    install_requires=[
        "whisper",
        "tqdm",
        "pyannote.audio",
        "torch",
        "ffmpeg-python",
        "huggingface_hub"
    ],
    entry_points={
        "console_scripts": [
            "whisperpyannote=whisperpyannote.main:run",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio :: Speech",
        "Intended Audience :: Developers",
    ],
    python_requires=">=3.8",
)
