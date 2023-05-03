import os
import whisper
import logging

logging.basicConfig(level=logging.INFO)

class Whisper:

    def __init__(self, model = "large-v1"):
        self.model =  whisper.load_model(model)

    def get_text(self,audio_file_path):
        result = self.model.transcribe(audio_file_path)
        return result['text']