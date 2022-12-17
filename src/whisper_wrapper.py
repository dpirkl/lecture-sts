"""This class is a simple wrapper for the whisper libary"""
import whisper


class Transcriber:

    model: whisper.Whisper
    fp16_settings: bool

    def __init__(self, model: str = "small", fp16_settings: bool = False):
        """Initializes a Transcriber object. You can set the model size and specify the fp16 settings.


        Args:
            model (str, optional): The size of the transcription model. Defaults to "small".
            fp16_settings (bool, optional): Wheter to use fp16 (or fp32). Defaults to False.
        """

        self.model = whisper.load_model(name=model)
        self.fp16_settings = fp16_settings

    def transcribe(self, file: str) -> dict:
        """This method transcribes a given audio file.

        Args:
            file (str): The path to the audio file.

        Returns:
            dict: The result of the transcripton. The plain text can be accessed by 'result["text"]'.
        """

        return self.model.transcribe(file, fp16=self.fp16_settings)

    def transcribe_and_translate(self, file: str) -> dict:
        """This method transcribes the audio file and translates it to english.

        Args:
            file (str): The path to the audio file.

        Returns:
            dict: The result of the transcription. The plain text can be accessed by 'result["text"]'.
        """

        options = whisper.DecodingOptions(task="translate")
        return self.model.transcribe(file, fp16=self.fp16_settings, options=options)
