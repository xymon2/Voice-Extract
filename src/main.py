# import vad
# import stt
# import os
# import csv
# import logging
# import re
# import time


# voice_dir = os.getenv("TARGET_VOICE_DIR")
# tts_model = os.getenv("MODEL_NAME")
# min_voice_length = float(os.getenv("MIN_VOICE_LENGTH"))
# max_voice_length = float(os.getenv("MAX_VOICE_LENGTH"))

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("MAIN")

# def get_all_wav_file_in_paths(input_dir):
#     file_paths = []
#     for file in os.listdir(input_dir):
#         if file.endswith(".wav"):
#             file_paths.append(os.path.join(input_dir, file))
#     return file_paths



# if __name__ == "__main__":

#     # Extract voice segments from input audio files
#     logger.info("Start MLT data maker")
#     whisper = stt.Whisper("large")
#     vad = vad.VAD(min_voice_length,max_voice_length)

#     logger.info("VAD is started")
#     paths = get_all_wav_file_in_paths(f"/voices/{voice_dir}")
#     output_dir = f"/voices/{voice_dir}/output"
    
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)

#     segment_list = []
#     for path in paths:
#         segment_list += vad.make_voice_segments(path)
    
#     logger.info("VAD is Done")
    
#     # Make a CSV file to train model with textified speech.
#     logger.info("Start to make a CSV file")
#     paths = get_all_wav_file_in_paths(f"/voices/{voice_dir}/output")

#     idx=0
#     with open(f'/csv/{tts_model}.csv', mode='w', newline='') as file:
#         writer = csv.writer(file,delimiter='|')
#         writer.writerow(["speaker","text","emotion","audio_path"])
#         for audio in segment_list:
#             text = remove_leading_spaces(whisper.get_text(audio))
#             if has_other_languages(text):
#                 continue
#             logger.info(f"{path}-{text}")
#             output_file_path = f"{output_dir}/clip_{idx}.wav"
#             audio.export(output_file_path, format="wav")
#             row = [
#                 f"{tts_model}",
#                 f'"{text}"',
#                 "자유",
#                 f"dummy_{tts_model}/raw_audio/{tts_model}/{tts_model}/{os.path.basename(path)}"
#             ]
#             writer.writerow(row)
#             idx+=1
#     logger.info("Whole %i audio clips are made", idx)
#     logger.info("DONE")