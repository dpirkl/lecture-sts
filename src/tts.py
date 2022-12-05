import TTS
from pathlib import Path

from TTS.utils.manage import ModelManager
from TTS.utils.synthesizer import Synthesizer


class TTSSpeaker:
    out_path: Path
    model_path: Path
    config_path: Path
    speakers_file_path: Path
    language_ids_file_path: Path
    vocoder_path: Path
    vocoder_config_path: Path
    encoder_path: Path
    encoder_config_path: Path
    model_name: str
    speaker_idx: int
    language_idx: int
    speaker_wav: Path
    reference_wav: Path
    capacitron_style_wav: Path
    capacitron_style_text: str
    reference_speaker_idx: int

    manager: ModelManager

    synthesizer: Synthesizer

    def __init__(
        self,
        out_path,
        model_path=None,
        config_path=None,
        speakers_file_path=None,
        language_ids_file_path=None,
        vocoder_path=None,
        vocoder_config_path=None,
        encoder_path=None,
        encoder_config_path=None,
        speaker_idx=None,
        language_idx=None,
        speaker_wav=None,
        reference_wav=None,
        capacitron_style_wav=None,
        capacitron_style_text=None,
        reference_speaker_idx=None,
        model_name="tts_models/en/ljspeech/tacotron2-DDC",
        vocoder_name=None,
    ):

        path = Path(TTS.__file__).parent / "bin/../models.json"
        print(path)

        self.manager = ModelManager(path)

        self.out_path = Path(out_path)
        self.model_path = model_path
        self.config_path = config_path
        self.speakers_file_path = speakers_file_path
        self.language_ids_file_path = language_ids_file_path
        self.vocoder_path = vocoder_path
        self.vocoder_config_path = vocoder_config_path
        self.encoder_path = encoder_path
        self.encoder_config_path = encoder_config_path
        self.model_name = model_name
        self.speaker_idx = speaker_idx
        self.language_idx = language_idx
        self.speaker_wav = speaker_wav
        self.reference_wav = reference_wav
        self.capacitron_style_wav = capacitron_style_wav
        self.capacitron_style_text = capacitron_style_text
        self.reference_speaker_idx = reference_speaker_idx

        # load pre-trained model paths
        if model_name is not None and not model_path:
            model_path, config_path, model_item = self.manager.download_model(
                model_name
            )
            vocoder_name = (
                model_item["default_vocoder"] if vocoder_name is None else vocoder_name
            )

        if vocoder_name is not None and not vocoder_path:
            vocoder_path, vocoder_config_path, _ = self.manager.download_model(
                vocoder_name
            )

        # set custom model paths
        if model_path is not None:
            self.model_path = model_path
            self.config_path = config_path
            self.speakers_file_path = speakers_file_path
            self.language_ids_file_path = language_ids_file_path

        if vocoder_path is not None:
            self.vocoder_path = vocoder_path
            self.vocoder_config_path = vocoder_config_path

        if encoder_path is not None:
            self.encoder_path = encoder_path
            self.encoder_config_path = encoder_config_path

        # load models
        self.synthesizer = Synthesizer(
            model_path,
            config_path,
            speakers_file_path,
            language_ids_file_path,
            vocoder_path,
            vocoder_config_path,
            encoder_path,
            encoder_config_path,
        )

    def list_models(self):
        self.manager.list_models()

    def list_speaker_idxs(self):
        print(
            " > Available speaker ids: (Set self.speaker_idx flag to one of these values to use the multi-speaker model. Via set_speaker_idx()."
        )
        print(self.synthesizer.tts_model.speaker_manager.name_to_id)
        return

    def list_language_idxs(self):
        print(
            " > Available language ids: (Set self.language_idx flag to one of these values to use the multi-lingual model. Via set_language_idx()."
        )
        print(self.synthesizer.tts_model.language_manager.name_to_id)

        return

    def set_speaker_idx(self, speaker_idx):
        self.speaker_idx = speaker_idx

    def save_to_file(self, text, filename, audio_format="mp3"):
        """Overw"""

        # check the arguments against a multi-speaker model.
        if self.synthesizer.tts_speakers_file and (
            not self.speaker_idx and not self.speaker_wav
        ):
            print(
                " [!] Looks like you use a multi-speaker model. Define `--speaker_idx` to "
                "select the target speaker. You can list the available speakers for this model by `--list_speaker_idxs`."
            )
            return

        # RUN THE SYNTHESIS
        if text:
            print(" > Text: {}".format(text))

        # kick it
        wav = self.synthesizer.tts(
            text,
            self.speaker_idx,
            self.language_idx,
            self.speaker_wav,
            reference_wav=self.reference_wav,
            style_wav=self.capacitron_style_wav,
            style_text=self.capacitron_style_text,
            reference_speaker_name=self.reference_speaker_idx,
        )

        # save the results
        print(" > Saving output to {}".format(self.out_path))
        self.synthesizer.save_wav(
            wav, str(self.out_path / f"{filename}.{audio_format}")
        )
