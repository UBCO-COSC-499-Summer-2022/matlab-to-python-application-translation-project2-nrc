import math
import numpy as np
import scipy.ndimage
from PIL import Image


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


def no_transform():
    return np.identity(3)


def translate_transform(x, y):
    return [
        [1, 0, y],
        [0, 1, x],
        [0, 0, 1]
    ]


def rotate_transform(degrees, origin_x=0, origin_y=0):
    offset_origin = translate_transform(-origin_x, -origin_y)
    reset_origin = translate_transform(origin_x, origin_y)
    theta = math.radians(degrees)
    rotation = [
        [math.cos(theta), -math.sin(theta), 0],
        [math.sin(theta), math.cos(theta), 0],
        [0, 0, 1]
    ]
    return combine_tranforms(offset_origin, rotation, reset_origin)


def scale_transform(percent, origin_x=0, origin_y=0):
    offset_origin = translate_transform(-origin_x, -origin_y)
    reset_origin = translate_transform(origin_x, origin_y)
    ratio = percent / 100
    scale = [
        [ratio, 0, 0],
        [0, ratio, 0],
        [0, 0, 1]
    ]
    return combine_tranforms(offset_origin, scale, reset_origin)


def combine_tranforms(*transforms):
    result = no_transform()
    for transform in transforms:
        result = np.matmul(transform, result)
    return result


def transform_img(img, transform):
    try:
        inverse_transform = scipy.linalg.inv(transform)
    except np.linalg.LinAlgError:
        return np.full(img.shape, img.mean())
    return scipy.ndimage.affine_transform(
        img, inverse_transform, cval=img.mean()
    )


def resize_img(img, factor):
    width, height = img.shape
    new_shape = (int(width * factor), int(height * factor))
    return np.array(Image.fromarray(img).resize(new_shape))


def sobel_filter_img(img):
    """
    Performs a convolution with a sobel operator.
    TODO: add larger sobel operator sizes
    """
    return scipy.ndimage.sobel(img)


def compute_img_shift(img1, img2):
    """
    Determines how much img2 must be shifted in x and y to align with img1
    """
    # compute 2-dimensional fourier transform for both images
    img2_fft = np.fft.fft2(img1)
    img1_fft = np.conjugate(np.fft.fft2(img2))
    # compute cross-correlation
    img_correlation = np.real(np.fft.ifft2((img1_fft*img2_fft)))
    img_correlation_shift = np.fft.fftshift(img_correlation)
    # determine image shift
    y_shift, x_shift = np.unravel_index(
        np.argmax(img_correlation_shift), img1.shape
    )
    height, width = img1.shape
    x_shift -= int(width/2)
    y_shift -= int(height/2)
    return x_shift, y_shift
