from .window_auto_track import AutoTrackWindow


class AutoTrackStep:

    def __init__(self, main_window, coarse_align_step):
        self.main_window = main_window
        self.coarse_align_step = coarse_align_step
        self.transform_window = None

    def open(self, close_callback):
        self.transform_window = AutoTrackWindow(self.main_window)

        def close():
            self.transform_window.destroy()
            self.transform_window = None
            close_callback(reset=True)

        self.transform_window.protocol("WM_DELETE_WINDOW", close)

    def load_image(self, i):
        return self.coarse_align_step.load_image(i)

    def image_count(self):
        return self.coarse_align_step.image_count()

    def select_image(self, i):
        image = self.load_image(i)
        self.main_window.image_frame.render_image(image, 0.0, 1.0)

    def canvas_click(self, x, y):
        self.main_window.image_frame.render_rect((x, y), (80, 80))
        # self.main_window.image_frame.render_point(x, y, "foo")
        self.main_window.image_frame.update()

    def reset(self):
        pass

    def is_ready(self):
        return self.contrast_step.is_ready()
