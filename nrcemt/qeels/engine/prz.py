import numpy as np


def load_prz(file_path):
    spectrogram = np.load(file_path, allow_pickle=True)
    return spectrogram['data']
