import abc
from abc import ABC


class Speaker(ABC):

    @abc.abstractmethod
    def save_to_file(self, text: str, filename: str, audio_format: str = "mp3") -> None:
        pass
