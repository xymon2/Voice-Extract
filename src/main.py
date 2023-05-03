import app
import stt
import os
import csv
import logging

voice_dir = os.getenv("TARGET_VOICE_DIR")
tts_model = os.getenv("MODEL_NAME")
logging.basicConfig(level=logging.INFO)

def get_all_wav_file_paths(input_dir):
    file_paths = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".wav"):
                file_paths.append(os.path.join(root, file))
    return file_paths

if __name__ == "__main__":

    # Extract voice segments from input audio files
    logging.info("VAD is started")
    paths = get_all_wav_file_paths(f"/voices/{voice_dir}")
    output_dir = f"/voices/{voice_dir}/output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    idx = 0
    for path in paths:
        idx = app.make_voice_segments(idx, path)
    logging.info("VAD is Done")
    
    # Make a CSV file to train model with textified speech.
    whisper = stt.Whisper("large-v1")
    logging.info("Start to make a CSV file")
    paths = get_all_wav_file_paths(f"/voices/{voice_dir}/output")

    with open(f'/csv/{tts_model}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["speaker|text|emotion|audio_path"])
        for path in paths:
            text = whisper.get_text(path)[1:]
            logging.info(f"{path}-{text}")
            row = [
                f"{tts_model}",
                f'"{text}"',
                "자유",
                f"dummy_{tts_model}/raw_audio/{tts_model}/{tts_model}/{os.path.basename(path)}"
            ]
            writer.writerow(row)
    logging.info("DONE")