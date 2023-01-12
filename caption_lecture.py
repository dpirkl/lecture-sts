"""This module is used to translate the videos."""
from pathlib import Path

import whisper
from rtpt import RTPT

from src.whisper_wrapper import Transcriber
from utils import file_handler
from utils.path_handler import (
    AUDIO_DIRECTORY,
    CAPTIONS_DIRECTORY,
    ORIGINAL_VIDEO_DIRECTORY,
    TRANSCRIPT_DIRECTORY,
)


def main(directory_of_videos: Path = ORIGINAL_VIDEO_DIRECTORY, rtpt: bool = True):

    """This function is the main function of the program. It is called when the program is executed.
    It is responsible for the whole process of translating a lecture.
    Steps:
    - split all videos into audio files and video files without audio
    - translate and transcribe the audio files
    - generate captions and text files
    - synthesize the audio files
    - merge the audio files and the video files
    - merge the video files and the captions
    """

    if rtpt:
        rtpt = RTPT(
            name_initials="DP",
            experiment_name="Translate_Lecture:_Intro_to_AI",
            max_iterations=40,
        )
        rtpt.start()

    # load the transcriber

    for original_video in directory_of_videos.iterdir():
        print(f"Transcribing {original_video.anchor}...")
        transcriber = Transcriber(model="large")

        # split all videos into audio files and video files without audio
        # audio files are saved in AUDIO_DIRECTORY
        # new video files are saved in VIDEO_DIRECTORY
        file_handler.get_audio_from_video_file(str(original_video))

        # transcribe audio file
        lecture_name = original_video.stem
        result = transcriber.transcribe_and_translate(
            str(AUDIO_DIRECTORY / f"{lecture_name}.wav")
        )

        # save transcript to a text file
        with open((TRANSCRIPT_DIRECTORY / f"{lecture_name}.txt"), "w") as transcript:
            whisper.utils.write_txt(result["segments"], file=transcript)

        # generate captions
        with open(
            (CAPTIONS_DIRECTORY / f"{lecture_name}.vtt"), "w", encoding="UTF-8"
        ) as vvt:
            whisper.utils.write_vtt(result["segments"], file=vvt)

        # merge video and subtitles
        file_handler.merge_video_and_captions(
            video_file=str(ORIGINAL_VIDEO_DIRECTORY / f"{lecture_name}.mp4"),
            captions_file=str(CAPTIONS_DIRECTORY / f"{lecture_name}.vtt"),
        )

        rtpt.step()


if __name__ == "__main__":
    print("Starting the program...")
    main()
    print("Program finished.")
