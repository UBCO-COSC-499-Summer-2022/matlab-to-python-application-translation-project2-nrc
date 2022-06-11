import os
import hashlib
from tempfile import TemporaryFile
import numpy as np
from nrcemt.alignment_software.engine.dm3 import DM3Image

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'resources/image_001.dm3')


def test_dm3_reading():
    """Reads and example DM3 file and verifies important fields from it."""
    with open(filename, 'rb') as dm3_file:
        dm3_img = DM3Image.read(dm3_file)
        assert dm3_img.version == 3
        assert dm3_img.is_little_endian
        assert dm3_img.size == 4_799_093
        dim = dm3_img.tag_group["ImageList"][0]["ImageData"]["Dimensions"]
        assert dim[0].decode() == 384
        assert dim[1].decode() == 384
        img = dm3_img.tag_group["ImageList"][0]["ImageData"]["Data"].decode()
        assert img.size == 384*384
        assert img.dtype == np.int32
        img_hash = hashlib.sha256(img.data.tobytes()).hexdigest()
        assert (
            img_hash ==
            "57c9d6ad22881e139e9594ce6cffa30a63c3e62b8e13f9729d4f6856e0e85bac"
        )


def test_dm3_rewriting():
    """Reads and rewrites a DM3 file, and verifies is hasn't changed."""
    with TemporaryFile('w+b') as tempfile:
        with open(filename, 'rb') as dm3_file:
            original_hash = compute_file_sha256(dm3_file)
            dm3_img = DM3Image.read(dm3_file)
            dm3_img.write(tempfile)
            rewritten_hash = compute_file_sha256(tempfile)
            assert original_hash == rewritten_hash


def test_dm3_rewriting_new_data():
    """Reads and rewrites a DM3 file with new image data, and verifies it."""
    with TemporaryFile('w+b') as tempfile:
        with open(filename, 'rb') as dm3_file:
            dm3_img = DM3Image.read(dm3_file)
            img_data = dm3_img.tag_group["ImageList"][0]["ImageData"]["Data"]
            # create a random 384x384 int32 array of bytes to store
            img_data.data_bytes = os.urandom(384*384*4)
            dm3_img.write(tempfile)
            # reread the temp file and verify its image data
            tempfile.seek(0)
            rewritten_img_data = (
                DM3Image.read(tempfile)
                .tag_group["ImageList"][0]["ImageData"]["Data"]
            )
            assert rewritten_img_data.data_bytes == img_data.data_bytes


# utility function used to check the equivalence of files
def compute_file_sha256(file):
    file.seek(0)
    sha256 = hashlib.sha256()
    while True:
        data = file.read(65536)
        if not data:
            break
        sha256.update(data)
    file.seek(0)
    return sha256.hexdigest()
