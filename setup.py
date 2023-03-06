from src import tts_wrapper, whisper_wrapper
from utils.path_handler import create_folders

# creating the necessary folders
create_folders()

# download the models
whisper = whisper_wrapper.Transcriber()
tts = tts_wrapper.TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC_ph")
