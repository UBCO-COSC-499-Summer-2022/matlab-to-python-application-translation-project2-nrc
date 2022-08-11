import os
import numpy as np
from nrcemt.alignment_software.engine.img_io import (
    load_dm3
)
from nrcemt.alignment_software.engine.img_processing import (
    compute_img_shift,
    combine_tranforms,
    convert_img_float64,
    no_transform,
    reject_outliers_percentile,
    adjust_img_range,
    resize_img,
    rotate_transform,
    sobel_filter_img,
    transform_img,
    translate_transform
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


def test_reject_outliers_percentile_normal():
    img = np.random.normal(0.4, 0.1, 20000).reshape((200, 100))
    img_copy = np.copy(img)
    minimum, maximum = reject_outliers_percentile(img, 2.0)
    # make sure the original image was not modified
    assert np.array_equal(img, img_copy)
    # check whether minimum and maximum reject the correct number of elements
    assert minimum < maximum
    assert (img < minimum).sum() == 200
    assert (img > maximum).sum() == 200


def test_reject_outliers_percentile_random():
    img = np.random.uniform(0.0, 1.0, 10000).reshape((100, 100))
    img_copy = np.copy(img)
    minimum, maximum = reject_outliers_percentile(img, 1.0)
    # make sure the original image was not modified
    assert np.array_equal(img, img_copy)
    # check whether minimum and maximum reject the correct number of elements
    assert minimum < maximum
    assert (img < minimum).sum() == 50
    assert (img > maximum).sum() == 50


def test_adjust_img_range():
    img = np.array([
        [0.1, 0.2],
        [0.3, 0.7],
        [0.8, 0.9]
    ])
    img_copy = np.copy(img)
    img_adjusted = adjust_img_range(img, 0.0, 1.0, 10.0, 20.0)
    # make sure the original image was not modified
    assert np.array_equal(img, img_copy)
    # check if the range has been adjusted correctly
    assert np.array_equal(img_adjusted, [
        [11.0, 12.0],
        [13.0, 17.0],
        [18.0, 19.0]
    ])


def test_no_transform():
    assert np.array_equal(
        no_transform(),
        [
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
        ]
    )


def test_translate_transform():
    assert np.array_equal(
        translate_transform(3, 2),
        [
            [1, 0, 2],
            [0, 1, 3],
            [0, 0, 1],
        ]
    )
    assert np.array_equal(
        translate_transform(-5, 0),
        [
            [1, 0, 0],
            [0, 1, -5],
            [0, 0, 1],
        ]
    )


def test_rotate_transform():
    np.testing.assert_allclose(
        rotate_transform(90),
        [
            [0, -1, 0],
            [1, 0, 0],
            [0, 0, 1],
        ],
        atol=1e-9,
        rtol=1e-9
    )
    np.testing.assert_allclose(
        rotate_transform(180),
        [
            [-1, 0, 0],
            [0, -1, 0],
            [0, 0, 1],
        ],
        atol=1e-9,
        rtol=1e-9
    )
    np.testing.assert_allclose(
        rotate_transform(180, 1, 1),
        [
            [-1, 0, 2],
            [0, -1, 2],
            [0, 0, 1],
        ],
        atol=1e-9,
        rtol=1e-9
    )
    np.testing.assert_allclose(
        rotate_transform(0),
        no_transform(),
        atol=1e-9,
        rtol=1e-9
    )


def test_combine_transforms():
    assert np.array_equal(
        combine_tranforms(no_transform(), rotate_transform(123)),
        rotate_transform(123)
    )
    np.testing.assert_allclose(
        combine_tranforms(
            translate_transform(5, 10),
            translate_transform(-5, -10),
            rotate_transform(-20),
            rotate_transform(60),
            rotate_transform(10)
        ),
        rotate_transform(50)
    )


def test_transform_img():
    img = np.array([
        [1, 1, 1],
        [2, 2, 2],
        [3, 3, 3]
    ]).astype(np.uint8)
    translate = translate_transform(1, 1)
    assert np.array_equal(
        transform_img(img, translate, fill=2),
        [
            [2, 2, 2],
            [2, 1, 1],
            [2, 2, 2]
        ]
    )


def test_resize_img():
    img = np.array([
        [2, 6, 2, 2],
        [2, 3, 2, 2],
        [0, 0, 1, 3],
        [0, 0, 3, 1],
    ]).astype(np.uint8)
    assert np.array_equal(
        resize_img(img, 1/2),
        [
            [3, 2],
            [0, 2]
        ]
    )


def test_sobel_filter_img():
    img = np.array([
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 1],
        [0, 0, 1, 1]
    ])
    np.array_equal(
        sobel_filter_img(img),
        [
            [0, 4, 4, 0],
            [0, 4, 4, 0],
            [0, 4, 4, 0],
            [0, 4, 4, 0]
        ]
    )


dirname = os.path.dirname(__file__)
img1_filename = os.path.join(dirname, 'resources/image_001.dm3')
img2_filename = os.path.join(dirname, 'resources/image_002.dm3')


def test_compute_img_shift():
    img1 = load_dm3(img1_filename)
    img2 = load_dm3(img2_filename)
    assert compute_img_shift(img1, img1) == (0, 0)
    assert compute_img_shift(img2, img2) == (0, 0)
    assert compute_img_shift(img1, img2) == (-36, -5)
    assert compute_img_shift(img2, img1) == (36, 5)
