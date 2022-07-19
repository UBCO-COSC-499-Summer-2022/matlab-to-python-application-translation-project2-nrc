import scipy.signal
import numpy as np
from PIL import Image


def create_particle_mask(radius, invert=False):
    """
    Creates a circular mask to probe for the existence of a ciruclar particle.
    By default it a black-on-white mask. Invert=True for white-on-black.
    """

    def mask_value(x, y):
        dx = 1 - (x+1) / radius
        dy = 1 - (y+1) / radius
        dx2 = np.square(dx)
        dy2 = np.square(dy)
        magnitude = np.square(np.clip(dx2+dy2, 0, 1))
        if invert:
            return 1 - magnitude
        else:
            return magnitude

    return np.fromfunction(mask_value, (2*radius-1, 2*radius-1))


def particle_search(img, particle_mask, search_location, search_size):
    """
    Finds a particle in the vicinity of a search location.
    img: the image to serach in
    particle_mask: a mask in the shape of the particle to detect.
    search_location: the center of the search location of the image.
    search_size: the width and height of the search area.
    """

    height, width = img.shape
    # calculate crop centered on search location
    left = int(search_location[0] - search_size[0] / 2)
    right = int(search_location[0] + search_size[0] / 2)
    top = int(search_location[1] - search_size[1] / 2)
    bottom = int(search_location[1] + search_size[1] / 2)
    # make sure crop is not out of bounds
    if left < 0:
        left = 0
    if right >= width:
        right = width - 1
    if top < 0:
        top = 0
    if bottom >= height:
        bottom = height - 1
    # perform crop
    img_crop = np.array(Image.fromarray(img).crop((left, top, right, bottom)))
    # map both filter and image onto the range [-0.5, 0.5]
    img_crop -= 0.5
    particle_mask = particle_mask - 0.5
    # convolve cropped search area with the particle mask
    img_filtered = scipy.signal.convolve2d(
        img_crop, particle_mask, mode="valid"
    )
    # find most-likely location in filtered image
    filtered_y, filtered_x = np.unravel_index(
        img_filtered.argmax(), img_filtered.shape
    )
    # convert coordinates to location in cropped image
    cropped_x = filtered_x + particle_mask.shape[1] / 2
    cropped_y = filtered_y + particle_mask.shape[0] / 2
    # convert coordinates to location in original image
    location_x = int(cropped_x + left)
    location_y = int(cropped_y + top)
    return location_x, location_y


class ParticleLocationSeries:
    """
    A container that contains the locations of particle over a sequence
    of frames.
    """

    def __init__(self, frame_count):
        if frame_count <= 0:
            raise ValueError("frame count must greater than zero")
        self.locations = [None for i in range(frame_count)]
        self.first_frame = 0
        self.last_frame = frame_count - 1

    def __getitem__(self, frame_index):
        return self.locations[frame_index]

    def __setitem__(self, frame_index, location):
        if frame_index >= self.first_frame and frame_index <= self.last_frame:
            self.locations[frame_index] = location
        else:
            raise IndexError("particle frame index out of bounds")

    def __len__(self):
        return len(self.locations)

    def get_first_frame(self):
        return self.first_frame

    def get_last_frame(self):
        return self.last_frame

    def set_first_frame(self, first_frame):
        if first_frame > self.last_frame:
            self.last_frame = len(self) - 1
        if first_frame < 0:
            raise ValueError("first frame must zero or greater")
        self.first_frame = first_frame

    def set_last_frame(self, last_frame):
        if self.first_frame > last_frame:
            raise ValueError("last frame index must not be less than first")
        if self.last_frame >= len(self):
            raise ValueError("last frame must less than length")
        self.last_frame = last_frame
        for i in range(last_frame+1, len(self)):
            self.locations[i] = None

    def is_complete(self):
        """returns whether the whole range is populated"""
        for i in range(self.first_frame, self.last_frame+1):
            if self.locations[i] is None:
                return False
        return True

    def to_array(self):
        return np.array(self.locations)
