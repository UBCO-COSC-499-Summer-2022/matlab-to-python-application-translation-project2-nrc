import math
import numpy as np


def convert_img_float64(img):
    float64_img = img.astype(np.float64)
    minimum = float64_img.min()
    maximum = float64_img.max()
    float64_img -= minimum
    float64_img /= maximum - minimum
    return float64_img


def reject_outliers_percentile(img, percentile):
    img_sorted = np.sort(img.ravel())
    rejection_count = len(img_sorted) / percentile / 50
    minimum_index = math.floor(rejection_count)
    maximum_index = math.ceil(len(img_sorted) - 1 - rejection_count)
    return (img_sorted[minimum_index], img_sorted[maximum_index])
