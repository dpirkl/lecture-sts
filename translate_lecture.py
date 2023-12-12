"""This module is used to translate the videos."""
import argparse
import logging
from pathlib import Path

from rtpt import RTPT
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '11'

from src.silence import Silence
from src.speaker import SegmentsSpeaker
from src.whisper_wrapper import Transcriber
from utils import file_handler
from utils.path_handler import (
    AUDIO_DIRECTORY,
    AUDIO_TRANSLATED_SPEED_DIRECTORY,
    ORIGINAL_VIDEO_DIRECTORY,
    SUBTITLES_DIRECTORY,
    VIDEO_DEST_DIRECTORY,
    VIDEO_DIRECTORY,
    VIDEO_SUBTITLES_DIRECTORY,
    create_folders,
)


def main(
    max_segment_duration: int,
    video_directory: Path = ORIGINAL_VIDEO_DIRECTORY,
    use_rtpt: bool = True,
    use_cuda: bool = True,
    no_cache=False
):
    """This function is the main function of the program. It is called when the program is executed.
    It is responsible for the whole process of translating a lecture.
    Steps:
    - split all videos into audio files and video files without audio
    - translate and transcribe the audio files
    - generate subtitles and text files
    - synthesize the audio files
    - merge the audio files and the video files
    - merge the video files and the subtitles
    """

    logging.info(
        f"Starting the translation process for all videos in {video_directory}."
    )

    if use_rtpt:
        logging.debug("Initializing and starting the RTPT process.")
        rtpt = RTPT(
            name_initials="DP",
            experiment_name="Translating:IntroAI",
            max_iterations=len(list(video_directory.iterdir())),
        )

        rtpt.start()

    create_folders()

    for original_video in video_directory.iterdir():
        lecture_name = original_video.stem

        # if there is a video with the same name in VIDEO_SUBTITLES_DIRECTORY , skip this video
        if (VIDEO_DEST_DIRECTORY / f"{lecture_name}.mp4").exists():
            logging.warning(
                f"{lecture_name}: Skipped, since a video with the same name exists at {VIDEO_SUBTITLES_DIRECTORY}."
            )
            if use_rtpt:
                rtpt.step()
            continue

        logging.info(lecture_name)

        file_handler.split_video(str(original_video))

        # If the audio file has already been transcribed, this method uses the stored results.
        transcriber = Transcriber(model="large", fp16_settings=True)
        result = transcriber.transcribe_and_translate(
            str(AUDIO_DIRECTORY / f"{lecture_name}.wav"), no_cache=no_cache
        )

        # Write the subtitle file
        Transcriber.write_srt(
            result=result, output_dir=str(SUBTITLES_DIRECTORY / f"{lecture_name}.srt")
        )

        # Prepare the results for tts
        segments = Silence.add_silence_segments_pydub_whisper(
            result["segments"],
            AUDIO_DIRECTORY / f"{lecture_name}.wav",
            max_duration=max_segment_duration,
        )

        # Synthesize the results
        speaker = SegmentsSpeaker(lecture_name=lecture_name, segments=segments)
        speaker.speak(use_gpu=use_cuda)

        # Merge audio and video file.
        file_handler.merge_audio_and_video_to_mp4(
            video_file=str(VIDEO_DIRECTORY / f"{lecture_name}.mp4"),
            audio_file=str(AUDIO_TRANSLATED_SPEED_DIRECTORY / f"{lecture_name}.wav"),
            output_path=str(VIDEO_DEST_DIRECTORY / lecture_name) + ".mp4",
        )

        # Embed the subtitles in the video
        file_handler.embed_subtitles_in_mp4(
            video_file=VIDEO_DEST_DIRECTORY / f"{lecture_name}.mp4",
            subtitles_file=SUBTITLES_DIRECTORY / f"{lecture_name}.srt",
            output_path=str(VIDEO_SUBTITLES_DIRECTORY / lecture_name) + ".mp4",
            language="eng",
        )

        logging.info(f"{lecture_name}: Finished.")

        if use_rtpt:
            rtpt.step()

    logging.info(f"Finished processing all videos in {video_directory}.")


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
        "-disable_cuda",
        "--disable_cuda",
        help="disable CUDA for the text-to-speech synthesizer",
        action="store_true",
    )
    parser.add_argument(
        "-max_segment_duration",
        "--max_segment_duration",
        help="specify the maximum duration of the segments",
    )
    parser.add_argument(
        "-disable_max_duration",
        "--disable_max_duration",
        help="disable the maximum duration for segments",
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
        os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu,
         print("Running Process on GPU " + args.gpu)

    else:
        os.environ['CUDA_VISIBLE_DEVICES'] = '11',
        print("wrong GPU number, default GPU used: 11.")
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    if args.disable_rtpt:
        use_rtpt = False
    else:
        use_rtpt = True
    if args.disable_cuda:
        use_cuda = False
    else:
        use_cuda = True
    if args.max_segment_duration:
        max_segment_duration = args.max_segment_duration
    else:
        max_segment_duration = 30
    if args.disable_max_duration:
        max_segment_duration = None
    if args.no_cache:
        no_cache = True
    else:
        no_cache = False

    main(
        max_segment_duration=max_segment_duration,
        use_rtpt=use_rtpt,
        use_cuda=use_cuda,
        no_cache=no_cache,
    )
