import os
from pathlib import Path


def get_audio_dest_directory() -> str:
    """Returns the path to the audio destination directory."""
    return str(Path(__file__).parent.parent / 'data' / 'audio_translated')

def get_test_audio_directory() -> str:
    """Returns the path to the test audio directory."""
    return str(path = Path(__file__).parent.parent / "data" / "audio" / "test.mp3")


AUDIO_DEST_DIRECTORY = get_audio_dest_directory()
