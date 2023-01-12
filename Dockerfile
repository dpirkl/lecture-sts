FROM nvcr.io/nvidia/pytorch:latest

# install python, ffmpeg and git
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    vim \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*


RUN git clone https://github.com/dpirkl/lecture-sts.git

RUN mv lecture-sts/* project/

# install the requirements
RUN pip install -r requirements.txt
