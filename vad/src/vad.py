from pyannote.audio import Pipeline
from pydub import AudioSegment
import logging
import boto3
import os
from random import randint


S3_BUCKET = "mltmaker"

class VAD():
    def __init__(self, ):
        self.logger = logging.getLogger("[VAD-PROCESSOR]")
        self.s3_client = boto3.client('s3')
        self.pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection",
                                            use_auth_token="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")


    async def make_voice_segments(self, s3_audio_path, min_duration, max_duration):

        rand = randint(0, 10000000)
       
        self.logger.info("Download File - %s", s3_audio_path)
        self.s3_client.download_file(S3_BUCKET, s3_audio_path, f"{rand}.wav")
        self.logger.info("VAD is started - %s", s3_audio_path)
        output=self.pipeline(f"{rand}.wav")
        
        whole_audio = AudioSegment.from_file(f"{rand}.wav", format="wav")
        dir = os.path.dirname(s3_audio_path)

        i = 0
        self.logger.info(f"Uploading voice clips")
        for speech in output.get_timeline().support():
            if speech.duration < min_duration:
                continue

            elif speech.duration > max_duration:
                end = speech.start + max_duration
                start = speech.start
                while end < speech.duration:
                    self.clip_audio_file(whole_audio, start, end, f"{rand}_{i}.wav")
                    self.s3_client.upload_file(f"{rand}_{i}.wav", S3_BUCKET, f"{dir}/clips/clip_{i}.wav")
                    self.logger.info(f"clip_{i}.wav")
                    i += 1
                    start = end
                    end = min(start + max_duration, speech.duration)

            else:
                self.clip_audio_file(whole_audio, speech.start, speech.end, f"{rand}_{i}.wav")
                self.s3_client.upload_file(f"{rand}_{i}.wav", S3_BUCKET, f"{dir}/clips/clip_{i}.wav")
                self.logger.info(f"clip_{i}.wav")
                i += 1

        for i in range(i):
            os.remove(f"{rand}_{i}.wav")
        self.logger.info(f"All {i-1} voice clips are uploaded")
        return
    
    def clip_audio_file(self, audio_file, start, end, export_path):
        segment_audio = audio_file[start * 1000:end * 1000]
        segment_audio = segment_audio.set_channels(1)
        segment_audio.export(export_path,format="wav")
        return

