import os
import hashlib
import numpy as np
from tempfile import TemporaryDirectory
from alignment_software.engine.img_io import (
    load_dm3,
    load_float_tiff,
    rewrite_dm3,
    save_float_tiff
)


dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'resources/image_001.dm3')


def test_load_dm3():
    img = load_dm3(filename)
    assert img.shape == (1024, 1024)
    img_hash = compute_bytes_sha256(img.tobytes())
    assert (
        img_hash ==
        "ca25e893b60460a8f1b745ac7e4cf9a3f9ab049900fa8f72bc537e06873af2d6"
    )


def test_rewrite_dm3():
    with TemporaryDirectory() as tempdir:
        tempfilename = os.path.join(tempdir, "test.dm3")
        img_data = np.random.randint(0, 1_000_000, (1024, 1024), np.uint32)
        rewrite_dm3(filename, tempfilename, img_data)
        img_data_rewritten = load_dm3(tempfilename)
        np.testing.assert_equal(img_data, img_data_rewritten)


def test_save_and_load_float_tiff():
    with TemporaryDirectory() as tempdir:
        tempfilename = os.path.join(tempdir, "test.tiff")
        img_original = np.array([[0.1, 0.5, 0.0], [0.2, 0.3, 1.0]])
        save_float_tiff(tempfilename, img_original)
        img_loaded = load_float_tiff(tempfilename)
        assert np.allclose(img_original, img_loaded)


def compute_bytes_sha256(byte_string):
    sha256 = hashlib.sha256()
    sha256.update(byte_string)
    return sha256.hexdigest()
