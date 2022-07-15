from nrcemt.qeels.engine.peak_detection import (
    compute_rect_corners,
    ycfit,
    calc_angle,
    rotate_points,
    peak_detection
)
import math
import numpy as np


def test_ycfit():
    # BASED ON MATLAB CODE
    # NEED TO LOAD SIGNAL in order to isolate this section
    pass


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
    pass


def test_compute_rect_corners():
    pass


def test_peak_detection():
    pass
