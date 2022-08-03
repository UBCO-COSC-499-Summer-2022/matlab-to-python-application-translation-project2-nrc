import os
import numpy as np
from nrcemt.alignment_software.engine.img_io import load_dm3
from nrcemt.alignment_software.engine.img_processing import (
    adjust_img_range, reject_outliers_percentile
)

from nrcemt.alignment_software.engine.particle_tracking import (
    ParticlePositionContainer, create_particle_mask, particle_search
)

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


def test_particle_search():
    # create a particle mask to use
    mask = create_particle_mask(20)
    # load the image and perform contrast adjsutments
    img = load_dm3(filename)
    contrast = reject_outliers_percentile(img, 2.0)
    img = adjust_img_range(img, contrast[0], contrast[1], 0, 1)
    img = np.clip(img, 0, 1)
    # perform a search for a particle 1
    search_location = (560, 500)
    search_size = (120, 120)
    assert (
        particle_search(img, mask, search_location, search_size) == (563, 476)
    )
    # perform another search for a particle 1, but with diff parameters
    search_location = (540, 490)
    search_size = (100, 100)
    assert (
        particle_search(img, mask, search_location, search_size) == (563, 476)
    )
    # perform a search for a particle 2
    search_location = (530, 780)
    search_size = (80, 80)
    assert (
        particle_search(img, mask, search_location, search_size) == (521, 770)
    )
    # perform a search for particle 3 near the top edge of the image
    search_location = (600, 20)
    search_size = (120, 120)
    assert (
        particle_search(img, mask, search_location, search_size) == (634, 19)
    )


def test_particle_position_container():
    container = ParticlePositionContainer()
    assert container.frame_count() == 0
    assert container.particle_count() == 0
    container.resize(5, 10)
    assert container.particle_count() == 5
    assert container.frame_count() == 10
    data, partial = container.get_complete()
    np.testing.assert_equal(data, [])
    np.testing.assert_equal(partial, [])
    assert container.get_status(0) == "empty"
    container[1, 2] = (123, 456)
    container[3, 4] = (567, 890)
    data, partial = container.get_complete()
    np.testing.assert_equal(data, [])
    np.testing.assert_equal(partial, [1, 3])
    assert container.get_status(1) == "partial"
    assert container.get_status(3) == "partial"
    assert container.get_position(0, 0) is None
    assert container.get_position(1, 2) == (123, 456)
    assert container.get_position(3, 4) == (567, 890)
    container.reset(1)
    assert container.get_position(1, 2) is None
    assert container.get_position(3, 4) == (567, 890)
    assert container.get_previous_position(3, 8) == (567, 890)
    container.reset_all()
    assert container.get_position(3, 4) is None
    for i in range(10):
        container[1, i] = (i, i)
    data, partial = container.get_complete()
    np.testing.assert_equal(data, [
        [(i, i) for i in range(10)]
    ])
    assert container.get_status(1) == "complete"


def test_particle_interpolation():
    container = ParticlePositionContainer()
    container.resize(1, 5)
    container[0, 0] = (1, 10)
    container[0, 3] = (4, 4)
    container.attempt_interpolation(0)
    assert container.get_position(0, 0) == (1, 10)
    assert container.get_position(0, 1) == (2, 8)
    assert container.get_position(0, 2) == (3, 6)
    assert container.get_position(0, 4) == (5, 2)
