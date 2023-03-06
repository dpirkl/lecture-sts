"""This module contains a simple wrapper around the TTS library."""
import io
import logging
import os
from contextlib import redirect_stdout

from TTS.api import TTS


def speak(model_name, text, output_path, gpu: bool = True):
    """This function performs tts using the TTS api.

    Args:
        model_name (str): The path to the model to load.
        text (str): The text to be converted to speech.
        output_path (str): The path of the created audio file.
        gpu (bool): Whether to use the gpu (cuda) or not.
    """
    logging.debug(f"{os.path.basename(output_path).split('.')[0]}: Performing TTS.")
    f = io.StringIO()
    with redirect_stdout(f):
        tts = TTS(model_name=model_name, progress_bar=True, gpu=gpu)
        tts.tts_to_file(text=text, file_path=str(output_path))
    logging.debug(f.getvalue())
    logging.debug(f"{os.path.basename(output_path).split('.')[0]}: TTS finished.")
