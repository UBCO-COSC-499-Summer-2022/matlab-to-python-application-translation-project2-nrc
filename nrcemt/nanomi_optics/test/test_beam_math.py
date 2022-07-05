import numpy as np
from nrcemt.nanomi_optics.engine.upperbeam_math import (
    thin_lens_matrix,
    transfer_free,
    transfer_thin,
    vacuum_matrix,
    ray_path
)


def test_transfer_free():
    np.testing.assert_allclose(
        transfer_free(257.03),
        [[1, 257.03], [0, 1]]
    )
    np.testing.assert_allclose(
        transfer_free(349),
        [[1, 349], [0, 1]]
    )
    np.testing.assert_allclose(
        transfer_free(168),
        [[1, 168], [0, 1]]
    )
    np.testing.assert_allclose(
        transfer_free(13.69253780272917),
        [[1, 13.6925378], [0, 1]]
    )
    np.testing.assert_allclose(
        transfer_free(91.97000000000003),
        [[1, 91.97], [0, 1]]
    )
    np.testing.assert_allclose(
        transfer_free(38.90127388535032),
        [[1, 38.90127389], [0, 1]]
    )


def test_transfer_thin():
    np.testing.assert_allclose(
        transfer_thin(13),
        [[1, 0], [-0.07692308, 1]]
    )
    np.testing.assert_allclose(
        transfer_thin(35),
        [[1, 0], [-0.02857143, 1]]
    )
    np.testing.assert_allclose(
        transfer_thin(10.68545),
        [[1, 0], [-0.0935852, 1]]
    )


def test_vacuum_matrix():
    ray_out, distance = vacuum_matrix(
        257.03,
        [[1.5000000e-02], [-2.5987526e-05]]
    )
    np.testing.assert_allclose(
        ray_out,
        [[8.3204262e-03], [-2.5987526e-05]]
    )
    assert distance == 257.03

    ray_out1, distance1 = vacuum_matrix(
        13.69253780272917,
        [[0.00832043], [-0.00066602]]
    )
    np.testing.assert_allclose(
        ray_out1,
        [[-0.00079908], [-0.00066602]]
    )
    assert distance1 == 13.69253780272917

    ray_out2, distance2 = vacuum_matrix(
        168,
        [[-0.05293346], [0.00084636]]
    )
    np.testing.assert_allclose(
        ray_out2,
        [[0.08925574], [0.00084636]]
    )
    assert distance2 == 168


def test_thin_lens_matrix():
    ray_out, img_location, distance, mag_out = thin_lens_matrix(
        349, 35,
        [[-0.05293346], [-0.00066602]], 0)
    np.testing.assert_allclose(
        ray_out,
        [[-0.05293346], [0.00084636]]
    )
    assert img_location == 387.9012738853503
    assert distance == 38.90127388535032
    assert mag_out == -0.11146496815286625


def test_ray_path():
    x, y = ray_path(
        [13, 35, 10.68545],
        [[1.5000000e-02], [-2.5987526e-05]],
    )

    np.testing.assert_allclose(
        x,
        [0, 257.03, 257.03,
         270.72253780272916, 257.03, 349.0,
         349, 387.9012738853503, 349,
         517, 517, 527.910959698867,
         517, 528.9]
    )
    np.testing.assert_allclose(
        y,
        [0.015, 0.008320426195426197, 0.008320426195426197,
         -0.0007990820800721221, 0.008320426195426197, -0.05293346173836562,
         -0.05293346173836562, -0.020008811875395355, -0.05293346173836562,
         0.08925574248360797, 0.08925574248360797, 0.007350960601603784,
         0.08925574248360797, -7.342115513725433e-05]
    )
