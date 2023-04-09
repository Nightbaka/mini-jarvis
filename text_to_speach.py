import os
import torch
from scipy.io.wavfile import write
import numpy as np
from IPython.display import Audio, display
from play import play

def speak(text, filename='voice.wav', saved_voice=True):
    device = torch.device('cpu')
    torch.set_num_threads(4)
    local_file = 'model.pt'

    if not os.path.isfile(local_file):
        torch.hub.download_url_to_file('https://models.silero.ai/models/tts/en/v3_en.pt',
                                       local_file)  

    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")
    model.to(device)
    sample_rate = 48000
    speaker='random'
    put_accent=False
    put_yo=True
    voice_path = 'test_voice.pt'
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
    play(filename)

if __name__ == '__main__':
    speak("I am a man and I know what a man should do in this situation. I should go to the store and buy some milk.")