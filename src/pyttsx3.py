import os

import pyttsx3
from speaker import Speaker
from utils import AUDIO_DEST_DIRECTORY


class PYTTSX3Speaker(Speaker):
    """Uses pyttsx3 for text to speech conversion for the given text."""

    engine: pyttsx3.Engine

    def __init__(self):
        self.engine = pyttsx3.init()

    def save_to_file(self, text: str, filename: str, audio_format: str = "mp3") -> None:
        """Uses pyttsx3 for text to speech conversion for the given text and saves it to an audio file.

        Args:
            text (str): The text used for the conversion.
            filename (str): The name of the generated audio file.
            audio_format (str, optional): The format of the generated audio file. Defaults to "mp3".
        """

        self.engine.save_to_file(text, os.path.join(AUDIO_DEST_DIRECTORY, filename, '.', audio_format))

        self.engine.runAndWait()

        return
