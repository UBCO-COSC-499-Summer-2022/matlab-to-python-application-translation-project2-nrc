import numpy as np
from nrcemt.nanomi_optics.engine.lens import Lens

dummy_lense = Lens(0, 0, 0, 0)
c1 = Lens(257.03, 13, 0, 257.03)
c2 = Lens(349, 35, 257.03, 91.97)
c3 = Lens(517, 10.68545, 349, 168)


def test_transfer_free():
    np.testing.assert_allclose(
        dummy_lense.transfer_free(257.03),
        [[1, 257.03], [0, 1]]
    )
    np.testing.assert_allclose(
        dummy_lense.transfer_free(349),
        [[1, 349], [0, 1]]
    )
    np.testing.assert_allclose(
        dummy_lense.transfer_free(168),
        [[1, 168], [0, 1]]
    )
    np.testing.assert_allclose(
        dummy_lense.transfer_free(13.69253780272917),
        [[1, 13.6925378], [0, 1]]
    )
    np.testing.assert_allclose(
        dummy_lense.transfer_free(91.97000000000003),
        [[1, 91.97], [0, 1]]
    )
    np.testing.assert_allclose(
        dummy_lense.transfer_free(38.90127388535032),
        [[1, 38.90127389], [0, 1]]
    )


def test_transfer_thin():
    np.testing.assert_allclose(
        c1.transfer_thin(),
        [[1, 0], [-0.07692308, 1]],
        rtol=1e-5
    )
    np.testing.assert_allclose(
        c2.transfer_thin(),
        [[1, 0], [-0.02857143, 1]],
        rtol=1e-5
    )
    np.testing.assert_allclose(
        c3.transfer_thin(),
        [[1, 0], [-0.0935852, 1]],
        rtol=1e-5
    )


def test_vacuum_matrix():
    ray_out, distance = dummy_lense.vacuum_matrix(
        257.03,
        [[1.5000000e-02], [-2.5987526e-05]]
    )
    np.testing.assert_allclose(
        ray_out,
        [[8.3204262e-03], [-2.5987526e-05]],
        rtol=1e-5
    )
    assert distance == 257.03

    ray_out1, distance1 = dummy_lense.vacuum_matrix(
        13.69253780272917,
        [[0.00832043], [-0.00066602]]
    )
    np.testing.assert_allclose(
        ray_out1,
        [[-0.00079908], [-0.00066602]],
        rtol=1e-5
    )
    assert distance1 == 13.69253780272917

    ray_out2, distance2 = dummy_lense.vacuum_matrix(
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
    ray_out, distance = c1.thin_lens_matrix(
        [[8.3204262e-03], [-2.5987526e-05]],
        0
    )
    np.testing.assert_allclose(
        ray_out,
        [[0.00832043], [-0.00066602]],
        rtol=1e-5
    )
    assert distance == 13.69253780272917

    ray_out, distance = c2.thin_lens_matrix(
        [[-0.09980961], [-0.00128528]],
        0
    )
    np.testing.assert_allclose(
        ray_out,
        [[-0.09980961], [0.00156642]],
        rtol=1e-5
    )
    assert distance == 38.90127388535032

    ray_out, distance = c3.thin_lens_matrix(
        [[0.16334898], [0.00156642]],
        0
    )
    np.testing.assert_allclose(
        ray_out,
        [[0.16334898], [-0.01372063]],
        rtol=1e-5
    )
    assert distance == 10.910959698867039


def test_ray_path():
    rays = [
        [[1.5000000e-02], [-2.5987526e-05]],
        [[0.0000000e+00], [5.1975052e-05]],
        [[0.015], [0]],
        [[-0.015], [0.00012994]]
    ]
    x_points = [0, 257.03, 257.03, 270.72253780272916]
    y_points_per_ray = [
        [
            0.015, 0.008320426195426197,
            0.008320426195426197, -0.0007990820800721221
        ],
        [
            0.0, 0.013359147609147609,
            0.013359147609147609, 0.0
        ],
        [
            0.015, 0.015,
            0.015, -0.0007990820800721221
        ],
        [
            -0.015, 0.018397869022869023,
            0.018397869022869023, 0.0007990820800721256
        ]
    ]

    for i in range(len(rays)):
        points = c1.ray_path(rays[i], 0)
        np.testing.assert_allclose(
            x_points,
            [x for x, y in points],
            rtol=1e-5
        )
        print([y for x, y in points])
        print(np.testing.assert_allclose(
            y_points_per_ray[i],
            [y for x, y in points],
            rtol=1e-5,
            atol=1e-6
        ))
