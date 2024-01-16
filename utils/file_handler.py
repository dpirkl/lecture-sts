"""This module contains functions for handling files.
This includes:
- splitting a video into audio and video files
- merging audio and video files
- deleting files
- merging video and subtitles
- adjusting the speed of an audio file
"""
import logging
import os
import subprocess
import wave

import librosa
import soundfile as sf
from moviepy.editor import *
from moviepy.video.io.VideoFileClip import VideoFileClip

from utils.path_handler import (
    AUDIO_DIRECTORY,
    VIDEO_DEST_DIRECTORY,
    VIDEO_DIRECTORY,
    VIDEO_SUBTITLES_DIRECTORY,
)


def get_audio_from_video_file(video_file: str, output_path: str = None) -> None:
    """Extracts the audio from the given video file and saves it to the audio directory."""
    audio_path = (
        str(output_path)
        if output_path
        else str(
            AUDIO_DIRECTORY / str(os.path.basename(video_file).split(".")[0] + ".wav")
        )
    )

    command = f"ffmpeg -y -i {video_file} -ab 160k -ac 2 -ar 44100 -vn {audio_path} -hide_banner -loglevel error"
    subprocess.call(command, shell=True)


def remove_audio_from_video_file(video_file: str, output_path: str = None) -> None:
    """Removes the audio from the given video file and saves it to the video destination directory."""
    output_path = (
        str(output_path)
        if output_path
        else str(
            VIDEO_DIRECTORY / str(os.path.basename(video_file).split(".")[0] + ".mp4")
        )
    )

    command = f"ffmpeg -y -i {str(video_file)} -vcodec copy -an {output_path} -hide_banner -loglevel error"
    subprocess.call(command, shell=True)


def split_video(
    video_file: str,
    video_output_path: str = None,
    audio_output_path: str = None,
) -> None:
    """Splits the given video file into an audio file and a video file without audio."""
    logging.info(
        f"{os.path.basename(video_file).split('.')[0]}: Splitting video into audio and video file."
    )
    get_audio_from_video_file(video_file=video_file, output_path=audio_output_path)
    remove_audio_from_video_file(video_file=video_file, output_path=video_output_path)


def merge_audio_and_video_to_mp4(
    video_file: str,
    audio_file: str,
    output_path: str = None,
) -> None:
    """Merges the audio and video file and saves it."""
    output_path = (
        str(output_path)
        if output_path
        else str(
            VIDEO_DEST_DIRECTORY
            / str(os.path.basename(video_file).split(".")[0] + ".mp4")
        )
    )
    logging.info(
        f"{os.path.basename(output_path).split('.')[0]}: Merging audio and video."
    )

    command = f"ffmpeg -y -i {video_file} -i {audio_file} -c:v copy -c:a aac -strict experimental -b:a 192k {output_path} -hide_banner -loglevel error"
    subprocess.call(command, shell=True)


def get_video_length(video_file: str) -> float:
    """Returns the length of the given video file in seconds."""
    return VideoFileClip(video_file).duration


def get_audio_length(audio_file: str) -> float:
    """Returns the audio file length in seconds."""
    with wave.open(audio_file, "r") as f:
        return f.getnframes() / float(f.getframerate())


def adjust_audio_length_to_video(
    audio_file: str, video_file: str, output_path: str = None
) -> None:
    """Adjusts the audio length of the given audio file to the length of the given video file."""
    output_path = output_path if output_path else audio_file
    length = get_video_length(video_file)

    adjust_audio_length(
        audio_file=audio_file,
        length=length,
        output_path=output_path,
    )


def adjust_audio_length(audio_file: str, length: float, output_path: str = None):
    """Adjusts the speed of an audio file, so it matches the given length."""
    output_path = output_path if output_path else audio_file
    y, sr = librosa.load(audio_file)
    length_ms = length * 1000
    #Bug: get_duration() takes 0 positional arguments but 2 were given
    factor = (librosa.get_duration(y=y, sr=sr) * 1000) / length_ms
    short_y = librosa.effects.time_stretch(y, factor)

    sf.write(output_path, short_y, sr)


def embed_subtitles_in_mp4(
    video_file: str,
    subtitles_file: str,
    language: str,
    output_path: str = None,
):
    """This method embeds the given subtitles in the video file. The subtitles must be formatted in .srt"""
    output_path = (
        str(output_path)
        if output_path
        else f"{VIDEO_SUBTITLES_DIRECTORY / os.path.basename(video_file)}"
    )
    logging.info(
        f"{os.path.basename(output_path).split('.')[0]}: Embedding subtitle in the video."
    )

    command = f"ffmpeg -i {video_file} -i {subtitles_file} -c copy -c:s mov_text -metadata:s:s:0 language={language} {output_path} -hide_banner -loglevel error"
    subprocess.call(command, shell=True)


def embed_two_subtitles_in_mp4(
    video_file: str,
    first_subtitles_file: str,
    first_language: str,
    second_subtitles_file: str,
    second_language: str,
    output_path: str = None,
):
    output_path = (
        str(output_path)
        if output_path
        else f"{VIDEO_SUBTITLES_DIRECTORY / os.path.basename(video_file)}"
    )
    logging.info(
        f"{os.path.basename(output_path).split('.')[0]}: Embedding subtitles in the video."
    )

    command = f"ffmpeg -i {video_file} -i {first_subtitles_file} -i {second_subtitles_file} -metadata:s:s:0 language={first_language} -metadata:s:s:1 language={second_language} -c:v copy -c:a copy -c:s mov_text -map 0:v -map 0:a -map 1:s -map 2:s {output_path} -hide_banner -loglevel error"
    subprocess.call(command, shell=True)


def print_subtitles_on_video(
    video_file: str, subtitles_file: str, output_path: str = None
) -> None:
    """This method prints the subtitles on the video."""
    output_path = (
        output_path
        if output_path
        else str(
            VIDEO_SUBTITLES_DIRECTORY
            / str(os.path.basename(video_file).split(".")[0] + ".mp4")
        )
    )
    logging.info(
        f"{os.path.basename(output_path).split('.')[0]}: Printing subtitles on the video frames."
    )

    command = f"ffmpeg -y -i {video_file} -vf subtitles={subtitles_file} {output_path} -hide_banner -loglevel error"
    subprocess.call(command, shell=True)
