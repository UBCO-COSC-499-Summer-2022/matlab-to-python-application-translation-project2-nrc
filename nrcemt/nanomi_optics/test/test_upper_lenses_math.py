import numpy as np
from nrcemt.nanomi_optics.engine.lens import Lens
CA_DIAMETER = 0.01
CONDENSOR_APERATURE = [192.4, 1.5, 1, [0, 0, 0], 'Cond. Apert']
ray = np.array(
    [[0], [(CA_DIAMETER/2) / CONDENSOR_APERATURE[0]]]
)
sample = Lens(528.9, None, None, None, None)
objective = Lens(551.6, 19.67, sample, 3, False)
intermediate = Lens(706.4, 6.498, objective, 3, False)
projective = Lens(826.9, 6, intermediate, False)

def test_transfer_free():
    np.testing.assert_allclose(
        Lens.transfer_free_space(257.03),
        [[1, 257.03], [0, 1]]
    )