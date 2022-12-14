"""This module contains functions for handling files.
This includes:
- splitting a video into audio and video files
- merging audio and video files
- deleting files
- merging video and captions
"""

import os
import subprocess

from utils import (
    AUDIO_DIRECTORY,
    AUDIO_TRANSLATED_SPEED_DIRECTORY,
    PATH_SEPARATOR,
    VIDEO_CAPTIONS_DIRECTORY,
    VIDEO_DEST_DIRECTORY,
    VIDEO_DIRECTORY,
)


def get_audio_from_video_file(
    video_file: str, output_path: str = AUDIO_DIRECTORY, file_name: str = None
) -> None:
    """Extracts the audio from the given video file and saves it to the audio directory."""

    file_name = file_name if file_name else os.path.basename(video_file).split(".")[0]
    audio_path = output_path + PATH_SEPARATOR + f"{file_name}.wav"

    command = f"ffmpeg -y -i {video_file} -ab 160k -ac 2 -ar 44100 -vn {audio_path}"
    subprocess.call(command, shell=True)


def merge_audio_and_video_to_mp4(
    video_file: str,
    audio_file: str,
    output_path: str = str(VIDEO_DEST_DIRECTORY),
    file_name: str = None,
) -> None:
    """Fuses the audio (from AUDIO_DIRECTORY) and video (from VIDEO_DIRECTORY)
    file and saves it to the video destination (VIDEO_DEST_DIRECTORY) directory.
    The output path is without the filename or extension."""

    file_name = file_name if file_name else os.path.basename(video_file).split(".")[0]
    output_path = output_path + PATH_SEPARATOR + f"{file_name}.mp4"

    print()
    print(f"output_path: {output_path}")
    print(f"video_file: {video_file}")
    print(f"audio_file: {audio_file}")
    print()

    command = f"ffmpeg -y -i {video_file} -i {audio_file} -c:v copy -c:a aac -strict experimental -b:a 192k {output_path}"
    subprocess.call(command, shell=True)

    # Delete the video and audio file.
    # delete(video_file)
    # delete(audio_file)


def remove_audio_from_video_file(
    video_file: str, output_path: str = str(VIDEO_DIRECTORY), file_name: str = None
) -> None:
    """Removes the audio from the given video file and saves it to the video destination directory.
    The output path is without the filename or extension."""

    file_name = file_name if file_name else os.path.basename(video_file).split(".")[0]
    output_path = output_path + PATH_SEPARATOR + f"{file_name}.mp4"

    command = f"ffmpeg -y -i {str(video_file)} -vcodec copy -an {output_path}"
    subprocess.call(command, shell=True)


def merge_video_and_captions(
    video_file: str,
    captions_file: str,
    output_path: str = str(VIDEO_CAPTIONS_DIRECTORY),
    file_name: str = None,
) -> None:
    """Merges a video file and captions file and saves it to the destination.
    The output path is without the filename or extension.
    The file name is without the extension."""

    file_name = file_name if file_name else os.path.basename(video_file).split(".")[0]
    output_path = output_path + PATH_SEPARATOR + f"{file_name}.mp4"

    print(video_file)
    print(captions_file)
    print(output_path)

    command = f"ffmpeg -y -i {video_file} -vf subtitles={captions_file} {output_path}"
    subprocess.call(command, shell=True)

    # Delete the video and captions file
    # delete(video_file)
    # delete(captions_file)

    # HIER ETWAS ÄNDERN


def split_video(
    video_file: str,
    video_output_path: str = str(VIDEO_DIRECTORY),
    video_file_name: str = None,
    audio_output_path: str = str(AUDIO_DIRECTORY),
    audio_file_name: str = None,
) -> None:
    """Splits the given video file into an audio file and a video file without audio."""

    get_audio_from_video_file(
        video_file=video_file, output_path=audio_output_path, file_name=audio_file_name
    )
    remove_audio_from_video_file(
        video_file=video_file, output_path=video_output_path, file_name=video_file_name
    )

    # Delete the video file
    # delete(video_file)
    # delete(audio_file)


def delete(file_path: str) -> None:
    """Deletes the file at the given path."""
    os.remove(file_path)


def get_video_length(video_file: str) -> float:
    """Returns the length of the given video file in seconds."""
    command = (
        f"ffmpeg -i {video_file} 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//"
    )
    video_length = subprocess.check_output(command, shell=True)
    video_length = video_length.decode("utf-8")
    video_length = video_length.split(":")

    hours = int(video_length[0])
    minutes = int(video_length[1])
    seconds = float(video_length[2])

    video_length = hours * 3600 + minutes * 60 + seconds

    return video_length


def get_audio_length(audio_file: str) -> float:
    """Returns the length of the given audio file in seconds."""
    command = (
        f"ffmpeg -i {audio_file} 2>&1 | grep 'Duration' | cut -d ' ' -f 4 | sed s/,//"
    )
    audio_length = subprocess.check_output(command, shell=True)
    audio_length = audio_length.decode("utf-8")
    audio_length = audio_length.split(":")

    hours = int(audio_length[0])
    minutes = int(audio_length[1])
    seconds = float(audio_length[2])

    audio_length = hours * 3600 + minutes * 60 + seconds

    return audio_length


def adjust_audio_length(
    audio_file: str,
    video_file: str,
    output_path: str = str(AUDIO_TRANSLATED_SPEED_DIRECTORY),
    file_name=None,
) -> None:
    """Adjusts the audio length of the given audio file to the length of the given video file."""

    file_name = file_name if file_name else os.path.basename(video_file).split(".")[0]
    output_path = output_path + PATH_SEPARATOR + f"{file_name}.wav"

    video_length = get_video_length(video_file)
    audio_length = get_audio_length(audio_file)

    speed = audio_length / video_length

    command = f'ffmpeg -y -i {audio_file} -filter:a "atempo={speed}" {output_path}'
    subprocess.call(command, shell=True)

    # Delete the audio file.
    # delete(audio_file)
