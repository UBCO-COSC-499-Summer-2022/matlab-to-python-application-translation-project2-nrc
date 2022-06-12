import numpy as np
from nrcemt.alignment_software.engine.img_processing import (
    convert_img_float64,
    reject_outliers_percentile
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


def test_reject_outliers_percentile():
    img = np.random.normal(0.4, 0.1, 20000).reshape((200, 100))
    img_copy = np.copy(img)
    minimum, maximum = reject_outliers_percentile(img, 2.0)
    # make sure the original image was not modified
    assert np.array_equal(img, img_copy)
    # check whether minimum and maximum reject the correct number of elements
    assert minimum < maximum
    assert (img < minimum).sum() == 200
    assert (img > maximum).sum() == 200
