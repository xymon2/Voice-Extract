# Use NVIDIA CUDA base image
FROM nvidia/cuda:11.4.2-runtime-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    ffmpeg \
    libsndfile1 \
    git

RUN pip install setuptools-rust

# # Install all pip pacakges in requirements.txt
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

# install from develop branch - pyannote-audio
RUN pip install -qq https://github.com/pyannote/pyannote-audio/archive/refs/heads/develop.zip

# install whisper
RUN pip install git+https://github.com/Blair-Johnson/batch-whisper.git

#Copy source codes in src dir
COPY src /src

# run main.py in src
CMD ["python3", "/src/main.py"]
