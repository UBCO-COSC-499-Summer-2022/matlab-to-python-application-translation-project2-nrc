import scipy.ndimage
import scipy.linalg
import numpy as np
from nrcemt.common.gui.async_handler import AsyncHandler
from .window_transform import TranformWindow


class TransformStep:

    def __init__(self, main_window, contrast_step):
        self.main_window = main_window
        self.contrast_step = contrast_step
        self.transform_window = None
        self.transform = None

    def open(self, close_callback):
        self.transform_window = TranformWindow(self.main_window)
        self.transform_window.set_command(AsyncHandler(self.update_transform))

        def close():
            self.transform_window.destroy()
            self.transform_window = None
            close_callback(reset=True)

        self.transform_window.protocol("WM_DELETE_WINDOW", close)

    def select_image(self, i):
        image = self.contrast_step.load_image(i)
        matrix = self.get_transform_matrix(i)
        matrix = scipy.linalg.inv(matrix)
        image = scipy.ndimage.affine_transform(image, matrix)
        self.main_window.image_frame.render_image(image, 0.0, 1.0)

    def update_transform(self):
        self.transform = self.transform_window.get_tranform()
        self.select_image(self.main_window.selected_image())

    def get_transform_matrix(self, i):
        width, height = self.contrast_step.load_image(i).shape
        offset_x = self.transform['offset_x'] / 100 * width
        offset_y = self.transform['offset_y'] / 100 * height
        translation_matrix = [
            [1, 0, offset_y],
            [0, 1, offset_x],
            [0, 0, 1]
        ]
        scale = self.transform['scale'] / 100
        scale_matrix = [
            [scale, 0, 0],
            [0, scale, 0],
            [0, 0, 1]
        ]
        return np.matmul(translation_matrix, scale_matrix)

    def reset(self):
        pass

    def is_ready(self):
        return self.contrast_step.is_ready()
