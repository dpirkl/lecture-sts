import argparse
import logging
from pathlib import Path

from rtpt import RTPT
import os
import sys
from src import whisper_wrapper
from utils.file_handler import embed_two_subtitles_in_mp4, get_audio_from_video_file
from utils.path_handler import (
    AUDIO_DIRECTORY,
    ORIGINAL_VIDEO_DIRECTORY,
    ORIGINAL_VIDEO_SUBTITLES_DIRECTORY,
    SUBTITLES_DIRECTORY,
    create_folders,
)


def main(video_directory: str = None, no_cache=False, use_rtpt=True):
    video_directory = video_directory if video_directory else ORIGINAL_VIDEO_DIRECTORY
     
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

        transcriber = whisper_wrapper.Transcriber(model="large")
        result_original = transcriber.transcribe(audio_file, no_cache=no_cache)
        whisper_wrapper.Transcriber.write_srt(
            result=result_original,
            output_dir=str(SUBTITLES_DIRECTORY / f"{name}_original.srt"),
        )
        result_english = transcriber.transcribe_and_translate(
            audio_file, no_cache=no_cache
        )
        whisper_wrapper.Transcriber.write_srt(
            result=result_english,
            output_dir=str(SUBTITLES_DIRECTORY / f"{name}_en.srt"),
        )

        if use_rtpt:
            rtpt.step()

        subtitle_one = str(f"{SUBTITLES_DIRECTORY/name}")
        language_one = "eng"
        subtitle_two = str(f"{SUBTITLES_DIRECTORY/name}")
        language_two = "deu"
        output_path = f"{ORIGINAL_VIDEO_SUBTITLES_DIRECTORY/name}.mp4"
        embed_two_subtitles_in_mp4(
            video_file,
            first_subtitles_file=subtitle_one,
            second_subtitles_file=subtitle_two,
            first_language=language_one,
            second_language=language_two,
            output_path=output_path,
        )

    logging.info("Finished.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "gpu",
        help="Defines on which GPU this process should run, Integer between 0 and 15",
    )
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
    if args.gpu.isdigit() and int(args.gpu) < 16 and int (args.gpu) >= 0:
        os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu
        sys.print("Running Process on GPU " + args.gpu)

    else:
        os.environ['CUDA_VISIBLE_DEVICES'] = '11'
        sys.print("wrong GPU number, default GPU used: 11.")
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
