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