import os
import hashlib
from nrcemt.alignment_software.engine.img_io import load_dm3


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'resources/image_001.dm3')


def test_dm3_reading():
    img = load_dm3(filename)
    assert img.shape == (1024, 1024)
    img_hash = compute_bytes_sha256(img.tobytes())
    assert (
        img_hash ==
        "ca25e893b60460a8f1b745ac7e4cf9a3f9ab049900fa8f72bc537e06873af2d6"
    )


def compute_bytes_sha256(byte_string):
    sha256 = hashlib.sha256()
    sha256.update(byte_string)
    return sha256.hexdigest()
