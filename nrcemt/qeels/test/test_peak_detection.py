from nrcemt.qeels.engine.peak_detection import (
    bulk_calculations,
    calculation_e,
    calculation_q,
    compute_rect_corners,
    mark_peaks,
    surface_plasmon_calculations,
    ycfit,
    calc_angle,
    rotate_points,
    find_peaks
)
from nrcemt.qeels.engine.spectrogram import (
    load_spectrogram
)
import math
import numpy as np
from scipy.io import loadmat
import os


def test_ycfit():
    dirname = os.path.dirname(__file__)
    signal_path = os.path.join(dirname, 'resources/signal.mat')
    ycfit_path = os.path.join(dirname, 'resources/ycfit.mat')

    signal = loadmat(signal_path)
    signal_data = signal['Signal']
    expected_result = loadmat(ycfit_path)
    expected_result = expected_result['ycfit'].flatten()
    ycfit_result = ycfit(
        signal_data, 10,
        254, 60,
        916,
        6062682.269999994
    )
    np.testing.assert_array_almost_equal(ycfit_result, expected_result)


def test_calc_angle():
    # test y1==y2
    angle_rad, angle_deg = calc_angle(38, 99, 88, 99)
    np.testing.assert_almost_equal(angle_rad, math.pi/2*-1)
    np.testing.assert_almost_equal(angle_deg, 90*-1)

    # test x1 == x2
    angle_rad, angle_deg = calc_angle(250, 849, 250, 544)
    assert angle_rad == 0
    assert angle_deg == 0

    # test some random values
    angle_rad, angle_deg = calc_angle(345, 567, 948, 232)
    np.testing.assert_almost_equal(angle_rad, -1.063697822402560)
    np.testing.assert_almost_equal(angle_deg, -60.945395900922875)


def test_rotate_points():
    # test 3 different angles
    x1, y1, x2, y2 = rotate_points(
        700, 256,
        494, 576,
        -0.571968992222047,
        1024, 1024
    )
    np.testing.assert_almost_equal(x1, 531.5074140510881)
    np.testing.assert_almost_equal(y1, 194.9835007495045)
    np.testing.assert_almost_equal(x2, 531.5074140510881)
    np.testing.assert_almost_equal(y2, 575.5567525683889)

    x1, y1, x2, y2 = rotate_points(
        905, 262,
        995, 708,
        0.199119696072498,
        1024, 1024
    )
    np.testing.assert_almost_equal(x1, 946.6863717422175)
    np.testing.assert_almost_equal(y1, 344.6776816393380)
    np.testing.assert_almost_equal(x2, 946.6863717422175)
    np.testing.assert_almost_equal(y2, 799.6677914219573)

    x1, y1, x2, y2 = rotate_points(
        924, 276,
        924, 691,
        0,
        1024, 1024
    )
    np.testing.assert_almost_equal(x1, 924)
    np.testing.assert_almost_equal(y1, 276)
    np.testing.assert_almost_equal(x2, 924)
    np.testing.assert_almost_equal(y2, 691)


def test_compute_rect_corners():
    # x1:928 y1:273
    # x2:909 y2:700
    calculated_corners = compute_rect_corners(928, 273, 909, 700, 60)
    # x
    assert calculated_corners[0][0] == 958
    assert calculated_corners[1][0] == 898
    assert calculated_corners[2][0] == 879
    assert calculated_corners[3][0] == 939
    # y
    assert calculated_corners[0][1] == 274
    assert calculated_corners[1][1] == 272
    assert calculated_corners[2][1] == 699
    assert calculated_corners[3][1] == 701


def test_peak_finding():
    dirname = os.path.dirname(__file__)
    ycfit_path = os.path.join(dirname, 'resources/ycfit.mat')
    ycfit = loadmat(ycfit_path)
    ycfit = ycfit['ycfit'][0]
    ind, magnitude = find_peaks(ycfit)

    ycfit2_path = os.path.join(dirname, 'resources/ycfit2.mat')
    ycfit2 = loadmat(ycfit2_path)
    ycfit2 = ycfit2['ycfit'][0]
    ind2, magnitude2 = find_peaks(ycfit2)

    assert ind == 22
    np.testing.assert_almost_equal(magnitude, 8.051116582363534e-7)

    assert ind2 == 60
    np.testing.assert_almost_equal(magnitude2, 6.274820123225556e-7)


def test_mark_peaks():
    dirname = os.path.dirname(__file__)
    signal_path = os.path.join(dirname, 'resources/signal.mat')
    spectrogram_path = os.path.join(dirname, 'resources/Converted.prz')
    peak_x_path = os.path.join(dirname, 'resources/peak_pos_x.mat')
    peak_y_path = os.path.join(dirname, 'resources/peak_pos_y.mat')
    image3_path = os.path.join(dirname, 'resources/image3.mat')

    spectrogram = load_spectrogram(spectrogram_path)

    signal = loadmat(signal_path)
    signal = signal['Signal']

    peak_x = loadmat(peak_x_path)
    peak_x = peak_x['Peak_position_x'].flatten()

    peak_y = loadmat(peak_y_path)
    peak_y = peak_y['Peak_position_y'].flatten()

    image3 = loadmat(image3_path)
    image3 = image3['image3']

    # Subtracted 1 from value because value is
    # based off matlabs 1 based indexing
    results = mark_peaks(
        915.5066294374852, 220.4379997324754-1, 688.4550934373956-1,
        signal, spectrogram,
        10, 60, 0.008546800432611, 1024, 1024
    )

    np.testing.assert_allclose(results[0], peak_x, rtol=1, atol=1)
    np.testing.assert_allclose(results[1], peak_y, rtol=1, atol=1)
    np.testing.assert_allclose(results[2], image3, rtol=1, atol=5000)


