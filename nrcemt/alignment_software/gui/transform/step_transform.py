from nrcemt.alignment_software.engine.img_processing import (
    no_transform,
    resize_img,
    combine_tranforms,
    rotate_transform,
    scale_transform,
    transform_img,
    translate_transform
)
from nrcemt.common.gui.async_handler import AsyncHandler
from .window_transform import TransformWindow


class TransformStep:

    def __init__(self, main_window, contrast_step):
        self.main_window = main_window
        self.contrast_step = contrast_step
        self.transform_window = None
        self.transform = {
            "offset_x": 0,
            "offset_y": 0,
            "angle": 0,
            "scale": 100,
            "binning": 1,
            "sobel": False
        }

    def open(self, close_callback):
        self.transform_window = TransformWindow(self.main_window)
        self.transform_window.set_command(AsyncHandler(self.update_transform))
        self.transform_window.set_transform(self.transform)

        def close():
            self.transform_window.destroy()
            self.transform_window = None
            close_callback(reset=True)

        self.transform_window.protocol("WM_DELETE_WINDOW", close)

    def load_image(self, i):
        image = self.contrast_step.load_image(i)
        image = resize_img(image, 1 / self.transform['binning'])
        return image

    def image_count(self):
        return self.contrast_step.image_count()

    def select_image(self, i):
        image = self.load_image(i)
        transform = self.get_transform(i)
        image = transform_img(image, transform)
        self.main_window.image_frame.render_image(image)
        self.main_window.image_frame.update()

    def update_transform(self):
        self.transform = self.transform_window.get_tranform()
        self.select_image(self.main_window.selected_image())

    def get_transform(self, i):
        if self.transform is None:
            return no_transform()
        width, height = self.load_image(i).shape
        center_x = width / 2
        center_y = height / 2
        offset_x = self.transform['offset_x'] / 100 * width
        offset_y = self.transform['offset_y'] / 100 * height
        translation = translate_transform(offset_x, offset_y)
        scale = scale_transform(self.transform['scale'], center_x, center_y)
        rotate = rotate_transform(self.transform['angle'], center_x, center_y)
        return combine_tranforms(scale, rotate, translation)

    def reset(self):
        pass

    def is_ready(self):
        return self.contrast_step.is_ready()
