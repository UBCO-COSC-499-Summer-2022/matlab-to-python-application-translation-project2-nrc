import os

import numpy as np

from nrcemt.alignment_software.engine.csv_io import load_marker_csv

dirname = os.path.dirname(__file__)
marker_filename = os.path.join(dirname, 'resources/marker_data.csv')


def test_load_marker_csv():
    """Loads marker data from a csv, frames are rows, 2 columns per marker."""
    markers = load_marker_csv(marker_filename)
    assert markers.shape == (5, 61, 2)
    np.testing.assert_equal(markers[0][0], [534, 851])
    np.testing.assert_equal(markers[0][1], [529, 850])
    np.testing.assert_equal(markers[0][2], [519, 850])
    np.testing.assert_equal(markers[1][0], [443, 726])
