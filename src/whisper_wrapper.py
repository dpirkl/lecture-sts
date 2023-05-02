import logging
import os

import whisper
from joblib import dump, load

from utils.file_handler import get_audio_length
from utils.path_handler import VARIABLE_DIRECTORY


class Transcriber:
    """This class is a simple wrapper for the whisper library"""

    def __init__(self, model: str = "large", fp16_settings: bool = False):
        """Initializes a Transcriber object. You can set the model size and specify the fp16 settings.


        Args:
            model (str, optional): The size of the transcription model. Defaults to "small".
            fp16_settings (bool, optional): Whether to use fp16 (or fp32). Defaults to False.
        """

        self.model = whisper.load_model(name=model)
        self.fp16_settings = fp16_settings

    def transcribe(self, audio_file: str, no_cache=False) -> dict:
        """This method transcribes a given audio file.

        Args:
            audio_file (str): The path to the audio file.
            no_cache (bool): If false, it loads previous transcriptions. Defaults to False.

        Returns:
            dict: The result of the transcription. The plain text can be accessed by 'result["text"]'.
        """
        name = os.path.basename(audio_file).split(".")[0]
        if (VARIABLE_DIRECTORY / f"{name}_original.joblib").exists() and not no_cache:
            logging.info(f"{name}: Loading variable with joblib.")
            result = load(VARIABLE_DIRECTORY / f"{name}_original.joblib")
        else:
            logging.info(
                f"{os.path.basename(audio_file).split('.')[0]}: Transcribing audio."
            )
            result = self.model.transcribe(audio_file, fp16=self.fp16_settings)
            dump(result, VARIABLE_DIRECTORY / f"{name}_original.joblib")
            logging.info(
                f"{os.path.basename(audio_file).split('.')[0]}: Transcription finished."
            )

        result["segments"] = self._adjust_end_time_whisper(
            result["segments"], audio_file=audio_file
        )

        return result

    def transcribe_and_translate(self, audio_file: str, no_cache=False) -> dict:
        """This method transcribes the audio file and translates the transcription to english.

        Args:
            audio_file (str): The path to the audio file.
            no_cache (bool): If false, it loads previous transcriptions. Defaults to False.

        Returns:
            dict: The result of the transcription. The plain text can be accessed by 'result["text"]'.
        """
        name = os.path.basename(audio_file).split(".")[0]
        if (VARIABLE_DIRECTORY / f"{name}_en.joblib").exists() and not no_cache:
            logging.info(f"{name}: Loading variable with joblib.")
            result = load(VARIABLE_DIRECTORY / f"{name}_en.joblib")
        else:
            logging.info(f"{name}: Transcribing and translating the audio file.")
            options = {"task": "translate", "suppress_blank": False}
            result = self.model.transcribe(
                audio_file, fp16=self.fp16_settings, **options
            )
            dump(result, VARIABLE_DIRECTORY / f"{name}_en.joblib")
            logging.info(f"{name}: Transcription and translation finished.")

        result["segments"] = Transcriber._adjust_end_time_whisper(
            result["segments"], audio_file=audio_file
        )

        return result

    @classmethod
    def write_vtt(cls, result, output_dir):
        """This method generates a vtt subtitle file.

        Args:
            result (dict): The "segments" key of the dict result returned by whisper.
            output_dir (str): The path to the subtitle file ending in '.vtt'.
        """
        logging.info(
            f"{os.path.basename(output_dir).split('.')[0]}: Generating vtt subtitles."
        )
        with open(str(output_dir), "w") as f:
            print("WEBVTT\n", file=f)
            for segment in result["segments"]:
                print(
                    f"{cls._format_timestamp(segment['start'])} --> {cls._format_timestamp(segment['end'])}\n"
                    f"{segment['text'].strip().replace('-->', '->')}\n",
                    file=f,
                    flush=True,
                )
        logging.info(
            f"{os.path.basename(output_dir).split('.')[0]}: Subtitles generated."
        )

    @classmethod
    def write_srt(cls, result: dict, output_dir: str):
        """This method generates a srt subtitle file.

        Args:
            result (dict): The "segments" key of the dict result returned by whisper.
            output_dir (str): The path to the subtitle file ending in '.srt'.
        """
        logging.info(
            f"{os.path.basename(output_dir).split('.')[0]}: Generating srt subtitles."
        )
        with open(str(output_dir), "w") as f:
            for i, segment in enumerate(result["segments"], start=1):
                print(
                    f"{i}\n"
                    f"{cls._format_timestamp(segment['start'], always_include_hours=True, decimal_marker=',')} --> "
                    f"{cls._format_timestamp(segment['end'], always_include_hours=True, decimal_marker=',')}\n"
                    f"{segment['text'].strip().replace('-->', '->')}\n",
                    file=f,
                    flush=True,
                )
        logging.info(
            f"{os.path.basename(output_dir).split('.')[0]}: Subtitles generated."
        )

    @classmethod
    def write_txt(cls, result: dict, output_dir: str):
        """This method generates a txt file with the transcription.

        Args:
            result (dict): The "segments" key of the dict result returned by whisper.
            output_dir (str): The path to the txt file.
        """
        logging.info(
            f"{os.path.basename(output_dir).split('.')[0]}: Generating txt file."
        )
        with open(str(output_dir), "w") as f:
            for segment in result["segments"]:
                print(
                    segment['text'].strip(),
                    file=f,
                    flush=True,
                )
        logging.info(
            f"{os.path.basename(output_dir).split('.')[0]}: Txt file generated."
        )

    @classmethod
    def _format_timestamp(
        cls,
        seconds: float,
        always_include_hours: bool = False,
        decimal_marker: str = ".",
    ):
        """This method is not intended for external use. It formats time stamps for the subtitles."""
        assert seconds >= 0, "non-negative timestamp expected"
        milliseconds = round(seconds * 1000.0)

        hours = milliseconds // 3_600_000
        milliseconds -= hours * 3_600_000

        minutes = milliseconds // 60_000
        milliseconds -= minutes * 60_000

        seconds = milliseconds // 1_000
        milliseconds -= seconds * 1_000

        hours_marker = f"{hours:02d}:" if always_include_hours or hours > 0 else ""
        return f"{hours_marker}{minutes:02d}:{seconds:02d}{decimal_marker}{milliseconds:03d}"

    @classmethod
    def _adjust_end_time_whisper(cls, segments: list, audio_file: str) -> list:
        """This method adjusts the final segment of the transcription. The end time of the last segment is greater than
        the length of the audio file. This caused problems for later use. To ensure all future methods work with the
        same transcription, this method is call right after the transcription.

        Args:
            segments (list): The segments from the whisper result. (Key "segments").
            audio_file (str): The path to the audio file to adjust the end time to.

        Returns:
            list: Returns the segments with the modified last entry.
        """
        audio_file_length = get_audio_length(audio_file=audio_file)
        last_segment = segments[-1]
        if last_segment["start"] < audio_file_length:
            last_segment["end"] = audio_file_length

        # There should not be any segments with start > end. Last segments do not tend to be longer than 10 seconds.
        else:
            last_segment["end"] = last_segment["start"] + 10
        segments[-1] = last_segment

        return segments
