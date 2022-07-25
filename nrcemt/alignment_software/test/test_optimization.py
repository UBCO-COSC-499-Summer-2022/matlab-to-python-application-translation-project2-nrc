import os
import numpy as np
from nrcemt.alignment_software.engine.csv_io import load_marker_csv
from nrcemt.alignment_software.engine.optimization import (
    compute_marker_shifts,
    compute_transformed_shift,
    normalize_marker_data,
    optimize_magnification_and_rotation,
    optimize_particle_model,
    optimize_tilt_angles,
    optimize_x_shift
)

dirname = os.path.dirname(__file__)
marker_filename = os.path.join(dirname, 'resources/marker_data.csv')
markers = load_marker_csv(marker_filename)


def test_normalize_marker_data():
    markers = [
        [[-1, 2], [-1, 2]],
        [[3, 4], [1, -2]]
    ]
    np.testing.assert_allclose(normalize_marker_data(markers), [
        [[-2, -1], [-1, 2]],
        [[2, 1], [1, -2]]
    ])


def test_optimize_particle_model():
    normalized_markers = normalize_marker_data(markers)
    tilt = np.arange(61) * 3
    x, y, z, alpha, phai = optimize_particle_model(normalized_markers, tilt)
    np.testing.assert_allclose(x, [
        -33.9940, -119.2370, 12.1170, 64.8145, 76.2996
    ], rtol=1e-4)
    np.testing.assert_allclose(y, [
        236.3193, 110.7438, -135.3844, 21.7134, -233.3922,
    ], rtol=1e-4)
    np.testing.assert_allclose(z, [
        -74.9492, -29.2715, 30.8413, -32.2439, 105.6234,
    ], rtol=1e-4)
    np.testing.assert_allclose([alpha, phai], [2.8963, -0.2604], rtol=1e-4)


def test_optimize_rotation_and_magnification():
    normalized_markers = normalize_marker_data(markers)
    tilt = np.arange(61) * 3
    x, y, z, alpha, phai = optimize_particle_model(normalized_markers, tilt)
    magnification, alpha, phai = optimize_magnification_and_rotation(
        normalized_markers, x, y, z, tilt, alpha, phai,
        fixed_phai=False, group_rotation=True, group_magnification=True
    )
    np.testing.assert_allclose(magnification, [
        1.0057, 1.0008, 1.0005, 1.0027, 1.0043, 1.0023, 1.0007, 1.0015, 1.0010,
        0.9986, 1.0006, 0.9975, 0.9993, 1.0017, 0.9995, 1.0007, 0.9996, 1.0006,
        0.9995, 1.0014, 0.9954, 0.9978, 0.9944, 0.9859, 0.9932, 0.9907, 0.9905,
        0.9968, 0.9923, 0.9919, 0.9935, 0.9909, 0.9938, 0.9858, 0.9954, 0.9963,
        0.9971, 1.0003, 0.9988, 1.0006, 0.9994, 1.0019, 1.0017, 1.0030, 1.0002,
        1.0015, 1.0023, 1.0021, 1.0037, 1.0024, 1.0020, 1.0018, 1.0035, 1.0018,
        1.0042, 1.0018, 1.0022, 1.0016, 1.0001, 1.0010, 1.0054
    ], rtol=1e-4)
    np.testing.assert_allclose(alpha, [
        2.5957, 3.0231, 2.9435, 2.8731, 2.8244, 2.8748, 2.9392, 2.9536, 2.9115,
        3.0800, 3.0439, 3.0873, 3.1964, 3.2012, 3.2722, 3.3255, 2.9540, 2.8146,
        2.8040, 2.9599, 2.5963, 2.3056, 2.4256, 1.8627, 2.2623, 2.1261, 2.1547,
        2.3726, 2.8391, 2.3440, 2.3526, 2.2316, 2.4408, 2.9496, 2.9305, 3.0430,
        3.0252, 2.6228, 2.4838, 2.4050, 2.2988, 2.2901, 2.2668, 2.5328, 2.5637,
        2.8385, 2.9965, 2.9440, 3.0507, 2.7727, 2.8636, 2.9000, 2.8981, 2.9134,
        3.0006, 3.0953, 3.2373, 3.1426, 3.1976, 3.1820, 3.1170
    ], rtol=1e-4)
    np.testing.assert_allclose(phai, -0.4428, rtol=1e-4)


