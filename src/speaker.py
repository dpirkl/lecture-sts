import logging
import os
from abc import ABC, abstractmethod

from pydub import AudioSegment

from src.tts_wrapper import speak
from utils import file_handler
from utils.path_handler import (
    AUDIO_DEST_DIRECTORY,
    AUDIO_TRANSLATED_SPEED_DIRECTORY,
    VIDEO_DIRECTORY,
)


class SpeakerInterface(ABC):
    @abstractmethod
    def speak(self, use_gpu: bool):
        pass


class SegmentsSpeaker(SpeakerInterface):
    def __init__(self, lecture_name: str, segments: list):
        """Creates a SegmentsSpeaker instance. The segments should look like the result of the methods in silence.py.

        Args:
            lecture_name (str): The name of the lecture.
            segments (list): The segments used to speak the result.
        """
        self.lecture_name = lecture_name
        self.segments = segments

    def speak(self, use_gpu: bool = True):
        """This performs tts for all segments.

        Args:
            use_gpu (bool, optional): Determines whether the gpu (cuda) should be used. Defaults to True.
        """
        logging.info(f"{self.lecture_name}: Synthesizing and adjusting audio.")

        if (AUDIO_DEST_DIRECTORY / f"{self.lecture_name}.wav").exists():
            os.remove(AUDIO_DEST_DIRECTORY / f"{self.lecture_name}.wav")

        for segment in self.segments:
            if segment["text"] == "__silence__":
                self._add_silence(segment=segment)

            else:
                self._add_text(segment=segment, use_gpu=use_gpu)

        file_handler.adjust_audio_length_to_video(
            audio_file=str(AUDIO_DEST_DIRECTORY / f"{self.lecture_name}.wav"),
            video_file=str(VIDEO_DIRECTORY / f"{self.lecture_name}.mp4"),
            output_path=str(
                AUDIO_TRANSLATED_SPEED_DIRECTORY / f"{self.lecture_name}.wav"
            ),
        )

        logging.info(f"{self.lecture_name}: Synthesizing and adjusting finished.")

    def _add_silence(self, segment: dict):
        """Not intended for external use. Adds silence to the translated audio.

        Args:
            segment (dict): A dict containing the start, end and duration of the silence.
        """

        duration = segment["duration"]

        if not (AUDIO_DEST_DIRECTORY / f"{self.lecture_name}.wav").exists():
            new_audio = AudioSegment.silent(duration=duration * 1000)
        else:
            audio = AudioSegment.from_file(
                AUDIO_DEST_DIRECTORY / f"{self.lecture_name}.wav"
            )
            pause = AudioSegment.silent(duration=duration * 1000)

            new_audio = audio.append(pause, crossfade=0)

        new_audio.export(
            AUDIO_DEST_DIRECTORY / f"{self.lecture_name}.wav", format="wav"
        )

        length = file_handler.get_audio_length(
            str(AUDIO_DEST_DIRECTORY / f"{self.lecture_name}.wav")
        )

        end = float(segment["end"])

        if abs(end - length) > 0.1:
            logging.warning(
                f"{self.lecture_name}: Audio length is not correct. Should be {end}, but is {length}. Differs by {end - length}."
            )

    def _add_text(self, segment: dict, use_gpu: bool):
        """Not intended for external use. This method performs tts and appends it to the translated audio file.

        Args:
            segment (dict): A dict containing the start, duration, end and text for TTS.
            use_gpu (bool): Determines whether to use the gpu (cuda).
        """

        if not (AUDIO_DEST_DIRECTORY / f"{self.lecture_name}.wav").exists():
            speak(
                model_name="tts_models/en/ljspeech/tacotron2-DDC_ph",
                text=segment["text"],
                output_path=str(AUDIO_DEST_DIRECTORY / f"{self.lecture_name}.wav"),
                gpu=use_gpu,
            )
            file_handler.adjust_audio_length(
                audio_file=str(AUDIO_DEST_DIRECTORY / f"{self.lecture_name}.wav"),
                length=segment["duration"],
            )

        else:
            speak(
                model_name="tts_models/en/ljspeech/tacotron2-DDC_ph",
                text=segment["text"],
                output_path=str(AUDIO_DEST_DIRECTORY / f"{self.lecture_name}_tmp.wav"),
                gpu=use_gpu,
            )

            file_handler.adjust_audio_length(
                audio_file=str(AUDIO_DEST_DIRECTORY / f"{self.lecture_name}_tmp.wav"),
                length=segment["duration"],
            )

            audio = AudioSegment.from_file(
                file=str(AUDIO_DEST_DIRECTORY / f"{self.lecture_name}.wav")
            )
            audio_tmp = AudioSegment.from_file(
                file=str(AUDIO_DEST_DIRECTORY / f"{self.lecture_name}_tmp.wav")
            )

            new_audio = audio.append(audio_tmp, crossfade=0)

            AudioSegment.export(
                new_audio,
                str(AUDIO_DEST_DIRECTORY / f"{self.lecture_name}.wav"),
                format="wav",
            )

            os.remove(AUDIO_DEST_DIRECTORY / f"{self.lecture_name}_tmp.wav")

            length = file_handler.get_audio_length(
                str(AUDIO_DEST_DIRECTORY / f"{self.lecture_name}.wav")
            )

            end = float(segment["end"])

            if abs(end - length) > 0.1:
                logging.warning(
                    f"{self.lecture_name}: Audio length is not correct. Should be {end}, but is {length}. Differs by {end - length}."
                )
