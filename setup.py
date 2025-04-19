from setuptools import setup, find_packages

setup(
    name="whisperpyannote",
    version="0.1.0",
    description="Script de transcription et de diarisation audio/vidéo avec Whisper et Pyannote.",
    author="Marc Delage",
    author_email="ton@email.com",
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
    ],
    python_requires='>=3.8',
)
