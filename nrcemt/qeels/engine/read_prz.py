import numpy as np
import matplotlib as plt
import matplotlib.pyplot as plt


# SHOULD I RENAME TO read() SIMILAR TO IN dm3.py


def read_prz(file):
    spectrogram=np.load("C:\\Users\\garre\\Desktop\\Capstone project-20220530T173400Z-001\\Capstone project\\qEELS\\1_qEELS_1deg_sum.prz", allow_pickle=True)
    plt.axes([0.25, 0.25, 0.6, 0.6]).set_axis_off()
    plt.imshow(np.log(spectrogram['data']+1))
    plt.show()
    return spectrogram
