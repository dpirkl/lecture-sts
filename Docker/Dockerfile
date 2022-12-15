FROM debian:sid-slim

# install python, ffmpeg and git
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

# create a directory for the project
RUN mkdir /tst

# copy the project into the container
COPY . /tst

# set the working directory to the project directory
WORKDIR /tst

# create a virtual environment and install the requirements
RUN python3 -m venv lecture_sts

# RUN git clone "https://github.com/dpirkl/lecture-sts.git"

RUN source lecture_sts/bin/activate && \
    pip install -r lecture-sts/requirements.txt


# create a folder structure for the audio and video files
RUN python3 setup.py

# set the entrypoint to the python script
ENTRYPOINT [ "python3", "translate_lecture_iteratively.py" ]
