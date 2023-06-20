from sanic_restful_api import Resource
from sanic.response import json

import grpc
import vad_pb2
import vad_pb2_grpc
import logging
from logdeco import httplog

logger = logging.getLogger("sanic.root")

S3_BUCKET = "mltmaker"
VAD_ADDRESS = "~~~"

class VadResource(Resource):
    @httplog
    async def get(self, request):
        # get vad results from a video
        return json({'hello': 'world?!'})
    
    @httplog
    async def post(self, request):
        # request vad process on video
        path = request.json['path']
        min_duration = request.json['min_duration']
        max_duration = request.json['max_duration']

        with grpc.insecure_channel(VAD_ADDRESS) as channel:
            stub = vad_pb2_grpc.VADStub(channel)
            response = stub.Detect(vad_pb2.DetectRequest(filepath=path, min_duration=min_duration, max_duration=max_duration))
        return json({'hello': 'world.,.'})

    @httplog
    async def delete(self, request):
        # delete a vad result from a video
        return json({'hello': 'world.,.'})