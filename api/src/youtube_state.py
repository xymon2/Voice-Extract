from sanic_restful_api import Resource
from sanic.response import json
from logdeco import httplog

class YotubeStateResource(Resource):
    @httplog
    async def get(self, request):
        # get the status of youtube vad process.
        return json({'hello': 'world?!'})
    
    @httplog
    async def post(self, request):
        # update the status of youtube vad.
        status = request.json['status']
        filePath = request.json['filePath']
        return json({'hello': 'world.,.'})