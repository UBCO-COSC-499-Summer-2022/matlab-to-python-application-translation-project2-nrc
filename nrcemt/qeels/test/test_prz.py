import os
import hashlib
from nrcemt.qeels.engine.spectrogram import load_prz, process_spectrogram

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'resources/1_qEELS_1deg_sum.prz')


def test_load_prz():
    # Load file
    img = load_prz(filename)

    # Verifying image data
    img_hash = hashlib.sha256(img).hexdigest()
    assert (
        img_hash ==
        "b4767ed885d933a99c8701ade22cd73e211e9443a6b0e574d2b43ab093d433fc"
    )

    # Confirms correct image size
    assert img.shape == (1024, 1024)


def test_process_prz():
    img = load_prz(filename)
    img_processed = process_spectrogram(img)
    img_hash = hashlib.sha256(img_processed).hexdigest()
    assert(
        img_hash ==
        "6e33b3c08b33a96a3efaf3bb9d66667e63f2eef822fe9c58260096d7516a323c"
    )
