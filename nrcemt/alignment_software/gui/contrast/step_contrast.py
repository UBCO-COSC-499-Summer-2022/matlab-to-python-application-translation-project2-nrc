from .window_contrast import ContrastWindow


class ContrastStep:

    def __init__(self, main_window, loading_step):
        self.main_window = main_window
        self.loading_step = loading_step
        self.reset()

    def open(self, close_callback):
        self.contrast_window = ContrastWindow(self.main_window)

        def close():
            self.contrast_window.destroy()
            close_callback(reset=True)

        self.contrast_window.protocol("WM_DELETE_WINDOW", close)

    def load_image(self, i):
        unprocessed_image = self.loading_step.load_image(i)
        return unprocessed_image

    def select_image(self, i):
        image = self.load_image(i)
        self.main_window.image_frame.render_image(image)
        self.contrast_window.histogram.render_histogram(image)

    def reset(self):
        self.contrast_ranges = None

    def is_ready(self):
        return self.loading_step.is_ready()
