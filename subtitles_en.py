import argparse
import logging
import os
from pathlib import Path

from rtpt import RTPT

from src import whisper_wrapper
from utils.file_handler import embed_subtitles_in_mp4, get_audio_from_video_file
from utils.path_handler import (
    AUDIO_DIRECTORY,
    ORIGINAL_VIDEO_DIRECTORY,
    ORIGINAL_VIDEO_SUBTITLES_DIRECTORY,
    SUBTITLES_DIRECTORY,
    create_folders,
)


def main(video_directory: str = None, no_cache=False, use_rtpt=False):
    video_directory = video_directory if video_directory else ORIGINAL_VIDEO_DIRECTORY
    os.environ['CUDA_VISIBLE_DEVICES'] = '1'
    if use_rtpt:
        rtpt = RTPT(
            name_initials="DP",
            experiment_name="Translate_Lecture:_Intro_to_AI",
            max_iterations=len(list(Path(video_directory).iterdir())),
        )
        rtpt.start()

    create_folders()

    for video in video_directory.iterdir():
        name = video.stem
        video_file = ORIGINAL_VIDEO_DIRECTORY / f"{name}.mp4"
        audio_file = str(AUDIO_DIRECTORY / f"{name}.wav")
        get_audio_from_video_file(video_file=video_file, output_path=audio_file)

        logging.info(name)

        transcriber = whisper_wrapper.Transcriber(model="large")
        result_english = transcriber.transcribe_and_translate(
            audio_file, no_cache=no_cache
        )
        whisper_wrapper.Transcriber.write_srt(
            result=result_english, output_dir=str(SUBTITLES_DIRECTORY / f"{name}.srt")
        )

        embed_subtitles_in_mp4(
            video_file,
            str(SUBTITLES_DIRECTORY / f"{name}.srt"),
            language="eng",
            output_path=str(ORIGINAL_VIDEO_SUBTITLES_DIRECTORY / f"{name}.srt)"),
        )

        if use_rtpt:
            rtpt.step()

    logging.info("Finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity to logging lever INFO",
        action="store_true",
    )
    parser.add_argument(
        "-disable_rtpt",
        "--disable_rtpt",
        help="use RTPT to show the remaining time of the process",
        action="store_true",
    )
    parser.add_argument(
        "-no_cache",
        "--no_cache",
        help="disable the use of stored translation results",
        action="store_true",
    )

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.disable_rtpt:
        use_rtpt = False
    else:
        use_rtpt = True
    if args.no_cache:
        no_cache = True
    else:
        no_cache = False

    main(use_rtpt=use_rtpt, no_cache=no_cache)
