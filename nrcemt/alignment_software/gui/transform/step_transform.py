from nrcemt.alignment_software.engine.img_processing import convert_img_float64, resize_img, sobel_filter_img, transform_img, combine_tranforms, rotation_transform, scale_transform, transform_img, translation_transform
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

    def load_image(self, i):
        return self.contrast_step.load_image(i)

    def select_image(self, i):
        image = self.load_image(i)
        transform = self.get_transform_matrix(i)
        image = transform_img(image, transform)
        image = resize_img(image, 1 / self.transform['binning'])
        self.main_window.image_frame.render_image(image, 0.0, 1.0)

    def update_transform(self):
        self.transform = self.transform_window.get_tranform()
        self.select_image(self.main_window.selected_image())

    def get_transform_matrix(self, i):
        width, height = self.load_image(i).shape
        center_x = width / 2
        center_y = height / 2
        offset_x = self.transform['offset_x'] / 100 * width
        offset_y = self.transform['offset_y'] / 100 * height
        translation = translation_transform(offset_x, offset_y)
        scale = scale_transform(self.transform['scale'], center_x, center_y)
        rotate = rotation_transform(self.transform['angle'], center_x, center_y)
        return combine_tranforms(scale, rotate, translation)

    def reset(self):
        pass

    def is_ready(self):
        return self.contrast_step.is_ready()
