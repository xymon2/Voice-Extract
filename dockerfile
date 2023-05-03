# Use python 3.10
FROM python:3.10

RUN apt-get update
RUN apt-get install ffmpeg libsndfile1 -y 
# # aptget setting to use python and pip commands
# RUN apt-get install -y python3-pip python3-dev


# install from develop branch - pyannote-audio
RUN pip install -qq https://github.com/pyannote/pyannote-audio/archive/refs/heads/develop.zip

# install whisper
RUN pip install git+https://github.com/Blair-Johnson/batch-whisper.git
# # Install all pip pacakges in requirements.txt
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

#Copy source codes in src dir
COPY src /src

# run main.py in src
CMD ["python", "/src/main.py"]
