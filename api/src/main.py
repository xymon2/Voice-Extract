import sys
from sanic import Sanic, response
from sanic.response import text, json
from sanic.exceptions import NotFound
from sanic_restful_api import reqparse, abort, Api, Resource
from youtube import YoutubeResource
from vad import VadResource
import logging

app = Sanic(__name__)
api = Api(app)
logger = logging.getLogger(__name__)

@app.route("/")
async def home(request):
    return text("Hello, world!")

@app.exception(NotFound)
async def default_handler(request, u_path):
    return text("404 - Not Found")

@app.exception(Exception)
async def server_error_handler(request, exception):
    logger.error("Exception: %s" % exception)
    return response.text("Internal Server Error", status=500)

api.add_resource(YoutubeResource, '/youtubes')
api.add_resource(VadResource, '/vad')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
