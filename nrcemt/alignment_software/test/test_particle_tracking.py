import os
import numpy as np

from nrcemt.alignment_software.engine.particle_tracking import create_particle_mask

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'resources/image_001.dm3')


def test_create_particle_mask():
    # assert a small mask
    np.testing.assert_allclose(
        create_particle_mask(2),
        [
            [0.25,   0.0625, 0.25],
            [0.0625, 0.,     0.0625],
            [0.25,   0.0625, 0.25]
        ]
    )
    # assert a bigger inverted mask
    np.testing.assert_allclose(
        create_particle_mask(3, invert=True),
        [
            [0.20987654, 0.69135802, 0.80246914, 0.69135802, 0.20987654],
            [0.69135802, 0.95061728, 0.98765432, 0.95061728, 0.69135802],
            [0.80246914, 0.98765432, 1.,         0.98765432, 0.80246914],
            [0.69135802, 0.95061728, 0.98765432, 0.95061728, 0.69135802],
            [0.20987654, 0.69135802, 0.80246914, 0.69135802, 0.20987654]
        ]
    )
    # assert invereted masks of the same shape add up to 1.0 for all values
    np.testing.assert_allclose(
        create_particle_mask(20, invert=True) +
        create_particle_mask(20, invert=False),
        np.ones((39, 39))
    )
