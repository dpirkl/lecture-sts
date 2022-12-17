import whisper


class SpeechToText:
    """A class for transcribing audio files."""

    model: whisper.Whisper
    fp16_settings: bool

    def __init__(self, model: str = "small", fp16_settings: bool = False):
        self.model = whisper.load_model(model)
        self.fp16_settings = fp16_settings

    def transcribe(self, file: str) -> str:
        """Transcribes the given audio file."""

        result = self.model.transcribe(file, fp16=self.fp16_settings)["text"]

        return result

    def transcribe_and_translate(self, file: str) -> str:
        """Transcribes and translates the given audio file."""

        options = whisper.DecodingOptions(task="translate")

        result = self.model.transcribe(file, fp16=self.fp16_settings, options=options)[
            "text"
        ]

        return result
