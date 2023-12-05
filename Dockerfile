FROM download.pytorch.org/whl/cu118
# FROM nvcr.io/nvidia/pytorch:22.12-py3

# To avoid tzdata asking for user input.
# There are also solutions that point to installing tzdata directly.
# To avoid this issue, I went with both solutions.
ARG DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    tzdata \
    python3 \
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

WORKDIR /project

# Install requirements to perform the translation
RUN pip install -r requirements.txt

# Creates the necessary folders and downloads the models
RUN python3 setup.py
