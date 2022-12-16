FROM nvcr.io/nvidia/pytorch:22.06-py3

# install python, ffmpeg and git
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# create a directory for the project
RUN mkdir /tst

# copy the project into the container
COPY . /tst

# set the working directory to the project directory
WORKDIR /tst

# install the requirements
RUN pip install -r requirements.txt

# create a folder structure for the audio and video files
RUN python3 setup.py
