from nrcemt.qeels.engine.peak_detection import (
    compute_rect_corners,
    ycfit,
    calc_angle,
    rotate_points
)
import math
import numpy as np
from scipy.io import loadmat


def test_ycfit():
    # x1:928 y1:273
    # x2:909 y2:700
    signal = loadmat('nrcemt\\qeels\\test\\resources\\signal.mat')
    signal_data = signal['Signal']
    expected_result = loadmat('nrcemt\\qeels\\test\\resources\\ycfit.mat')
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


def test_peak_detection():
    pass
