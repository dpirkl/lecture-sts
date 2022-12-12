"""This module is used to translate the videos."""
from pathlib import Path

import whisper

from src.tts_wrapper import Speaker
from utils import (
    AUDIO_DEST_DIRECTORY,
    AUDIO_DIRECTORY,
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

    # split all videos into audio files and video files without audio
    # audio files are saved in AUDIO_DIRECTORY
    # new video files are saved in VIDEO_DIRECTORY
    for original_video in directory_of_videos.iterdir():
        file_handler.split_video(original_video)

    # load the model
    model = whisper.load_model("tiny")
    options = {"task": "translate", "fp16": False, "beam_size": 5, "best_of": 5}

    # load the synthesizer
    synthesizer = Speaker()

    for audio_file in AUDIO_DIRECTORY.iterdir():
        # transcribe audio file
        lecture_name = audio_file.stem
        result = model.transcribe(str(audio_file), **options)

        # save transcript to a text file
        transcript_path = TRANSCRIPT_DIRECTORY / f"{lecture_name}.txt"
        with open(transcript_path, "w", encoding="UTF-8") as transcript_file:
            whisper.utils.write_txt(result["segments"], file=transcript_file)

        # generate captions
        captions_path_vtt = CAPTIONS_DIRECTORY / f"{lecture_name}.vtt"
        with open(captions_path_vtt, "w", encoding="UTF-8") as vvt:
            whisper.utils.write_vtt(result["segments"], file=vvt)

        """captions_path_srt = CAPTIONS_DIRECTORY / f"{lecture_name}.srt"
        with open(captions_path_srt, "w", encoding="UTF-8") as srt:
            whisper.utils.write_srt(result["segments"], file=srt)
        """

        # synthesize audio file
        translated_audio_path = AUDIO_DEST_DIRECTORY / f"{lecture_name}.wav"
        synthesizer.speak(result["text"], translated_audio_path)

    for audio_file, video_file in zip(
        AUDIO_DEST_DIRECTORY.iterdir(), VIDEO_DIRECTORY.iterdir()
    ):
        # merge audio file and video file
        file_handler.merge_audio_and_video_to_mp4(video_file, audio_file)

    for video_file in VIDEO_DEST_DIRECTORY.iterdir():
        # add captions to video file
        video_name = video_file.stem
        captions_file = CAPTIONS_DIRECTORY / f"{video_name}.vtt"
        file_handler.merge_video_and_captions(video_file, str(captions_file))


if __name__ == "__main__":
    main()
