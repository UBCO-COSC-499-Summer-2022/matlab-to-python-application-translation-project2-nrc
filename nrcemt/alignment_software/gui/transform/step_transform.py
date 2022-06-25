from .window_transform import TranformWindow


class TransformStep:

    def __init__(self, main_window, contrast_step):
        self.main_window = main_window
        self.contrast_step = contrast_step
        self.transform_window = None

    def open(self, close_callback):
        width, height = self.contrast_step.load_image(0).shape
        self.transform_window = TranformWindow(self.main_window, width, height)

        def close():
            self.transform_window.destroy()
            self.transform_window = None
            close_callback(reset=True)

        self.transform_window.protocol("WM_DELETE_WINDOW", close)

    def select_image(self, i):
        image = self.contrast_step.load_image(i)
        self.main_window.image_frame.render_image(image)

    def reset(self):
        pass

    def is_ready(self):
        return self.contrast_step.is_ready()
