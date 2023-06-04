import torch
import zipfile
import torchaudio
from glob import glob

def listen(soundfile):
    device = torch.device('cpu')  # gpu also works, but our models are fast enough for CPU
    model, decoder, utils = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                       model='silero_stt',
                                       language='en', # also available 'de', 'es'
                                       device=device)
    (read_batch, split_into_batches,
    read_audio, prepare_model_input) = utils  # see function signature for details

    test_files = glob(soundfile)
    batches = split_into_batches(test_files, batch_size=10)
    input = prepare_model_input(read_batch(batches[0]),
                            device=device)

    output = model(input)
    return decoder(output[0])
    

if __name__ == '__main__':
    listen('output.wav')