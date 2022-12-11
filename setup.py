import whisper

from src import tts_wrapper
from utils import path_handler

# Create folders
path_handler.create_folders()

# Download TTS models
tts_wrapper.download_models()

# Download Whisper models
whisper.load_model("large")
