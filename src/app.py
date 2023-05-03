from pyannote.audio import Pipeline
from pydub import AudioSegment
import logging
import os

logging.basicConfig(level=logging.INFO)
voice_dir = os.getenv("TARGET_VOICE_DIR")

def make_voice_segments(idx, audio_file_path, ):
    # VAD pipeline
    filename = os.path.splitext(os.path.basename(audio_file_path))[0]

    logging.info(f"Start to detect voice activity of a file - {filename}")
    pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection",
                                        use_auth_token="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")
    output = pipeline(audio_file_path)

    logging.info(f"voice activity detection is done - {filename}")

    # Load the input audio file using pydub
    audio = AudioSegment.from_file(audio_file_path, format="wav")
    min_segment_duration = 3.0

    logging.info(f"making segments to actual voice clip - {filename}")

    for i, speech in enumerate(output.get_timeline().support()):
        if speech.duration < min_segment_duration:
            continue

        segment_audio = audio[speech.start * 1000:speech.end * 1000]
        segment_audio = segment_audio.set_channels(1)
        
        output_file_path = f"/voices/{voice_dir}/output/{voice_dir}_{i+idx}.wav"
        segment_audio.export(output_file_path, format="wav")
    
    logging.info(f"{len(output)} audio clips are made - {filename}")

    return i+idx+1