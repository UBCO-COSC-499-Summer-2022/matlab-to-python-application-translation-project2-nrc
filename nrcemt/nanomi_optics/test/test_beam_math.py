import numpy as np
from nrcemt.nanomi_optics.engine.upperbeam_math import (
    transfer_free,
    transfer_thin,
    vacuum_matrix,
    # thin_lens_matrix
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
        0, 257.03,
        [[1.5000000e-02], [-2.5987526e-05]]
    )
    np.testing.assert_allclose(
        ray_out,
        [[8.3204262e-03], [-2.5987526e-05]]
    )
    assert distance == 257.03

    ray_out, distance = vacuum_matrix(
        257.03, 13.69253780272917,
        [[0.00832043], [-0.00066602]]
    )
    np.testing.assert_allclose(
        ray_out,
        [[-0.00079908], [-0.00066602]]
    )
    assert distance == 13.69253780272917
