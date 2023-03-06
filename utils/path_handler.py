import logging
import os
from pathlib import Path


def get_project_directory() -> Path:
    """Returns the path to the project directory."""
    return Path(__file__).parent.parent


def get_data_directory() -> Path:
    """Returns the path to the data directory."""
    project_directory = get_project_directory()
    return project_directory / "data"


def get_audio_directory() -> Path:
    """Returns the path to the audio directory."""
    data_directory = get_data_directory()
    return data_directory / "audio"


def get_audio_dest_directory() -> Path:
    """Returns the path to the audio destination directory."""
    data_directory = get_data_directory()
    return data_directory / "audio-translated"


def get_audio_translated_speed_directory() -> Path:
    """Returns the path to the audio translated speed directory."""
    return get_data_directory() / "audio-translated-speed"


def get_video_directory() -> Path:
    """Returns the path to the video directory."""
    data_directory = get_data_directory()
    return data_directory / "video-without-audio"


def get_video_dest_directory() -> Path:
    """Returns the path to the video destination directory."""
    data_directory = get_data_directory()
    return data_directory / "video-translated"


def get_original_video_directory() -> Path:
    """Returns the path to the original video directory."""
    return get_data_directory() / "video-original"


def get_video_subtitles_directory() -> Path:
    """Returns the path to the subtitle directory."""
    return get_data_directory() / "video-translated-subtitles"


def get_subtitles_original_language_directory() -> Path:
    """Returns the path to the subtitle original language directory."""
    return get_data_directory() / "video-original-subtitles"


def get_subtitles_directory() -> Path:
    """Returns the path to the subtitle directory."""
    return get_data_directory() / "subtitles"


def get_variable_directory() -> Path:
    """Returns the path to the variable directory."""
    return get_data_directory() / "variables"


PROJECT_DIRECTORY = get_project_directory()
DATA_DIRECTORY = get_data_directory()

AUDIO_DIRECTORY = get_audio_directory()
AUDIO_DEST_DIRECTORY = get_audio_dest_directory()
AUDIO_TRANSLATED_SPEED_DIRECTORY = get_audio_translated_speed_directory()

ORIGINAL_VIDEO_DIRECTORY = get_original_video_directory()
ORIGINAL_VIDEO_SUBTITLES_DIRECTORY = get_subtitles_original_language_directory()
VIDEO_DIRECTORY = get_video_directory()
VIDEO_DEST_DIRECTORY = get_video_dest_directory()
VIDEO_SUBTITLES_DIRECTORY = get_video_subtitles_directory()

SUBTITLES_DIRECTORY = get_subtitles_directory()

VARIABLE_DIRECTORY = get_variable_directory()


def create_folders():
    """Create folders for storing audio, video and subtitles."""
    logging.info("Creating folders.")
    if not os.path.exists(DATA_DIRECTORY):
        os.makedirs(DATA_DIRECTORY)
    if not os.path.exists(AUDIO_DIRECTORY):
        os.makedirs(AUDIO_DIRECTORY)
    if not os.path.exists(VIDEO_DIRECTORY):
        os.makedirs(VIDEO_DIRECTORY)
    if not os.path.exists(VIDEO_SUBTITLES_DIRECTORY):
        os.makedirs(VIDEO_SUBTITLES_DIRECTORY)
    if not os.path.exists(AUDIO_DEST_DIRECTORY):
        os.makedirs(AUDIO_DEST_DIRECTORY)
    if not os.path.exists(VIDEO_DEST_DIRECTORY):
        os.makedirs(VIDEO_DEST_DIRECTORY)
    if not os.path.exists(ORIGINAL_VIDEO_DIRECTORY):
        os.makedirs(ORIGINAL_VIDEO_DIRECTORY)
    if not os.path.exists(SUBTITLES_DIRECTORY):
        os.makedirs(SUBTITLES_DIRECTORY)
    if not os.path.exists(AUDIO_TRANSLATED_SPEED_DIRECTORY):
        os.makedirs(AUDIO_TRANSLATED_SPEED_DIRECTORY)
    if not os.path.exists(ORIGINAL_VIDEO_SUBTITLES_DIRECTORY):
        os.makedirs(ORIGINAL_VIDEO_SUBTITLES_DIRECTORY)
    if not os.path.exists(VARIABLE_DIRECTORY):
        os.makedirs(VARIABLE_DIRECTORY)
