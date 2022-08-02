import math
import scipy.signal
import scipy.interpolate
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


class ParticlePositionContainer:

    def __init__(self, array=None):
        if array is not None:
            self.array = array.astype(np.float64)
        else:
            self.array = np.empty((0, 0, 2), dtype=np.float64)

    def resize(self, particle_count, frame_count):
        particle_pad = particle_count - self.particle_count()
        particle_pad = 0 if particle_pad < 0 else particle_pad
        frame_pad = frame_count - self.frame_count()
        frame_pad = 0 if frame_pad < 0 else frame_pad
        padded_array = np.pad(
            self.array, ((0, particle_pad), (0, frame_pad), (0, 0)),
            mode="constant", constant_values=np.nan
        )
        self.array = np.resize(padded_array, (particle_count, frame_count, 2))

    def replace(self, array):
        self.array = array.astype(np.float64)

    def get_position(self, particle_index, frame_index):
        x, y = self.array[particle_index, frame_index]
        if np.any(np.isnan([x, y])):
            return None
        else:
            return (x, y)

    def __getitem__(self, index):
        return self.array[index]

    def __setitem__(self, index, value):
        self.array[index] = value

    def particle_count(self):
        return self.array.shape[0]

    def frame_count(self):
        return self.array.shape[1]

    def trim(self, i, end_frame):
        self.array[i, end_frame+1:] = np.nan

    def reset(self, i):
        self.array[i, :] = np.nan

    def reset_all(self):
        self.array[:] = np.nan

    def get_complete(self):
        complete_arrays = []
        partial_indices = []
        for i, particle in self.array:
            is_nan = np.isnan(particle)
            some_not_nan = ~np.all(is_nan)
            all_not_nan = np.all(~is_nan)
            partial_nan = some_not_nan and not all_not_nan
            if all_not_nan:
                complete_arrays.append(particle)
            elif partial_nan:
                partial_indices.append(i)
        return np.array(complete_arrays), np.array(partial_indices)

    def attempt_interpolation(self, i):
        try:
            particle = self.array[i]
            nan_interpolation(particle[:, 0])
            nan_interpolation(particle[:, 1])
            return True
        except Exception as e:
            print(str(e))
            return False


def nan_interpolation(array):
    is_nan = np.isnan(array)
    x = np.argwhere(~is_nan).ravel()
    y = [array[i] for i in x]
    interpolation_func = scipy.interpolate.interp1d(
        x, y, kind="quadratic", fill_value="extrapolate"
    )
    for missing in np.argwhere(is_nan):
        array[missing] = interpolation_func(missing)


# class ParticleLocationSeries:
#     """
#     A container that contains the locations of particle over a sequence
#     of frames.
#     """

#     def __init__(self, frame_count, locations=None):
#         if frame_count <= 0:
#             raise ValueError("frame count must greater than zero")
#         if locations is not None:
#             self.locations = locations
#         else:
#             self.locations = [None for i in range(frame_count)]
#         self.first_frame = 0
#         self.last_frame = frame_count - 1

#     def __getitem__(self, frame_index):
#         return self.locations[frame_index]

#     def __setitem__(self, frame_index, location):
#         if frame_index >= self.first_frame and frame_index <= self.last_frame:
#             self.locations[frame_index] = location
#         else:
#             raise IndexError("particle frame index out of bounds")

#     def __len__(self):
#         return len(self.locations)

#     def get_first_frame(self):
#         return self.first_frame

#     def get_last_frame(self):
#         return self.last_frame

#     def set_first_frame(self, first_frame):
#         if first_frame > self.last_frame:
#             self.last_frame = len(self) - 1
#         if first_frame < 0:
#             raise ValueError("first frame must zero or greater")
#         self.first_frame = first_frame

#     def set_last_frame(self, last_frame):
#         if self.first_frame > last_frame:
#             raise ValueError("last frame index must not be less than first")
#         if self.last_frame >= len(self):
#             raise ValueError("last frame must less than length")
#         self.last_frame = last_frame
#         for i in range(last_frame+1, len(self)):
#             self.locations[i] = None

#     def attempt_interpolation(self):
#         if self.is_complete():
#             return
#         known_i = []
#         known_x = []
#         known_y = []
#         for i, location in enumerate(self.locations):
#             if location is not None:
#                 x, y = location
#                 known_i.append(i)
#                 known_x.append(x)
#                 known_y.append(y)
#         try:
#             func_x = scipy.interpolate.interp1d(
#                 known_i, known_x, kind="slinear", fill_value="extrapolate"
#             )
#             func_y = scipy.interpolate.interp1d(
#                 known_i, known_y, kind="slinear", fill_value="extrapolate"
#             )
#         except ValueError:
#             return False
#         for i, location in enumerate(self.locations):
#             if location is None:
#                 self.locations[i] = (int(func_x(i)), int(func_y(i)))
#         return True

#     def is_complete(self):
#         """returns whether the whole range is populated"""
#         for location in self.locations:
#             if location is None:
#                 return False
#         return True

#     def to_array(self):
#         return np.array(self.locations)
