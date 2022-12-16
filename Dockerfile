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

# create a virtual environment  
RUN python3 -m venv lecture_sts


# install the requirements
RUN /lecture_sts/bin/pip install -r requirements.txt


# create a folder structure for the audio and video files
RUN /lecture_sts/bin/python setup.py

# set the entrypoint to the python script
ENTRYPOINT [ "/lecture_sts/bin/python", "translate_lecture_iteratively.py" ]
