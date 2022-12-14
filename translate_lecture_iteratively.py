"""This module is used to translate the videos."""
from pathlib import Path

import whisper
from rtpt import RTPT

from src.tts_wrapper import Speaker
from utils import (
    AUDIO_DEST_DIRECTORY,
    AUDIO_DIRECTORY,
    AUDIO_TRANSLATED_SPEED_DIRECTORY,
    CAPTIONS_DIRECTORY,
    ORIGINAL_VIDEO_DIRECTORY,
    TRANSCRIPT_DIRECTORY,
    VIDEO_DEST_DIRECTORY,
    VIDEO_DIRECTORY,
    file_handler,
)


def main(directory_of_videos: Path = ORIGINAL_VIDEO_DIRECTORY):

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

    rtpt = RTPT(
        name_initials="DP",
        experiment_name="Translate_Lecture:_Intro_to_AI",
        max_iterations=len(list(directory_of_videos.iterdir())),
    )

    rtpt.start()

    # load the model
    model = whisper.load_model("large")
    options = {"task": "translate", "fp16": False, "beam_size": 5, "best_of": 5}

    # load the synthesizer
    synthesizer = Speaker()

    for original_video in directory_of_videos.iterdir():
        # split all videos into audio files and video files without audio
        # audio files are saved in AUDIO_DIRECTORY
        # new video files are saved in VIDEO_DIRECTORY
        file_handler.split_video(str(original_video))

        # transcribe audio file
        lecture_name = original_video.stem
        result = model.transcribe(
            str(AUDIO_DIRECTORY / f"{lecture_name}.wav"), **options
        )

        # save transcript to a text file
        with open((TRANSCRIPT_DIRECTORY / f"{lecture_name}.txt"), "w") as transcript:
            whisper.utils.write_txt(result["segments"], file=transcript)

        # generate captions
        with open(
            (CAPTIONS_DIRECTORY / f"{lecture_name}.vtt"), "w", encoding="UTF-8"
        ) as vvt:
            whisper.utils.write_vtt(result["segments"], file=vvt)

        # synthesize audio file
        synthesizer.speak(
            result["text"], str(AUDIO_DEST_DIRECTORY / f"{lecture_name}.wav")
        )

        # fit the length of the audio file to the length of the video file and save it in AUDIO_DEST_DIRECTORY
        file_handler.adjust_audio_length(
            audio_file=str(AUDIO_DIRECTORY / f"{lecture_name}.wav"),
            video_file=str(VIDEO_DIRECTORY / f"{lecture_name}.mp4"),
        )

        # merge the audio file and the video file
        file_handler.merge_audio_and_video_to_mp4(
            VIDEO_DIRECTORY / f"{lecture_name}.mp4",
            AUDIO_TRANSLATED_SPEED_DIRECTORY / f"{lecture_name}.wav",
        )

        # add captions to the video file
        file_handler.merge_video_and_captions(
            VIDEO_DEST_DIRECTORY / f"{lecture_name}.mp4",
            CAPTIONS_DIRECTORY / f"{lecture_name}.vtt",
        )

        rtpt.step()


if __name__ == "__main__":
    main()
