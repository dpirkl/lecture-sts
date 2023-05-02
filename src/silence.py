import logging
import os

import pydub.silence
from joblib import dump
from pydub import AudioSegment

from utils.file_handler import get_audio_length
from utils.path_handler import VARIABLE_DIRECTORY


class Silence:
    """This class can be used to enhance the output of `whisper` by adding silence segments.
    It was created to ensure better timing for `TTS`."""

    @classmethod
    def get_silence_segments_pydub(
            cls, audio_file: str, silence_duration: float, silence_threshold: float = -50
    ) -> list:
        """This method uses pydub to detect silence in an audio file.

        Args:
            audio_file (str): The path to the audio file.
            silence_duration (float): The minimum duration of silence in seconds.
            silence_threshold (float, optional): The upper bound for how quiet is silent in dFBS. Defaults to -50.
                                                 See also `pydub.silence.detect_silence`.

        Returns:
            list: A list of dicts with the start and end of the silence in seconds.
        """
        audio = AudioSegment.from_file(audio_file)
        silences = pydub.silence.detect_silence(
            audio, int(silence_duration * 1000), silence_threshold
        )

        result = []
        for element in silences:
            result.append({"start": element[0] / 1000, "end": element[1] / 1000})

        return result

    @classmethod
    def add_silence_segments_whisper(
            cls, segments: list, max_duration: int = None
    ) -> list:
        """This method adds silence segments to a list of segments. It compares the start and end of the segments and
        adds silence if there is a difference. If a silence is added the key `text` is set to `__silence__`, since it
        cannot occur naturally in the text.

        Args:
            segments (list): A list of dicts with the start and end of the segments in seconds.
                             The format is the same as the output of `whisper`.
            max_duration (int): The maximum duration of a resulting segment. Defaults to None.

        Returns:
            list: A list of dicts with the start and end of the segments in seconds,
                  the content of the segment and the duration of the segment.
        """

        logging.info("Preparing the results of whisper for TTS.")

        substrings = []

        current_duration = 0

        for i, segment in enumerate(segments):
            if i == 0:
                substrings.append(
                    {
                        "text": segment["text"],
                        "start": round(segment["start"], 2),
                        "end": round(segment["end"], 2),
                    }
                )
                duration = abs(round((segment["end"] - segment["start"]), 2))
                current_duration += duration
                continue

            difference = abs(round((segment["start"] - segments[i - 1]["end"]), 2))
            if segment["start"] != segments[i - 1]["end"] and difference > 0.1:
                substrings.append(
                    {
                        "text": "__silence__",
                        "start": round(segments[i - 1]["end"], 2),
                        "end": round(segment["start"], 2),
                        "duration": difference,
                    }
                )
                substrings.append(
                    {
                        "text": segment["text"],
                        "start": round(segment["start"], 2),
                        "end": round(segment["end"], 2),
                    }
                )

                current_duration = 0

            else:
                duration = abs(round((segment["end"] - segment["start"]), 2))
                current_duration += duration

                if max_duration and (max_duration < current_duration):
                    substrings.append(
                        {
                            "text": segment["text"],
                            "start": segment["start"],
                            "end": segment["end"],
                        }
                    )
                    current_duration = 0

                else:
                    substrings[-1]["text"] += segment["text"]
                    substrings[-1]["end"] = round(segment["end"], 2)

        for segment in substrings:
            segment["duration"] = round((segment["end"] - segment["start"]), 2)

        logging.info("Preparation finished.")

        return substrings

    @classmethod
    def add_silence_segments_pydub_whisper(
            cls,
            segments: list,
            audio_file: str,
            silence_duration: float = 1,
            silence_threshold: float = -50,
            max_duration: int = 30,
    ):
        """This method adds silence segments to the result of whisper transcription.
        It uses the information of both the whisper result and pydub.

        Args:
            segments (list): The result provided by whisper.
            audio_file (str): The path to the audio file used for the transcription.
            silence_duration (float, optional): The minimum length of silence for pydub. Defaults to 1.
            silence_threshold (float, optional): The silence threshold (`get_silence_segments_pydub`). Defaults to -50.
            max_duration (int, optional): The maximum duration of text segments. Defaults to 30.

        Raises:
            RuntimeError: If there is a mistake and the start time of a segment is equal to or after the end time.

        Returns:
            list: The list with added silence segments.
        """
        logging.info(
            f"{os.path.basename(audio_file).split('.')[0]}: Preparing the results of whisper for TTS."
        )

        result = []

        pydub_silences = cls.get_silence_segments_pydub(
            audio_file=audio_file,
            silence_duration=silence_duration,
            silence_threshold=silence_threshold,
        )

        for i, segment in enumerate(segments):
            pydub_segments = cls._get_pydub_segments_for_whisper_segment(
                round(segment["start"], 2), round(segment["end"], 2), pydub_silences
            )

            if i == 0:
                cls._add_text(
                    pydub_segments,
                    result,
                    index=i,
                    segments=segments,
                    max_duration=max_duration,
                )
                continue

            else:
                difference = round(abs((segment["start"] - segments[i - 1]["end"])), 2)
                if segment["text"] == "...":
                    result.append(
                        {
                            "start": round(segments[i-1]["end"], 2),
                            "end": round(segment["end"], 2),
                            "text": "__silence__",
                        }
                    )

                elif difference > 0.1:
                    result.append(
                        {
                            "start": round(segments[i - 1]["end"], 2),
                            "end": round(segment["start"], 2),
                            "text": "__silence__",
                        }
                    )

                    result.append(
                        {
                            "start": round(segment["start"], 2),
                            "end": round(segment["end"], 2),
                            "duration": round((segment["end"] - segment["start"]), 2),
                            "text": segment["text"],
                        }
                    )

                else:
                    cls._add_text(
                        pydub_segments,
                        result,
                        index=i,
                        segments=segments,
                        max_duration=max_duration,
                    )

        i = 0
        while i < len(result):
            segment = result[i]
            duration = round((segment["end"] - segment["start"]), 2)
            if duration <= 0:
                raise RuntimeError(f"Duration of segment is lower than or equal to zero.")

            segment["duration"] = duration
            if segment["text"] == "__silence__" and len(result) > i + 1 and result[i + 1]["text"] == "__silence__":
                segment["end"] = result[i + 1]["end"]
                segment["duration"] = round(abs(segment["end"]-segment["start"]), 2)
                result.pop(i + 1)
            else:
                i += 1

        name = os.path.basename(audio_file).split(".")[0]
        dump(result, str(VARIABLE_DIRECTORY / f"{name}_en_segments.joblib"))

        logging.info(f"{name}: Results prepared.")

        return result

    @classmethod
    def _add_text(
            cls,
            pydub_segments: list,
            result: list,
            index: int,
            segments: list,
            max_duration: int,
    ) -> None:
        """Not intended for external use.
        This method is used by `add_silence_segments_pydub_whisper` to add text segments, including the pydub silence.

        Args:
            pydub_segments (list): The segments generated by `get_silence_segments_pydub`.
            result (list): The resulting list to append the text to.
            index (int): The current index in segments.
            segments (list): The segments containing the text information.
            max_duration (int): The maximum duration of resulting text segments.
        """
        segment = segments[index]

        segment_start = segment["start"]
        segment_end = segment["end"]
        segment_duration = segment_end - segment_start

        total_pydub_duration = 0

        pydub_duration = 0
        if len(pydub_segments) != 0:
            for pydub_segment in pydub_segments:
                if pydub_segment["position"] == "start":
                    pydub_duration += round(
                        (pydub_segment["end"] - pydub_segment["start"]), 2
                    )

                    pydub_segments.remove(pydub_segment)

        total_pydub_duration += pydub_duration

        if pydub_duration > 0:
            if total_pydub_duration > segment_duration:
                start = segment_start
            elif index == 0:
                start = 0
            else:
                start = round(result[-1]["end"], 2)

            result.append(
                {
                    "start": round(start, 2),
                    "end": round(start + pydub_duration, 2),
                    "text": "__silence__",
                }
            )

        if ((index == 0) or (result[-1]["text"] == "__silence__")) or (
                (result[-1]["text"] != "__silence__")
                and (result[-1]["duration"] > max_duration)
        ):
            result.append(
                {
                    "start": round((segment["start"] + pydub_duration), 2),
                    "end": round(segment["end"], 2),
                    "duration": round((segment["end"] - segment["start"]), 2),
                    "text": segment["text"],
                }
            )
        else:
            result[-1]["text"] += segment["text"]
            result[-1]["end"] = round(segment["end"], 2)
            result[-1]["duration"] = round((result[-1]["end"] - result[-1]["start"]), 2)

        pydub_duration = 0

        if len(pydub_segments) != 0:
            for pydub_segment in pydub_segments:
                if pydub_segment["position"] == "end":
                    # add silence to results

                    pydub_duration += round(
                        (pydub_segment["end"] - pydub_segment["start"]), 2
                    )

        total_pydub_duration += pydub_duration

        if pydub_duration > 0:
            if not (total_pydub_duration > segment_duration):
                end = round(result[-1]["end"], 2)
                result[-1]["end"] = round((end - pydub_duration), 2)

                result.append(
                    {
                        "start": round(result[-1]["end"], 2),
                        "end": round(end, 2),
                        "text": "__silence__",
                    }
                )

    @classmethod
    def _get_pydub_segments_for_whisper_segment(
            cls, start: float, end: float, pydub_silence: list
    ) -> list:
        """This method returns silences starting between start and end.

        Args:
            start (float): The start time in seconds.
            end (float): The end time in seconds.
            pydub_silence (list): A list of dictionaries containing start and end.

        Returns:
            list: Returns all fitting silences.
        """

        pydub_segments = []

        for silence in pydub_silence:
            if silence["start"] < start:
                pydub_silence.remove(silence)
                continue

            if silence["start"] > end:
                break

            if end < silence["end"]:
                silence["position"] = "end"
            else:
                middle = round((silence["start"] + silence["end"]) / 2, 2)
                silence["position"] = (
                    "start"
                    if abs(middle - silence["start"]) < abs(middle - silence["end"])
                    else "end"
                )

            pydub_segments.append(silence)

        return pydub_segments
