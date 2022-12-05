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


def get_video_directory() -> Path:
    """Returns the path to the video directory."""
    data_directory = get_data_directory()
    return data_directory / "video"


def get_video_dest_directory() -> Path:
    """Returns the path to the video destination directory."""
    data_directory = get_data_directory()
    return data_directory / "video-translated"


def get_original_video_directory() -> Path:
    """Returns the path to the original video directory."""
    return get_data_directory() / "original-video"


def get_transcript_directory() -> Path:
    """Returns the path to the transcript directory."""
    return get_data_directory() / "transcript-translated"


def get_captions_directory() -> Path:
    """Returns the path to the captions directory."""
    return get_data_directory() / "captions"


AUDIO_DIRECTORY = get_audio_directory()
AUDIO_DEST_DIRECTORY = get_audio_dest_directory()

VIDEO_DIRECTORY = get_video_directory()
VIDEO_DEST_DIRECTORY = get_video_dest_directory()

PROJECT_DIRECTORY = get_project_directory()

DATA_DIRECTORY = get_data_directory()

ORIGINAL_VIDEO_DIRECTORY = get_original_video_directory()

TRANSCRIPT_DIRECTORY = get_transcript_directory()

CAPTIONS_DIRECTORY = get_captions_directory()
