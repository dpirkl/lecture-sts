FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime
# FROM nvcr.io/nvidia/pytorch:22.12-py3
# used pytorch docker image by pytorch https://hub.docker.com/r/pytorch/pytorch/tags

# To avoid tzdata asking for user input.
# There are also solutions that point to installing tzdata directly.
# To avoid this issue, I went with both solutions.
ARG DEBIAN_FRONTEND=noninteractive

# Install deadsnakes repository for Python 3.11 Installation
RUN add-apt-repository ppa:deadsnakes/ppa
# Install dependencies
RUN apt-get update && apt-get install -y \
    tzdata \
    python3.11 \
    python3-pip \
    git \
    vim \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Clone the repository and move all files to the project folder
WORKDIR /

RUN mkdir project

RUN git clone https://github.com/OrbitPeppermint/lecture-sts.git

RUN mv lecture-sts/* project/

RUN rm -r lecture-sts

# added  for seamlessm4t installation
RUN git clone https://github.com/facebookresearch/seamless_communication.git


WORKDIR /project

# Install requirements to perform the translation
RUN pip install -r requirements.txt

# added for seamlessm4t
#UN pip install -r dev_requirements.txt

# Install latest Whisper Version
RUN pip install -U openai-whisper


# Upgrade pip
# RUN python3 -m pip install --upgrade pip

# Install pytorch and torchvision from https://pytorch.org/
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

#added for Seamlessm4t installation
#RUN pip install .


# Creates the necessary folders and downloads the models
RUN python3 setup.py
