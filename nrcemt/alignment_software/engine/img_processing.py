import numpy as np


def convert_img_float64(img):
    float64_img = img.astype(np.float64)
    minimum = float64_img.min()
    maximum = float64_img.max()
    float64_img -= minimum
    float64_img /= maximum - minimum
    return float64_img
