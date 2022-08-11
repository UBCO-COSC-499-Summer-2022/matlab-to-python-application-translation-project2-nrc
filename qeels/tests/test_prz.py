import os
import hashlib
import numpy as np
from qeels.engine.spectrogram import (
    load_spectrogram,
    process_spectrogram
)

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'resources/1_qEELS_1deg_sum_revised.prz')


def test_load_prz():
    # Load file
    img = load_spectrogram(filename)

    # Verifying image data
    img_hash = hashlib.sha256(img).hexdigest()
    assert (
        img_hash ==
        "8307a4ba8a65c728df11667bbba785acbf92c04cffb27387cef0d1d17d63f257"
    )

    # Confirms correct image size
    assert img.shape == (1024, 1024)


def test_process_prz():
    # Create a 4x4 array
    img = np.array([
        [3, 1, 4, 5],
        [5, 3, 1, 6],
        [9, 1, 6, 4],
        [1, 4, 2, 8]
    ])

    # Expected results
    expected = np.array([
        [1.38629436, 0.693147, 1.60943791, 1.79175947],
        [1.79175947, 1.38629436, 0.693147, 1.94591015],
        [2.30258509, 0.693147, 1.94591015, 1.60943791],
        [0.693147, 1.60943791, 1.09861229, 2.19722458]
    ])

    img_processed = process_spectrogram(img)
    np.testing.assert_allclose(img_processed, expected, rtol=1e-4)
