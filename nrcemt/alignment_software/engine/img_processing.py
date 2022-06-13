import math
import numpy as np


def convert_img_float64(img):
    """Converts an image matrix to float64 type on the range [0.0, 1.0]."""
    float64_img = img.astype(np.float64)
    minimum = float64_img.min()
    maximum = float64_img.max()
    float64_img -= minimum
    float64_img /= maximum - minimum
    return float64_img


def reject_outliers_percentile(img, percent):
    """
    Returns a minimum and maximum threshold which elminate a given percent of
    percent of outliers.
    """
    img_sorted = np.sort(img.ravel())
    rejection_count = len(img_sorted) * percent / 200
    minimum_index = math.floor(rejection_count)
    maximum_index = math.ceil(len(img_sorted) - 1 - rejection_count)
    return (img_sorted[minimum_index], img_sorted[maximum_index])


def adjust_img_range(img, min1, max1, min2, max2):
    """Maps image values from a range [min1, max1] to another [min2, max2]."""
    img_normalized = (img - min1) / (max1 - min1)
    return img_normalized * (max2 - min2) + min2
