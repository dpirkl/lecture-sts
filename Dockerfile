FROM nvcr.io/nvidia/pytorch:22.06-py3

# install python, ffmpeg and git
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    ffmpeg \
    git \
    && rm -rf /var/lib/apt/lists/*


RUN cd /root \
    && git clone https://github.com/dpirkl/lecture-sts.git

# install the requirements
RUN pip install -r requirements.txt
