import torch
from glob import glob
from scipy.io.wavfile import write
import os
import speech_recognition as sr
from abc import ABC

class ISpeechInterface(ABC):
    def to_text(self,filename = None):
        pass

    def to_speach(self,text, filename = None):
        pass
    
class SpeechInterface(ISpeechInterface):

    def __init__(self, sound_input, sound_output):
        self.sound_input = sound_input
        self.sound_output = sound_output

    
    def to_speach(self, text, filename = None, saved_voice=True, model_path= "./models/ts_model.pt"):
        if filename is None:
            filename = self.sound_output
        print("text to speech")
        device = torch.device('cpu')
        torch.set_num_threads(4)
        local_file = model_path

        model_url = 'https://models.silero.ai/models/tts/en/v3_en.pt'

        if not os.path.isfile(local_file):
            torch.hub.download_url_to_file(model_url,
                                        local_file)  

        model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
        model.to(device)
        sample_rate = 48000
        speaker='random'
        put_accent=False
        put_yo=True
        voice_path = './models/test_voice.pt'
        if saved_voice:
            audio = model.apply_tts(text=text,
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo,
                            voice_path = voice_path
                            )
        else:
            audio = model.apply_tts(text=text,
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yo,
                            )
            model.save_random_voice(voice_path)
        audio_np = audio.numpy()
        write(filename, sample_rate, audio_np)
        print("done text to speech")

    
    def to_text(self,filename = None):
        if filename is None:
            filename = self.sound_input
        recognizer = sr.Recognizer()
        audio = sr.AudioFile(filename)
        with audio as source:
            audio = recognizer.record(source)
            return recognizer.recognize_google(audio)