import numpy as np
from PIL import Image
from .dm3 import DM3Image


def load_dm3(filename):
    """
    Loads just the image data form a DM3 file as a 2D numpy array.
    Other image metadata included in the DM3 file format is ignored.
    """
    with open(filename, 'rb') as file:
        img = DM3Image.read(file)
        img_data = img.tag_group["ImageList"][1]["ImageData"]
        width = img_data["Dimensions"][0].decode()
        height = img_data["Dimensions"][1].decode()
        array = img_data["Data"].decode()
        return array.reshape((width, height))


def load_float_tiff(filename):
    """
    Loads a 32-bit tiff and maps it onto a [0.0, 1.0] 64-bit float range
    """
    with Image.open(filename) as img:
        img_uint32 = np.array(img).astype(np.uint32)
        img_float = np.array(img_uint32).astype(np.float64)
        img_scaled = img_float / 4294967295  # 4294967295 = 2^32-1
        return img_scaled


def save_float_tiff(filename, img):
    """
    Takes a 64-bit float image, and saves to a 32-bit tiff format.
    The input should be on the range [0.0, 1.0].
    """
    img_clipped = np.clip(img, 0.0, 1.0)
    img_scaled = img_clipped * 4294967295  # 4294967295 = 2^32-1
    img_uint32 = img_scaled.astype(np.uint32)
    Image.fromarray(img_uint32).save(filename, format="tiff")
