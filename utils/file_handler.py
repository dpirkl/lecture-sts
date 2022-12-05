"""This module contains functions for handling files.
This includes:
- splitting a video into audio and video files
- merging audio and video files
- deleting files
- merging video and captions
"""

import subprocess
import os

from utils import VIDEO_DIRECTORY, AUDIO_DIRECTORY, VIDEO_DEST_DIRECTORY


def get_audio_from_video_file(
    video_file: str, output_path: str = AUDIO_DIRECTORY, file_name: str = None
) -> None:
    """Extracts the audio from the given video file and saves it to the audio directory."""

    file_name = file_name if file_name else os.path.basename(video_file).split(".")[0]
    audio_path = output_path / file_name + ".wav"

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
    output_path = output_path / file_name + ".mp4"

    command = f"ffmpeg -y -i {video_file} -i {audio_file} -c:v copy -c:a aac -strict experimental -b:a 192k {output_path}"
    subprocess.call(command, shell=True)

    # Delete the video and audio file.
    delete(video_file)
    delete(audio_file)


def remove_audio_from_video_file(
    video_file: str, output_path: str = str(VIDEO_DIRECTORY), file_name: str = None
) -> None:
    """Removes the audio from the given video file and saves it to the video destination directory.
    The output path is without the filename or extension."""

    file_name = file_name if file_name else os.path.basename(video_file).split(".")[0]
    output_path = output_path / file_name + ".mp4"

    command = f"ffmpeg -y -i {str(video_file)} -vcodec copy -an {output_path}"
    subprocess.call(command, shell=True)


def merge_video_and_captions(
    video_file: str,
    captions_file: str,
    output_path: str = str(VIDEO_DEST_DIRECTORY),
    file_name: str = None,
) -> None:
    """Merges a video file and captions file and saves it to the destination.
    The output path is without the filename or extension.
    The file name is without the extension."""

    file_name = file_name if file_name else os.path.basename(video_file).split(".")[0]
    output_path = output_path / file_name + ".mp4"

    command = f"ffmpeg -y -i {video_file} -vf subtitles={captions_file} {output_path}"
    subprocess.call(command, shell=True)

    # Delete the video and captions file
    delete(video_file)
    delete(captions_file)


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
    delete(video_file)


def delete(file_path: str) -> None:
    """Deletes the file at the given path."""
    os.remove(file_path)
