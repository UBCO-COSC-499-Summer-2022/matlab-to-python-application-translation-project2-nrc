import os
import hashlib
from nrcemt.alignment_software.engine.img_loading import load_dm3


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'resources/image_001.dm3')


def test_dm3_reading():
    img = load_dm3(filename)
    assert img.shape == (384, 384)
    img_hash = compute_bytes_sha256(img.tobytes())
    assert (
        img_hash ==
        "57c9d6ad22881e139e9594ce6cffa30a63c3e62b8e13f9729d4f6856e0e85bac"
    )


def compute_bytes_sha256(byte_string):
    sha256 = hashlib.sha256()
    sha256.update(byte_string)
    return sha256.hexdigest()
