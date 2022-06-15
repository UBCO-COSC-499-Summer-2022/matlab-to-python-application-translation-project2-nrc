import os
import hashlib
from nrcemt.qeels.engine.prz import load_prz

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'resources/1_qEELS_1deg_sum.prz')


def test_load_prz():
    # Load file
    img = load_prz(filename)

    # Verifying image data
    img_hash = hashlib.sha256(img['data']).hexdigest()
    assert (
        img_hash ==
        "b4767ed885d933a99c8701ade22cd73e211e9443a6b0e574d2b43ab093d433fc"
    )

    # Confirm reads everything
    assert len(img) == 4

    # Confirms correct image size
    assert len(img['data']) == 1024

    # Check file version
    assert img['file_format_version'] == 3
