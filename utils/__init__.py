"""This module contains all the utility functions for the project."""

__all__ = [
    "file_handler",
    "path_handler",
    "AUDIO_DIRECTORY",
    "AUDIO_DEST_DIRECTORY",
    "DATA_DIRECTORY",
    "PROJECT_DIRECTORY",
    "VIDEO_DEST_DIRECTORY",
    "VIDEO_DIRECTORY",
    "ORIGINAL_VIDEO_DIRECTORY",
    "TRANSCRIPT_DIRECTORY",
    "CAPTIONS_DIRECTORY",
    "PATH_SEPARATOR",
    "VIDEO_CAPTIONS_DIRECTORY",
]

from .path_handler import (
    AUDIO_DIRECTORY,
    AUDIO_DEST_DIRECTORY,
    DATA_DIRECTORY,
    PROJECT_DIRECTORY,
    VIDEO_DEST_DIRECTORY,
    VIDEO_DIRECTORY,
    ORIGINAL_VIDEO_DIRECTORY,
    TRANSCRIPT_DIRECTORY,
    CAPTIONS_DIRECTORY,
    PATH_SEPARATOR,
    VIDEO_CAPTIONS_DIRECTORY,
)

from . import file_handler
from . import path_handler
