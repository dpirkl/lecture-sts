import src as sts
import click


@click.command()
@click.option(
    "--des_lang",
    help="The language for translation",
    prompt="Enter the destination language (i.e. 'EN-US')",
    type=str,
)
@click.option(
    "--path",
    help="The path of the file for translation",
    prompt="Enter the path of the source file",
    type=str,
)
@click.option(
    "--source_lang",
    default=None,
    show_default=False,
    help="The language of the audio file to be translated",
    type=str,
)
@click.option(
    "--transcription",
    default=False,
    show_default=True,
    help="Whether a file of the transcription in the original langauge should be saved",
    type=bool,
)
@click.option(
    "--trans_text",
    default=False,
    show_default=True,
    help="Whether a file of the translated transcription should be saved",
    type=bool,
)
@click.option(
    "--output_path",
    default=None,
    show_default=False,
    help="The path used to save the generated files",
    type=str,
)
@click.option(
    "--formality",
    default="prefer_more",
    show_default=True,
    help="The formality of the translation",
    type=str,
)
def main(
        des_lang: str,
        path: str,
        source_lang: str,
        transcription: bool,
        trans_text: bool,
        output_path: str,
        formality: str
) -> None:
    if output_path is None:
        output_path = path


    stt = sts.SpeechToText()
    t = sts.DeepLTranslator(target_lang=des_lang, source_lang=source_lang, formality=formality)
    tts1 = sts.PYTTSX3Speaker()
    tts2 = sts.TTSSpeaker(out_path=output_path)

    print("Loaded all modules.")

    transcription_text: str = stt.transcribe_advanced(path)
    # Save a text file of the transcription if the user specified it.
    if transcription:
        with open(output_path.join("transcription.txt")) as transcription_txt:
            transcription_txt.write(transcription_text)

    translation_text: str = t.translate(transcription_text)
    if trans_text:
        with open(output_path.join("translation.txt")) as translation_txt:
            translation_txt.write(translation_text)

    tts1.save_to_file(translation_text, f"{output_path}_translated")
    tts2.main(translation_text)

    print("Done.")


if __name__ == "__main__":
    main()
