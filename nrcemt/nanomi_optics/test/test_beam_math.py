import numpy as np
from nrcemt.nanomi_optics.engine.upperbeam_math import (
    transfer_free,
    transfer_thin,
    ray_path,
    vacuum_matrix,
    thin_lens_matrix
)


def test_transfer_free():
    np.testing.assert_allclose(transfer_free(257.03),
                               [[1, 257.03], [0, 1]])
    np.testing.assert_allclose(transfer_free(349),
                               [[1, 349], [0, 1]])
    np.testing.assert_allclose(transfer_free(168),
                               [[1, 168], [0, 1]])
    np.testing.assert_allclose(transfer_free(13.69253780272917),
                               [[1, 13.6925378], [0, 1]])
    np.testing.assert_allclose(transfer_free(91.97000000000003),
                               [[1, 91.97], [0, 1]])
    np.testing.assert_allclose(transfer_free(38.90127388535032),
                               [[1, 38.90127389], [0, 1]])


def test_transfer_thin():
    np.testing.assert_allclose(transfer_thin(13),
                               [[1, 0], [-0.07692308, 1]])
    np.testing.assert_allclose(transfer_thin(35),
                               [[1, 0], [-0.02857143, 1]])
    np.testing.assert_allclose(transfer_thin(10.68545),
                               [[1, 0], [-0.0935852, 1]])
