import src as sts
import click
import os
import utils


@click.command()
@click.option(
    "--path",
    help="The path of the file for translation",
    prompt="Enter the path of the source file",
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
    "--output_path",
    default=None,
    show_default=False,
    help="The path used to save the generated files",
    type=str,
)
def main(
        
        path: str,
        
        transcription: bool,
        
        output_path: str,
        
) -> None:
    if output_path is None:
        output_path = utils.AUDIO_DEST_DIRECTORY

    stt = sts.SpeechToText()
    tts1 = sts.PYTTSX3Speaker()
    tts2 = sts.TTSSpeaker(out_path=output_path)

    print("Loaded all modules.")

    translation_text: str = stt.transcribe_and_translate(path)
    # Save a text file of the transcription if the user specified it.
    if transcription:
        with open(os.join(output_path, "transcription.txt")) as transcription_txt:
            transcription_txt.write(translation_text)

    tts1.save_to_file(translation_text, f"translated.mp3")
    tts2.main(translation_text, 'tts_translated', audio_format='mp3')

    print("Done.")


if __name__ == "__main__":
    main()
