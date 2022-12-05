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
        options = whisper.DecodingOptions(fp16=self.fp16_settings)

        result = self.model.transcribe(file, fp16=self.fp16_settings)["text"]

        return result

    def transcribe_and_translate(self, file: str) -> str:
        """Transcribes and translates the given audio file."""

        options = whisper.DecodingOptions(task="translate")

        result = self.model.transcribe(file, fp16=self.fp16_settings, options=options)[
            "text"
        ]

        return result

    def transcribe_advanced(self, file: str) -> str:
        """Transcribes the given audio file. Uses more steps than transcribe() for an optimized transcription.
        Only the first 30 seconds of the audio file will be transcribed.

        """

        # Processing of the audio file. Trims or pads it to fit 30 seconds.
        audio = whisper.load_audio(file)
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        options = whisper.DecodingOptions(fp16=self.fp16_settings)
        result = whisper.decode(self.model, mel, options).text

        return result

    def transcribe_and_translate_advanced(self, file: str) -> str:
        """Transcribes and translates the given audio file.
        Only the first 30 seconds of the audio file will be transcribed and translated.

        """

        audio = whisper.load_audio(file)
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(self.model.device)

        options = whisper.DecodingOptions(fp16=self.fp16_settings, task="translate")
        result = whisper.decode(self.model, mel, options).text

        return result
