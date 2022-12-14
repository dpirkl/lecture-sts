FROM debian:sid-slim

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /tst

COPY . /tst

WORKDIR /tst

RUN python3 -m venv lecture_sts

# RUN git clone "https://github.com/dpirkl/lecture-sts.git"

RUN source lecture_sts/bin/activate && \
    pip install -r lecture-sts/requirements.txt

RUN python3 setup.py

ENTRYPOINT [ "python3", "translate_lecture.py" ]
