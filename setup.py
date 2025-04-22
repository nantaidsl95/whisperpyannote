from setuptools import setup, find_packages

setup(
    name="whisperpyannote",
    version="0.1.0",
    description="Python script for automatic audio/video transcription and speaker diarization with Whisper and Pyannote.",
    author="Marc Delage",
    author_email="your.email@example.com",  # <-- Update with your real email
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
