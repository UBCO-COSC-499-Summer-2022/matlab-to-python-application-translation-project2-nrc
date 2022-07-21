from matplotlib import image
from nrcemt.qeels.engine.peak_detection import (
    compute_rect_corners,
    rotate_spectrogram,
    ycfit,
    calc_angle,
    rotate_points,
    find_peaks,
    peak_detection,
    do_math
)
from nrcemt.qeels.engine.spectrogram import (
    load_spectrogram,
    process_spectrogram
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
    expected_result = expected_result['ycfit']
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
    np.testing.assert_almost_equal(magnitude, 8.051116582363534*(10**-7))
    
    assert ind2 == 60
    np.testing.assert_almost_equal(magnitude2, 6.274820123225556*(10**-7))



def test_do_math():
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
    peak_x = peak_x['Peak_position_x']

    peak_y = loadmat(peak_y_path)
    peak_y = peak_y['Peak_position_y']

    image3 = loadmat(image3_path)
    image3 = image3['image3']
    results = do_math(
        #688.4550934373956
        915.5066294374852, 220.4379997324754+32, 252,
        signal, spectrogram,
        10, 60, 0.008546800432611, 1024, 1024
    )

    # a = np.argmax(np.abs(results[0]-peak_x))
    # print(results[0][0][32])
    # print(peak_x[0][32])


    np.testing.assert_array_almost_equal(results[0], peak_x)
    np.testing.assert_array_almost_equal(results[1], peak_y)
    np.testing.assert_array_almost_equal(results[2], image3)


def test_rotate_spectrogram():
    dirname = os.path.dirname(__file__)
    spectrogram_path = os.path.join(dirname, 'resources/Converted.prz')
    spectrogram = load_spectrogram(spectrogram_path)
    rotated_path = os.path.join(dirname, 'resources/rotated.mat')
    rotated = loadmat(rotated_path)['image']
    result = rotate_spectrogram(spectrogram, 0.4896955931291964)
    # 0.4896955931291964
    # np.testing.assert_array_almost_equal(result, rotated)

#     plasmon_array = [
#         [913, 217], [917, 685],
#         [0, 0], [0, 0],
#         [0, 0], [0, 0]
#     ]
