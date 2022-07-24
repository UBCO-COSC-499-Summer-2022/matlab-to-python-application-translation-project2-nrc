from .window_optimization import OptimizationWindow


class OptimizationStep:

    def __init__(self, main_window, loading_step, auto_track_step):
        self.main_window = main_window
        self.loading_step = loading_step
        self.auto_track_step = auto_track_step

    def open(self, close_callback):
        self.optimization_window = OptimizationWindow(self.main_window)

        def close():
            self.optimization_window.destroy()
            self.optimization_window = None
            close_callback(reset=True)

        self.optimization_window.protocol("WM_DELETE_WINDOW", close)

        self.optimization_window.optimize_button.config(
            command=self.perform_optimization
        )

    def load_image(self, i):
        image = self.loading_step.load_image(i)
        return image

    def image_count(self):
        return self.loading_step.image_count()

    def select_image(self, i):
        image = self.loading_step.load_image(i)
        self.main_window.image_frame.render_image(image, None, None)
        self.main_window.image_frame.update()

    def perform_optimization(self):
        pass
