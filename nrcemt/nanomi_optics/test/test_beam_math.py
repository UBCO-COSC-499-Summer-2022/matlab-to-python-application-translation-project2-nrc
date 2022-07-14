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


def test_transfer_free():
    np.testing.assert_allclose(
        Lens.transfer_free_space(257.03),
        [[1, 257.03], [0, 1]]
    )
    np.testing.assert_allclose(
        Lens.transfer_free_space(349),
        [[1, 349], [0, 1]]
    )
    np.testing.assert_allclose(
        Lens.transfer_free_space(168),
        [[1, 168], [0, 1]]
    )
    np.testing.assert_allclose(
        Lens.transfer_free_space(13.69253780272917),
        [[1, 13.6925378], [0, 1]]
    )
    np.testing.assert_allclose(
        Lens.transfer_free_space(91.97000000000003),
        [[1, 91.97], [0, 1]]
    )
    np.testing.assert_allclose(
        Lens.transfer_free_space(38.90127388535032),
        [[1, 38.90127389], [0, 1]]
    )


def test_transfer_thin():
    np.testing.assert_allclose(
        c1.transfer_thin_lense(),
        [[1, 0], [-0.014861049190073, 1]],
        rtol=1e-6,
        atol=1e-6
    )
    np.testing.assert_allclose(
        c2.transfer_thin_lense(),
        [[1, 0], [-0.043591979075850, 1]],
        rtol=1e-6,
        atol=1e-6
    )
    np.testing.assert_allclose(
        c3.transfer_thin_lense(),
        [[1, 0], [-0.025075225677031, 1]],
        rtol=1e-6,
        atol=1e-6
    )


def test_vacuum_matrix():
    ray_out, distance = Lens.vacuum_matrix(
        257.03,
        [[1.5000000e-02], [-2.5987526e-05]]
    )
    np.testing.assert_allclose(
        ray_out,
        [[8.3204262e-03], [-2.5987526e-05]],
        rtol=1e-5
    )
    assert distance == 257.03

    ray_out1, distance1 = Lens.vacuum_matrix(
        13.69253780272917,
        [[0.00832043], [-0.00066602]]
    )
    np.testing.assert_allclose(
        ray_out1,
        [[-0.00079908], [-0.00066602]],
        rtol=1e-5
    )
    assert distance1 == 13.69253780272917

    ray_out2, distance2 = Lens.vacuum_matrix(
        168,
        [[-0.05293346], [0.00084636]]
    )
    np.testing.assert_allclose(
        ray_out2,
        [[0.08925574], [0.00084636]],
        rtol=1e-5
    )
    assert distance2 == 168


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
        rtol=1e-5
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
        rtol=1e-5
    )
    np.testing.assert_allclose(
        y_points,
        [y for x, y in points],
        rtol=1e-5,
        atol=1e-6
    )

