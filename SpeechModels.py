import torch
from glob import glob
from scipy.io.wavfile import write
import os
from dotenv import load_dotenv

class SpeechModels:
    

    @staticmethod
    def to_text(filename):
        device = torch.device('cpu')
        model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                        model='silero_stt',
                                        language='en',
                                        device=device)
        (read_batch, split_into_batches,
        read_audio, prepare_model_input) = utils

        test_files = glob(filename)
        batches = split_into_batches(test_files, batch_size=10)
        input = prepare_model_input(read_batch(batches[0]),
                                device=device)

        output = model(input)
        return decoder(output[0])
    
    @staticmethod
    def to_speech(text, filename, saved_voice=True, model_path= "./models/ts_model.pt"):
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

if __name__ == '__main__':
    #print(SpeechModels.to_text())
    device = torch.device('cpu')  # gpu also works, but our models are fast enough for CPU
    model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                        model='silero_stt',
                                        language='en', # also available 'de', 'es'
                                        device=device)
    (read_batch, split_into_batches,
    read_audio, prepare_model_input) = utils  # see function signature for details

    # download a single file in any format compatible with TorchAudio
    torch.hub.download_url_to_file('https://opus-codec.org/static/examples/samples/speech_orig.wav',
                                dst ='speech_orig.wav', progress=True)
    test_files = glob('speech_orig.wav')
    batches = split_into_batches(test_files, batch_size=10)
    input = prepare_model_input(read_batch(batches[0]),
                                device=device)

    output = model(input)
    for example in output:
        print(decoder(example.cpu()))