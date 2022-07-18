from nrcemt.qeels.engine.peak_detection import (
    compute_rect_corners,
    ycfit,
    calc_angle,
    rotate_points,
    peak_detection
)
import math
import numpy as np
from scipy.io import loadmat


def test_ycfit():
    signal = loadmat('nrcemt\\qeels\\test\\resources\\signal.mat')
    signal_data = signal['Signal']
    expected_result = loadmat('nrcemt\\qeels\\test\\resources\\ycfit.mat')
    expected_result = expected_result['ycfit']
    ycfit_result = ycfit(
        signal_data, 5,
        256, 60,
        923.0977699888354,
        6156293.133333326
    )

    assert np.testing.assert_almost_equal(ycfit_result, expected_result)


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
    pass


def test_peak_detection():
    pass
