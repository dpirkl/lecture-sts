# Lecture STS

**S**peech\
**T**ranslation\
**S**ynthesis of Speech

---

This repository can be used to translate any video to english. It uses [OpenAI's whisper](https://github.com/openai/whisper) to transcribe and translate the video. Then it uses [coqui AI's TTS](https://github.com/coqui-ai/TTS) to synthesize the translated transcription. Finally, it combines subtitles and the translated audio with the video.

It was originally built to translate the lectures and exercises of [Introduction to AI](https://www.tucan.tu-darmstadt.de/scripts/mgrqispi.dll?APPNAME=CampusNet&PRGNAME=COURSEDETAILS&ARGUMENTS=-N000000000000001,-N000662,-N0,-N382005038576888,-N382005038510889,-N0,-N0,-N0) in the winter term of 2022/23 at [Technische Universität Darmstadt](https://www.tu-darmstadt.de/).

The course is offered by the [Artificial Intelligence and Machine Learning Lab](https://ml-research.github.io/).

Please contact me if you have any suggestions [david.pirkl@stud.tu-darmstadt.de](mailto:david.pirkl@stud.tu-darmstadt.de).

## Installation

### Dockerfile

You can use the Dockerfile for a simple build. This takes care of all requirements/dependencies. You might want to change the base image, depending on the machine you are using. You have to configure a shared folder at **/project/data** to access the generated files. A simple command to run the image would be:

```bash
docker run --rm -v local_dir:/project/data --name lecture_sts name_of_your_docker_image:latest
```

### Manual

If you do not want to use docker, you also can perform the steps manually. You need to install:

- Python3
- Pip
- Git
- FFmpeg

  ```bash
  # on MacOS using Homebrew: (https://brew.sh/)
  brew install ffmpeg

  # on Ubuntu/Debian:
  sudo apt update && sudo apt install ffmpeg
  ```

Clone the repository:

```bash
git clone https://github.com/dpirkl/lecture-sts.git
```

Afterwards, move to the **_lecture-sts_** folder and install the python requirements via:

```bash
pip install -r requirements.txt
```

## Information

This translation works best for videos with a lot of speech and few pauses. There is only one voice, so multiple speakers can be confusing. The quality of the translation/transcription is dependent on whisper's performance for the specific language. Check out their [repository](https://github.com/openai/whisper) for more information.

## Usage

You should make sure, you have the correct folder structure. To do this and download the models you can use this command:

```bash
python3 setup.py
```

Move your videos to the **_original-video_** folder.

To translate the audio of the video to english and add subtitles to it, you can run:

```bash
python3 translate_lecture.py {Index of GPU you want to use} [args]
```

Or if you want to keep the original audio and just add english subtitles, run:

```bash
python3 subtitles_en.py {Index of GPU you want to use} [args]
```

Subtitles in english and the original language:

```bash
python3 subtitles_en_original.py {Index of GPU you want to use} [args]
```

### Options/Flags/Args

To see more details of the process, you can add the -v/--verbose flag the command.

```bash
python3 subtitles_en.py {Index of GPU you want to use} -v
```

To disable [rtpt](https://github.com/ml-research/rtpt):

```bash
python3 subtitles_en_original.py {Index of GPU you want to use} --disable_rtpt
```

Whether to use stored whisper results:

```bash
python3 translate_lecture.py {Index of GPU you want to use} --no_cache
```

#### For translate_lecture only

You can control the use of cuda via the --disable cuda flag:

```bash
python3 translate_lecture.py {Index of GPU you want to use} --disable_cuda
```

You can specify the maximum duration of a text segment in seconds for TTS or disable the maximum duration:

```bash
python3 translate_lecture.py {Index of GPU you want to use} --max_segment_duration 30

python3 translate_lecture.py {Index of GPU you want to use} --diable_max_duration
```

## Directory Structure

```
|- data/
    |- audio/
    |- audio-translated/
    |- audio-translated-speed/
    |- subtitles/                   (subtitle files are saved here)
    |- variables/                   (to avoid reprocessing)
    |- video-original/              (where the original videos go)
    |- video-original-subtitles/    (original videos with subtitles)
    |- video-translated/            (translated videos without subtitles)
    |- video-translated-subtitles   (translated videos with subtitles)
    |- video-without-audio/
|- src/
    |- silence.py
    |- tts_wrapper.py
    |- whisper_wrapper.py
|- utils
    |- file_handler.py
    |- path_handler.py
|- setup.py
|- subtitles_en.py
|- subtitles_en_original.py
|- translate_lecture.py
...
```
