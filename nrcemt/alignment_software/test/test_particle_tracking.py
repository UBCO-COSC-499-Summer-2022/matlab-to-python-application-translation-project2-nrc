import os
import numpy as np
from nrcemt.alignment_software.engine.img_io import load_dm3
from nrcemt.alignment_software.engine.img_processing import (
    adjust_img_range, reject_outliers_percentile
)

from nrcemt.alignment_software.engine.particle_tracking import (
    ParticleLocationSeries, create_particle_mask, particle_search
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


def test_particle_location_series():
    # series with 5 frames
    series = ParticleLocationSeries(5)
    assert len(series) == 5
    assert series.get_first_frame() == 0
    assert series.get_last_frame() == 4
    for i in range(5):
        assert series[i] is None
    assert not series.is_complete()
    series[0] = (123, 456)
    assert series[0] == (123, 456)
    assert not series.is_complete()
    series[1] = (678, 321)
    series[2] = (987, 436)
    series[3] = (543, 222)
    assert not series.is_complete()
    series[4] = (543, 214)
    assert series.is_complete()
    assert len(series) == 5
    series.set_first_frame(2)
    assert series[0] == (123, 456)
    assert series[1] == (678, 321)
    assert series[2] == (987, 436)
    assert series.get_first_frame() == 2
    assert series.get_last_frame() == 4
    series.set_last_frame(3)
    assert series[4] is None


def test_particle_interpolation():
    series = ParticleLocationSeries(5, [(1, 10), None, None, (4, 4), None])
    series.attempt_interpolation()
    assert series[0] == (1, 10)
    assert series[1] == (2, 7)
    assert series[2] == (3, 6)
    assert series[4] == (5, 2)
