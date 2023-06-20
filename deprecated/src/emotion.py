import torch
import torch.nn as nn
import torch.nn.functional as F
import torchaudio
from transformers import Wav2Vec2Processor, Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification
import librosa

class EmotionRecognizer:
    def __init__(self) -> None:

        # load the model and the processor
        model_name = "jungjongho/wav2vec2-xlsr-korean-speech-emotion-recognition2_data_rebalance"
        feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(model_name)
        self.sampling_rate = feature_extractor.sampling_rate
        self.model = Wav2Vec2ForSequenceClassification.from_pretrained(model_name)
        self.processor = Wav2Vec2Processor.from_pretrained(model_name)

        # self.model = Wav2Vec2ForSpeechEmotionRecognition.from_pretrained(model_name)
    def emotion_recognize(self, audio_segment):
        preprocessed_audio = librosa.load(audio_segment, sr=self.sampling_rate)
        input_values = self.processor(preprocessed_audio, return_tensors="pt", sampling_rate=16_000).input_values
        logits = self.model(input_values).logits
        predicted_class = torch.argmax(logits, dim=1)

        emotion_labels = ["neutral", "happy", "sad", "angry", "fearful", "disgusted", "surprised"]

# Print the predicted emotion
        print("Predicted emotion:", emotion_labels[predicted_class.item()])
        # input_dict = self.processor(preprocessed_audio, sampling_rate=16000, return_tensors="pt", padding=True)

        # # make a prediction
        # outputs = self.model(**input_dict)
        # predicted_label = self.processor.batch_decode(outputs.logits.argmax(axis=-1))[0]
        # print(predicted_label) 

    # def speech_file_to_array_fn(self,audio):
    #     speech_array, _sampling_rate = torchaudio.load(audio)
    #     resampler = torchaudio.transforms.Resample(self.sampling_rate)
    #     speech = resampler(speech_array).squeeze().numpy()
    #     return speech
    
    # def predict(self, audio, sampling_rate):
    #     speech = self.speech_file_to_array_fn(path, sampling_rate)
    #     inputs = self.feature_extractor(speech, sampling_rate=sampling_rate, return_tensors="pt", padding=True)
    #     inputs = {key: inputs[key].to(device) for key in inputs}
    #     with torch.no_grad():
    #         logits = model(**inputs).logits
    #     scores = F.softmax(logits, dim=1).detach().cpu().numpy()[0]
    #     outputs = [{"Emotion": config.id2label[i], "Score": f"{round(score * 100, 3):.1f}%"} for i, score in enumerate(scores)]
    #     return outputs




# load and preprocess the audio file
