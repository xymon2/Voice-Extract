# 3.10.11 - linux/amd64 - 230525
FROM python@sha256:fc1d7d6e1df26c603b5729e92fff684a56e9d1b8c6db263c6169a1f250e80787

RUN apt-get update
RUN apt-get install -y ffmpeg 

COPY api/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY api/src ./src
COPY proto/ ./

RUN python3 -m grpc_tools.protoc -I=./ --python_out=./src --grpc_python_out=./src ./vad.proto

CMD ["python3", "/src/main.py"]
