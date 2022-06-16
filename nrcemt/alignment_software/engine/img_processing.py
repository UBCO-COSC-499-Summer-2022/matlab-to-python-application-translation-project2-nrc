import math
import numpy as np
import scipy.ndimage


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
    img_flat = img.flatten()
    rejection_count = len(img_flat) * percent / 200
    minimum_index = math.floor(rejection_count)
    maximum_index = math.ceil(len(img_flat) - 1 - rejection_count)
    img_flat.partition(minimum_index)
    minimum = img_flat[minimum_index]
    img_flat.partition(maximum_index)
    maximum = img_flat[maximum_index]
    return (minimum, maximum)


def adjust_img_range(img, min1, max1, min2, max2):
    """Maps image values from a range [min1, max1] to another [min2, max2]."""
    img_normalized = (img - min1) / (max1 - min1)
    return img_normalized * (max2 - min2) + min2


def translate_img(img, x, y):
    return scipy.ndimage.shift(img, (y, x), mode="constant", cval=img.mean())
