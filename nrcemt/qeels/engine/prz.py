import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import matplotlib

def load_prz(file_path):
    spectrogram = np.load(file_path, allow_pickle=True)
    render_prz(spectrogram['data'])
    return spectrogram['data']


def render_prz(spectrogram):
    # Temporary solution for displaying image(mainly to perfect adjustments)
    plt.axes([0.25, 0.25, 0.6, 0.6]).set_axis_off()
    spectrogram=np.log(spectrogram+1)
    return spectrogram
    

