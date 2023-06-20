import vad_pb2
import vad_pb2_grpc
import grpc
from concurrent import futures
import logging  
from vad import VAD
import asyncio
import signal
from logdeco import log
import requests


logger = logging.getLogger("[VAD-MAIN]")
PORT = 8001

class VADServicer(vad_pb2_grpc.VADServicer):
    def __init__(self, ):
        self.vad = VAD()

    @log
    async def Detect(self, request, context):
        asyncio.create_task(self.vad_update_request(request.filepath, request.min_duration, request.max_duration))
        return vad_pb2.DetectResponse(status="ok")

    
    async def vad_update_request(self, filepath, min_duration, max_duration):
        try:
            await self.vad.make_voice_segments(filepath, min_duration, max_duration)
            # requests.post('url')
            return
        except Exception as e:
            logger.error(e)
            # requests.post('url')
            return

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    vad_pb2_grpc.add_VADServicer_to_server(VADServicer(), server)
    server.add_insecure_port(f'[::]:{PORT}')
    await server.start()
    logger.info(f"grpc server start - port: {PORT}")

    shutdown = asyncio.Event()
    loop = asyncio.get_event_loop()
    for sig in ('SIGINT', 'SIGTERM'):
        loop.add_signal_handler(getattr(signal, sig), shutdown.set)
    
    await shutdown.wait()
    await server.stop(grace=None)
    logger.info(f"grpc server stop")

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(name)s [%(asctime)s] %(message)s',
                    level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S')
    asyncio.run(serve())