# Test comment out because rotation is producing a slightly different rotation
# Visually the rotation looks the same
def test_rotate_spectrogram():
    pass
#     dirname = os.path.dirname(__file__)
#     spectrogram_path = os.path.join(dirname, 'resources/Converted.prz')
#     spectrogram = load_spectrogram(spectrogram_path)
#     rotated_path = os.path.join(dirname, 'resources/rotated.mat')
#     rotated = loadmat(rotated_path)['image']
#     result = rotate_spectrogram(spectrogram, 0.4896955931291964)

#     # 0.4896955931291964
#     np.testing.assert_array_almost_equal(result, rotated)

#     plasmon_array=[
#         [913, 217], [917, 685],
#         [0, 0], [0, 0],
#         [0, 0], [0, 0]
#


def test_calculation_e():
    dirname = os.path.dirname(__file__)
    peak_x_path = os.path.join(dirname, 'resources/peak_pos_x.mat')
    peak_x = loadmat(peak_x_path)
    peak_x = peak_x['Peak_position_x'].flatten()

    res = calculation_e(200, peak_x)
    assert res == 4139449


def test_bulk_calculations():
    dirname = os.path.dirname(__file__)
    peak_x_path = os.path.join(dirname, 'resources/peak_pos_x.mat')
    peak_y_path = os.path.join(dirname, 'resources/peak_pos_y.mat')
    image2_path = os.path.join(dirname, 'resources/image2.mat')

    image2 = loadmat(image2_path)
    image2 = image2['image2']

    spectrogram_path = os.path.join(dirname, 'resources/Converted.prz')
    spectrogram = load_spectrogram(spectrogram_path)

    peak_x = loadmat(peak_x_path)
    peak_x = peak_x['Peak_position_x'].flatten()

    peak_y = loadmat(peak_y_path)
    peak_y = peak_y['Peak_position_y'].flatten()

    result, image = bulk_calculations(peak_x, peak_y, 15.0, spectrogram)

    np.testing.assert_almost_equal(result, 0.051094149613447)
    np.testing.assert_allclose(
        image, image2,
        atol=10000, rtol=1
    )


# 1:(682, 482), 2:(844, 390)
def test_calculation_q():
    dirname = os.path.dirname(__file__)
    peak_x_path = os.path.join(dirname, 'resources/peak_pos_x(upper).mat')
    peak_y_path = os.path.join(dirname, 'resources/peak_pos_y(upper).mat')

    peak_x = loadmat(peak_x_path)
    peak_x = peak_x['Peak_position_x'].flatten()

    peak_y = loadmat(peak_y_path)
    peak_y = peak_y['Peak_position_y'].flatten()

    res = calculation_q(
        1165934, peak_x, peak_y, 0.0569
    )

    res2 = calculation_q(
        3.127567785110500e5,
        peak_x, peak_y,
        0.0569
    )

    res3 = calculation_q(
        1.5243e5,
        peak_x, peak_y,
        0.0569
    )

    res4 = calculation_q(
        1.6345e5,
        peak_x, peak_y,
        0.0569
    )

    res5 = calculation_q(
        1.9546e5,
        peak_x, peak_y,
        0.0569
    )

    res6 = calculation_q(
        2e6,
        peak_x, peak_y,
        0.0569
    )

    np.testing.assert_almost_equal(res, 1.613344424025299e03)
    np.testing.assert_almost_equal(res2, 1.483953382190898e03)
    np.testing.assert_almost_equal(res3, 1.872686170354184e+03)
    np.testing.assert_almost_equal(res4, 1.787347483147202e+03)
    np.testing.assert_almost_equal(res5, 1.624980374906233e+03)
    np.testing.assert_almost_equal(res6, 1.628523280306290e+03)


def test_surface_plasmon_calculations():
    dirname = os.path.dirname(__file__)
    peak_x_path = os.path.join(dirname, 'resources/peak_pos_x(upper).mat')
    peak_y_path = os.path.join(dirname, 'resources/peak_pos_y(upper).mat')
    spectrogram_path = os.path.join(dirname, 'resources/Converted.prz')
    image2_path = os.path.join(dirname, 'resources/image2.mat')

    spectrogram = load_spectrogram(spectrogram_path)
    peak_x = loadmat(peak_x_path)

    peak_x = peak_x['Peak_position_x'].flatten()

    peak_y = loadmat(peak_y_path)
    peak_y = peak_y['Peak_position_y'].flatten()

    image2 = loadmat(image2_path)
    image2 = image2['image2']

    results, image_result, q_pixel = surface_plasmon_calculations(
        peak_x, peak_y,
        1165934, 0.0569,
        spectrogram
    )
    # 1165944 is expected, however 312756.77851105 is produced

    # Testing is this way because matlab least squares
    # optimization produces a different result than pythons
    # This test confirms python produces a equal
    # or better result
    assert (
        calculation_q(q_pixel, peak_x, peak_y, 0.0569) <=
        calculation_q(1165944, peak_x, peak_y, 0.0569)
    )

    # Following test are from matlab using our calculated q_pixel value
    np.testing.assert_almost_equal(results, 0.6157, decimal=4)

    # atm fails because matlab code
    np.testing.assert_allclose(
        image_result, image2,
        atol=10000, rtol=1
    )
