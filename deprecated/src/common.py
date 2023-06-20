import os

voice_dir = os.getenv("TARGET_VOICE_DIR")
tts_model = os.getenv("MODEL_NAME")

def get_all_wav_file_in_paths(input_dir):
    file_paths = []
    for file in os.listdir(input_dir):
        if file.endswith(".wav"):
            file_paths.append(os.path.join(input_dir, file))
    return file_paths

