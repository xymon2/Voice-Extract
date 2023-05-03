import app
import stt
import os
import csv

#Env var
voice_dir = os.environ["VOICE_DIR"]
tts_model = os.environ["MODEL_NAME"]
# a function returning all paths of wav extension file inside of input directory
def get_all_wav_file_paths(input_dir):
    file_paths = []
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".wav"):
                file_paths.append(os.path.join(root, file))
    return file_paths


if __name__ == "__main__":

    # Extract voice segments from input audio files
    paths = get_all_wav_file_paths(f"/voices/{voice_dir}")
    os.makedirs(f"/voices/{voice_dir}/output")
    idx = 0
    for path in paths:
        idx = app.make_voice_segments(idx, path)
    

    # Make a CSV file to train model with textified speech.
    whisper = stt.Whisper("large-v1")
    paths = get_all_wav_file_paths(f"/voices/{voice_dir}/output")
    with open(f'/csv/{tts_model}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["speaker|text|emotion|audio_path"])
        for path in paths:
            writer.writerow([f"{tts_model}|{whisper.get_text(path)[1:]}|자유|dummy_{tts_model}/raw_audio/{tts_model}/{tts_model}/{os.path.basename(path)}"])




