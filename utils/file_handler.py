import subprocess

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
    print(video_file)
    video_path: Path = video_file
    video_name = video_path.name.split(".")[0]
    print(video_name)
    audio_path = AUDIO_DIRECTORY / (video_name + ".wav")
    print(audio_path)
    command = f"ffmpeg -y -i {video_file} -ab 160k -ac 2 -ar 44100 -vn {audio_path}"
    subprocess.call(command, shell=True)


def merge_audio_and_video_to_mp4(video_file: str, audio_file: str) -> None:
    """Fuses the audio (from AUDIO_DIRECTORY) and video (from VIDEO_DIRECTORY)
    file and saves it to the video destination (VIDEO_DEST_DIRECTORY) directory."""

    video_path = VIDEO_DIRECTORY / video_file
    audio_path = AUDIO_DEST_DIRECTORY / audio_file
    output_path = VIDEO_DEST_DIRECTORY / (video_file.split(".")[0] + ".mp4")
    command = f"ffmpeg -y -i {video_path} -i {audio_path} -c copy -map 0:v:0 -map 1:a:0 {output_path}"
    subprocess.call(command, shell=True)


def remove_audio_from_video_file(video_file: str) -> None:
    """Removes the audio from the given video (from VIDEO_DIRECTORY) file and saves it to the video destination directory."""
    video_path = ORIGINAL_VIDEO_DIRECTORY / video_file
    output_path = VIDEO_DIRECTORY / video_file
    command = f"ffmpeg -y -i {video_path} -vcodec copy -an {output_path}"
    subprocess.call(command, shell=True)


def merge_video_and_captions(video_file: str, captions_file: str) -> None:
    """Merges the video (from VIDEO_DIRECTORY) and captions (from CAPTIONS_DIRECTORY)
    file and saves it to the video destination (VIDEO_DEST_DIRECTORY) directory."""

    video_path = VIDEO_DIRECTORY / video_file
    captions_path = CAPTIONS_DIRECTORY / captions_file
    output_path = VIDEO_DEST_DIRECTORY / video_file
    command = f"ffmpeg -y -i {video_path} -vf subtitles={captions_path} {output_path}"
    subprocess.call(command, shell=True)
