import math
import numpy as np
from nrcemt.alignment_software.engine.img_loading import load_dm3
import matplotlib.pyplot as plt

def create_particle_mask(radius, invert=False):

    def mask_value(x, y):
        dx = 1 - (x+1) / radius
        dy = 1 - (y+1) / radius
        dx2 = np.square(dx)
        dy2 = np.square(dy)
        magnitude = np.square(np.clip(dx2+dy2, 0, 1))
        if invert:
            return 0.5 - magnitude
        else:
            return magnitude - 0.5

    return np.fromfunction(mask_value, (2*radius-1, 2*radius-1))

if __name__ == "__main__":
    plt.imshow(create_particle_mask(20, False), cmap="gray", vmin=-0.5, vmax=0.5)
    plt.show()
    # img = load_dm3("nrcemt/alignment_software/test/resources/image_001.dm3")
