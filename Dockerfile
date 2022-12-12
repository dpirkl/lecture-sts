FROM python:alpine
COPY . /app
WORKDIR /app

# set up virtual environment and install (pip) requirements
RUN python3 -m venv lecture_sts
RUN source lecture_sts/bin/activate
RUN pip install -r requirements.txt

# install ffmpeg
RUN sudo apt update
RUN sudo apt install ffmpeg
RUN ffmpeg -version

# create the folders for data storage
RUN python3 setup.py

# translate the lecture
CMD [ "python3", "translate_lecture.py" ]