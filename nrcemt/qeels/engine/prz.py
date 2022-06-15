import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt


# SHOULD I RENAME TO read() SIMILAR TO IN dm3.py


def read_prz(file_path):
    spectrogram=np.load(file_path, allow_pickle=True)
    return spectrogram
