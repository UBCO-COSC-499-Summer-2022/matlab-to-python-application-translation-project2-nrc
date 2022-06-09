import os
import hashlib
import numpy as np
from nrcemt.alignment_software.engine.dm3 import DM3Image

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'resources/image_001.dm3')


def test_dm3_reading():
    with open(filename, 'rb') as file:
        dm3_img = DM3Image.read(file)
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
