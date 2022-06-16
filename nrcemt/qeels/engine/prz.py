import numpy as np
import matplotlib.pyplot as plt

def load_prz(file_path):
    spectrogram = np.load(file_path, allow_pickle=True)
    render_prz(spectrogram['data'])
    return spectrogram['data']


def render_prz(spectrogram):
    # temporary solution for displaying image
    plt.axes([0.25, 0.25, 0.6, 0.6]).set_axis_off()
    plt.imshow(np.log(spectrogram+1))
    plt.show()
