import numpy as np


def load_spectrogram(file_path):
    """Loads the data from the prz file from provied file_path"""
    spectrogram = np.load(file_path, allow_pickle=True)
    return spectrogram['data']


def process_spectrogram(spectrogram):
    """Performs basic processing on provided array"""
    spectrogram = np.log(np.absolute(spectrogram+1))
    return spectrogram
