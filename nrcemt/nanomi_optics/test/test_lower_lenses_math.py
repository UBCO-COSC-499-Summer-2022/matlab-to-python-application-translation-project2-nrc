import numpy as np
from nrcemt.nanomi_optics.engine.lens import Lens
CA_DIAMETER = 0.01
CONDENSOR_APERATURE = [192.4, 1.5, 1, [0, 0, 0], 'Cond. Apert']
ray = np.array(
    [[0], [(CA_DIAMETER/2) / CONDENSOR_APERATURE[0]]]
)
c1 = Lens(257.03, 67.29, None, 3, True)
c2 = Lens(349, 22.94, c1, 3, True)
c3 = Lens(517, 39.88, c2, 3, True)


def test_transfer_thin():
    np.testing.assert_allclose(
        c1.transfer_thin_lense(),
        [[1, 0], [-0.014861049190073, 1]],
        rtol=1e-8,
        atol=1e-8
    )
    np.testing.assert_allclose(
        c2.transfer_thin_lense(),
        [[1, 0], [-0.043591979075850, 1]],
        rtol=1e-8,
        atol=1e-8
    )
    np.testing.assert_allclose(
        c3.transfer_thin_lense(),
        [[1, 0], [-0.025075225677031, 1]],
        rtol=1e-8,
        atol=1e-8
    )


def test_thin_lens_matrix():
    ray_out, overall_ray_out, distance = c1.thin_lens_matrix(
        [[0.006679573804574], [0.000025987525988]],
        0
    )
    np.testing.assert_allclose(
        ray_out,
        [[0.006679573804574], [-0.000073277948891]],
        rtol=1e-8,
        atol=1e-8
    )
    np.testing.assert_allclose(
        overall_ray_out,
        [[-0.000000000000004], [-0.000073277948891]],
        rtol=1e-8,
        atol=1e-8
    )
    np.testing.assert_allclose( 
        distance,
        91.15394065563403,
        rtol=1e-8,
        atol=1e-8
    )

    ray_out, overall_ray_out, distance = c2.thin_lens_matrix(
        [[-0.597991549284478], [-0.732779488909672]],
        348.18394065563398954
    )
    np.testing.assert_allclose(
        ray_out,
        [[-0.597991549284478], [-0.706711853805727]],
        rtol=1e-8,
        atol=1e-8
    )
    np.testing.assert_allclose(
        overall_ray_out,
        [[0.000000000000009], [-0.706711853805727]],
        rtol=1e-8,
        atol=1e-8
    )
    np.testing.assert_allclose( 
        distance,
        -0.84616034960250274821,
        rtol=1e-8,
        atol=1e-8
    )


def test_ray_path():
    x_points = [
        0, 257.02999999999997272, 348.18394065563398954, 348.18394065563398954
    ]
    y_points = [
        0.0, 0.006679573804573804563, 0, -4.336808689942017736e-19
    ]

    points = c1.ray_path(ray, 0)
    np.testing.assert_allclose(
        x_points,
        [x for x, y in points],
        rtol=1e-8,
        atol=1e-8
    )
    np.testing.assert_allclose(
        y_points,
        [y for x, y in points],
        rtol=1e-8,
        atol=1e-8
    )

    c2.update_output_plane_location()
    x_points = [
        257.02999999999997272, 349,
        348.15383965039751502, 348.15383965039751502
    ]

    y_points = [
        0.006679573804573804563, -5.9799154928447811885e-05,
        0, 9.0801931945660996348e-19
    ]
    points = c2.ray_path(c1.ray_out_lense, 0)
    np.testing.assert_allclose(
        x_points,
        [x for x, y in points],
        rtol=1e-8,
        atol=1e-8
    )
    np.testing.assert_allclose(
        y_points,
        [y for x, y in points],
        rtol=1e-8,
        atol=1e-8
    )

    c3.update_output_plane_location()
    x_points = [
        349, 517, 569.21202877164591882, 569.21202877164591882
    ]

    y_points = [
        -5.9799154928447811885e-05, -0.011932558298864670218,
        0, 8.6736173798840354721e-19
    ]
    points = c3.ray_path(c2.ray_out_lense, 0)
    np.testing.assert_allclose(
        x_points,
        [x for x, y in points],
        rtol=1e-8,
        atol=1e-8
    )
    np.testing.assert_allclose(
        y_points,
        [y for x, y in points],
        rtol=1e-8,
        atol=1e-8
    )
