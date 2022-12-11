"""This module contains a simple wrapper around the TTS library."""
from pathlib import Path

import TTS
from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer


class Speaker:
    """An instance of this object can generate audio from text using the TTS library."""

    def __init__(self, model_name="tts_models/en/ljspeech/tacotron2-DDC"):

        path = Path(TTS.__file__).parent / ".models.json"
        manager = ModelManager(path)

        model_path, config_path, model_item = manager.download_model(model_name)

        vocoder_name = model_item["default_vocoder"]

        vocoder_path, vocoder_config_path, _ = manager.download_model(vocoder_name)

        self.synthesizer = Synthesizer(
            tts_checkpoint=model_path,
            tts_config_path=config_path,
            tts_speakers_file=None,
            tts_languages_file=None,
            vocoder_checkpoint=vocoder_path,
            vocoder_config=vocoder_config_path,
            encoder_checkpoint=None,
            encoder_config=None,
        )

    def speak(self, text: str, output_path: str):
        """This method performs the actual text-to-speech conversion.

        Args:
            text (str): The text to be converted to speech.
            output_path (str): The path to the output file.
        """
        wav = self.synthesizer.tts(text)
        self.synthesizer.save_wav(wav, output_path)
