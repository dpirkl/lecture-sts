import subprocess
import os

from pathlib import Path

from utils import (
    VIDEO_DIRECTORY,
    AUDIO_DIRECTORY,
    AUDIO_DEST_DIRECTORY,
    VIDEO_DEST_DIRECTORY,
    ORIGINAL_VIDEO_DIRECTORY,
    CAPTIONS_DIRECTORY,
)


def get_audio_from_video_file(video_file: str) -> None:
    """Extracts the audio from the given video file and saves it to the audio directory."""
    video_name = os.path.basename(video_file).split(".")[0]
    audio_path = AUDIO_DIRECTORY / (video_name + ".wav")
    command = f"ffmpeg -y -i {video_file} -ab 160k -ac 2 -ar 44100 -vn {audio_path}"
    subprocess.call(command, shell=True)


def merge_audio_and_video_to_mp4(video_file: str, audio_file: str) -> None:
    """Fuses the audio (from AUDIO_DIRECTORY) and video (from VIDEO_DIRECTORY)
    file and saves it to the video destination (VIDEO_DEST_DIRECTORY) directory."""

    # merge video and mono audio

    output_path = VIDEO_DEST_DIRECTORY / (
        os.path.basename(video_file).split(".")[0] + ".mp4"
    )
    command = f"ffmpeg -y -i {video_file} -i {audio_file} -c:v copy -c:a aac -strict experimental -b:a 192k {output_path}"
    subprocess.call(command, shell=True)


def remove_audio_from_video_file(video_file: str) -> None:
    """Removes the audio from the given video (from VIDEO_DIRECTORY) file and saves it to the video destination directory."""
    video_name = os.path.basename(video_file).split(".")[0]
    output_path = VIDEO_DIRECTORY / f"{video_name}.mp4"
    command = f"ffmpeg -y -i {str(video_file)} -vcodec copy -an {output_path}"
    subprocess.call(command, shell=True)


def merge_video_and_captions(video_file: str, captions_file: str) -> None:
    """Merges the video (from VIDEO_DIRECTORY) and captions (from CAPTIONS_DIRECTORY)
    file and saves it to the video destination (VIDEO_DEST_DIRECTORY) directory."""

    video_name = os.path.basename(video_file).split(".")[0]
    output_path = VIDEO_DEST_DIRECTORY / f"{video_name}.mp4"
    command = f"ffmpeg -y -i {video_file} -vf subtitles={captions_file} {output_path}"
    subprocess.call(command, shell=True)