def test_optimize_tilt_angles():
    normalized_markers = normalize_marker_data(markers)
    tilt = np.arange(61) * 3
    x, y, z, alpha, phai = optimize_particle_model(normalized_markers, tilt)
    magnification, alpha, phai = optimize_magnification_and_rotation(
        normalized_markers, x, y, z, tilt, alpha, phai,
        fixed_phai=False, group_rotation=True, group_magnification=True
    )
    tilt = optimize_tilt_angles(
        normalized_markers,
        x, y, z, tilt, alpha, phai, magnification
    )
    np.testing.assert_allclose(tilt, [
        -0.1364, 2.6636, 5.5231, 8.9888, 11.9178, 14.7196, 17.8887, 21.1305,
        23.6549, 26.2108, 29.7244, 32.8887, 36.1446, 39.2754, 42.4153, 45.4619,
        48.3679, 51.5830, 53.5020, 57.1340, 61.1946, 63.2826, 66.2590, 69.6200,
        71.7850, 74.8360, 76.9400, 80.3543, 83.4121, 87.1919, 89.9696, 92.6787,
        95.6712, 99.1122, 102.0437, 105.2664, 108.1246, 111.0872, 113.7436,
        116.8476, 119.7210, 122.9163, 126.0602, 129.0652, 131.9776, 135.0402,
        138.0943, 141.1443, 144.0876, 147.1936, 150.0783, 153.0283, 156.1017,
        159.0384, 162.1008, 165.2311, 168.1828, 171.1973, 174.2014, 177.3179,
        180.1012
    ], rtol=1e-3)


def test_compute_marker_shifts():
    shifts = compute_marker_shifts(markers[:, 0:5], (1024, 1024))
    np.testing.assert_allclose(shifts, [
        [46.2000, 100.2000],
        [43.2000, 100.0000],
        [37.6000, 100.6000],
        [31.2000, 100.4000],
        [25.6000, 100.8000]
    ], rtol=1e-3)


def test_compute_transformed_shift():
    shifts = compute_marker_shifts(markers, (1024, 1024))
    x_shift = shifts[:, 0]
    y_shift = shifts[:, 1]
    normalized_markers = normalize_marker_data(markers)
    tilt = np.arange(61) * 3
    x, y, z, alpha, phai = optimize_particle_model(normalized_markers, tilt)
    magnification, alpha, phai = optimize_magnification_and_rotation(
        normalized_markers, x, y, z, tilt, alpha, phai,
        fixed_phai=False, group_rotation=True, group_magnification=True
    )
    x_shift, y_shift = compute_transformed_shift(x_shift, y_shift, alpha, magnification)
    np.testing.assert_equal(x_shift, [
        -41, -38, -32, -26, -21, -13, -8, -4, 1, 5, 11, 15, 20, 24, 29, 32, 36,
        41, 45, 50, 54, 57, 61, 65, 68, 71, 74, 78, 81, 83, 85, 85, 85, 86, 86,
        86, 86, 82, 78, 77, 75, 73, 68, 66, 61, 58, 54, 49, 44, 41, 35, 28, 20,
        14, 7, 0, -7, -15, -21, -27, -34
    ])
    np.testing.assert_equal(y_shift, [
        0, 0, -1, 0, 0, 0, 0, 0, 1, 1, 2, 1, 2, 2, 2, 3, 4, 4, 2, 3, 2, 2, 2,
        0, 5, 4, 4, 4, 6, 5, 7, 7, 9, 9, 9, 9, 11, 10, 10, 10, 9, 10, 10, 11,
        11, 11, 11, 11, 11, 10, 10, 10, 10, 10, 10, 9, 10, 10, 10, 9, 10
    ])


def test_optimize_x_shift():
    tilt = np.arange(61) * 3
    x_shift = [
        -41, -38, -32, -26, -21, -13, -8, -4, 1, 5, 11, 15, 20, 24, 29, 32, 36,
        41, 45, 50, 54, 57, 61, 65, 68, 71, 74, 78, 81, 83, 85, 85, 85, 86, 86,
        86, 86, 82, 78, 77, 75, 73, 68, 66, 61, 58, 54, 49, 44, 41, 35, 28, 20,
        14, 7, 0, -7, -15, -21, -27, -34
    ]
    x_shift = optimize_x_shift(x_shift, tilt)
    np.testing.assert_equal(x_shift, [
        -29, -30, -28, -26, -25, -20, -19, -19, -17, -17, -15, -14, -13, -12,
        -10, -10, -9, -7, -6, -3, -2, -1, 1, 3, 4, 5, 7, 9, 11, 12, 14, 13,
        13, 14, 14, 14, 15, 11, 8, 8, 8, 7, 4, 3, 0, -1, -2, -5, -7, -8, -11,
        -15, -20, -22, -26, -30, -33, -38, -40, -42, -46
    ])
