from pyannote.audio import Pipeline
from pydub import AudioSegment
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("VAD")

class VAD():
    def __init__(self, min_length:float = 3.0, max_length:float = 20.0):
        self.min_length = min_length
        self.max_length = max_length
        self.logger = logger
        
    def make_voice_segments(self, audio_file_path):
        filename = os.path.splitext(os.path.basename(audio_file_path))[0]

        self.logger.info("Start to detect voice activity of a file - %s", filename)
        pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection",
                                            use_auth_token="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")
        output = pipeline(audio_file_path)
        self.logger.info("voice activity detection is done - %s", filename)

        # Load the input audio file.
        whole_audio = AudioSegment.from_file(audio_file_path, format="wav")
        min_segment_duration = 3.0
        self.logger.info("making the segments as actual voice clips - %s",filename)

        audio_segment_list = []
        for speech in output.get_timeline().support():
            if speech.duration < min_segment_duration or speech.duration > self.max_length:
                continue

            segment_audio = whole_audio[speech.start * 1000:speech.end * 1000]
            audio_segment_list.append(segment_audio)

        return audio_segment_list
    
if __name__ == "__main__":

    voice_dir = os.getenv("TARGET_VOICE_DIR")
    tts_model = os.getenv("MODEL_NAME")
    min_voice_length = float(os.getenv("MIN_VOICE_LENGTH"))
    max_voice_length = float(os.getenv("MAX_VOICE_LENGTH"))

    def get_all_wav_file_in_paths(input_dir):
        file_paths = []
        for file in os.listdir(input_dir):
            if file.endswith(".wav"):
                file_paths.append(os.path.join(input_dir, file))
        return file_paths
    

    logger.info("VAD is started")
    vad = VAD(min_voice_length,max_voice_length)
    paths = get_all_wav_file_in_paths(f"/voices/{voice_dir}")
    output_dir = f"/output/{tts_model}/raw/raw_audio/{tts_model}/{tts_model}"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    segment_list = []
    for path in paths:
        segment_list += vad.make_voice_segments(path)

    for idx, audio in enumerate(segment_list):
        output_file_path = f"{output_dir}/clip_{idx}.wav"
        audio = audio.set_channels(1)
        audio.export(output_file_path, format="wav")
    
    logger.info("Whole %i audio clips are made", idx)
    logger.info("VAD is DONE")