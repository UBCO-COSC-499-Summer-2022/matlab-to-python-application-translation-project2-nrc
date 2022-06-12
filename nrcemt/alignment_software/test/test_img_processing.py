import numpy as np
from nrcemt.alignment_software.engine.img_processing import (
    convert_img_float64
)


def test_convert_img_float64():
    img = np.arange(4, 16).reshape((3, 4))
    img_copy = np.copy(img)
    img_float64 = convert_img_float64(img)
    # make sure the original image was not modified
    assert np.array_equal(img, img_copy)
    # assert expected
    img_expected = (img.astype(np.float64) - 4.0) / 11.0
    assert np.array_equal(img_float64, img_expected)
