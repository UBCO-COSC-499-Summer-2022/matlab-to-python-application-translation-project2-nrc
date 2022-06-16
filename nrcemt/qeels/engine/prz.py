import numpy as np


def load_prz(file_path):
    spectrogram = np.load(file_path, allow_pickle=True)
    return spectrogram['data']


def process_prz(spectrogram):
    spectrogram = np.log(spectrogram+1)
    return spectrogram
