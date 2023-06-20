from sanic_restful_api import Resource
from sanic.response import json
import yt_dlp
import boto3
import os
from logdeco import httplog

S3_BUCKET = "mltmaker"

class YoutubeResource(Resource):
    @httplog
    async def get(self, request):
        # get list of all videos in model.
        model = request.json['model']
        return json({'hello': 'world?!'})
    
    @httplog
    async def post(self, request): 
        # upload the video to s3. 
        url = request.json['url']
        model = request.json['model']
        ydl_opts = {
            "format": "bestaudio/best",
            'postprocessors': [{ 
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
                'preferredquality': 0,
            }],
            'outtmpl': f"/videos/{model}/%(title)s.%(ext)s"
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info['title']

        s3_client = boto3.client('s3')
        s3_client.upload_file(f"/videos/{model}/{title}.wav", S3_BUCKET, f"{model}/{title}/{title}.wav")
        os.remove(f"/videos/{model}/{title}.wav")

        return 200
    
    @httplog
    async def delete(self, request):
        # delete video
        return json({'hello': 'world.,.'})
    