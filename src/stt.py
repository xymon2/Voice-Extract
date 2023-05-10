import os
import whisper
import logging
import common

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("STT")

class Whisper:

    def __init__(self, model = "large-v1"):
        self.logger = logger
        self.logger.info("Loading whisper model - %s", model)
        self.model =  whisper.load_model(model)
        self.logger.info("Whisper model is loaded - %s", model)


    def get_text(self,audio_path):
        # for audio file paht
        result = self.model.transcribe(audio_path)
        # for raw audio - bytes
        # result = self.model.transcribe_audio(audio_path, raw_audio=True)
        return result['text']
    
    def text_to_mlt_csv_format(self, text, emotion, model, path):
        # ex. "CHIM|오히려좋아|자유|dummy_CHIM/raw_audio/CHIM/CHIM/clip_0.wav"
        return [
            f"{model}",
            f"{text}",
            f"{emotion}",
            f"dummy_{model}/raw_audio/{model}/{model}/{os.path.basename(path)}"
        ]

if __name__ == "__main__":
    
    import csv
    import re

    tts_model = common.tts_model

    # To remove leading spaces of whisper.
    # For ex) - " hello world! -> "hello world!"
    def remove_leading_spaces(text):
        pattern = r"^\s+"  
        replacement = "" 
        return re.sub(pattern, replacement, text)

    # Check other langauges in text
    def has_other_languages(text):
        # regex pattern to match non-Korean characters, numbers and punctuation.
        pattern = r"[^ㄱ-ㅎㅏ-ㅣ가-힣0-9\s!\"#$%&'()*+,-./:;<=>?@\[\]^_`{|}~\\]"
        return bool(re.search(pattern, text))

    logger.info("STT is started")
    whisper = Whisper("large-v1")
    audio_clips = common.get_all_wav_file_in_paths(f"/output/{tts_model}/raw/raw_audio/{tts_model}/{tts_model}")

    print("Start to edit csv")
    emotion_list = ["자유", "중립", "기쁨", "친절", "분노", "짜증", "약한분노","울부짖음", "울먹임", "놀람", "공포", "속삭임", "힘없는", "취한"]
    idx = 0
    with open(f'/output/{tts_model}/raw/raw_samples.csv', mode='w', newline='',encoding='utf-8') as file:
        writer = csv.writer(file,delimiter='|')
        writer.writerow(["speaker","text","emotion","audio_path"])
        for audio in audio_clips :
            text = remove_leading_spaces(whisper.get_text(audio))
            if has_other_languages(text):
                continue
            logger.info("%s:%s",audio,text)
            row =whisper.text_to_mlt_csv_format(text,"자유",tts_model,audio)
            writer.writerow(row)

            # print(f"Please listen audio: {audio}")
            # while True:
            #     emotion = input("D to delete or input a emotion of this file:")
            #     if emotion == "D":
            #         break
            #     elif emotion in emotion_list:
            #         row =whisper.text_to_mlt_csv_format(text,emotion,tts_model,audio)
            #         writer.writerow(row)
            #         idx+=1
            #         break
            #     else:
            #         print("Invalid input")

    logger.info("%i data are written in csv", idx)
    logger.info("STT is done")