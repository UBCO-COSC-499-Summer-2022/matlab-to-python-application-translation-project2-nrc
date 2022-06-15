from .dm3 import DM3Image


def load_dm3(filename):
    """
    Loads just the image data form a DM3 file as a 2D numpy array.
    Other image metadata included in the DM3 file format is ignored.
    """
    with open(filename, 'rb') as file:
        img = DM3Image.read(file)
        img_data = img.tag_group["ImageList"][0]["ImageData"]
        width = img_data["Dimensions"][0].decode()
        height = img_data["Dimensions"][1].decode()
        array = img_data["Data"].decode()
        return array.reshape((width, height))
