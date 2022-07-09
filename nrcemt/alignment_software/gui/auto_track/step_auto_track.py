from nrcemt.alignment_software.engine.particle_tracking import ParticleLocationSeries
from .window_auto_track import AutoTrackWindow


MAX_PARTICLES = 13


class AutoTrackStep:

    def __init__(self, main_window, coarse_align_step):
        self.main_window = main_window
        self.coarse_align_step = coarse_align_step
        self.auto_track_window = None
        self.particle_locations = None

    def open(self, close_callback):
        if self.particle_locations is None:
            self.particle_locations = [
                ParticleLocationSeries(self.image_count())
                for i in range(MAX_PARTICLES)
            ]
            self.particle_locations[0][0] = (100, 100)
            self.particle_locations[0][1] = (110, 120)
            self.particle_locations[0][2] = (120, 140)

        self.auto_track_window = AutoTrackWindow(
            self.main_window, MAX_PARTICLES
        )

        def close():
            self.auto_track_window.destroy()
            self.auto_track_window = None
            close_callback(reset=True)

        self.auto_track_window.protocol("WM_DELETE_WINDOW", close)

    def load_image(self, i):
        return self.coarse_align_step.load_image(i)

    def image_count(self):
        return self.coarse_align_step.image_count()

    def select_image(self, i):
        image = self.load_image(i)
        self.main_window.image_frame.render_image(image, 0.0, 1.0)
        self.render_markers(i)
        self.main_window.image_frame.update()

    def render_markers(self, i):
        for particle in self.particle_locations:
            location = particle[i]
            if location is None:
                continue
            if particle.get_first_frame() == i:
                self.main_window.image_frame.render_rect(location, (80, 80))
            else:
                self.main_window.image_frame.render_point(location)

    def canvas_click(self, x, y):
        self.main_window.image_frame.render_rect((x, y), (80, 80))
        # self.main_window.image_frame.render_point(x, y, "foo")
        self.main_window.image_frame.update()

    def reset(self):
        self.particle_locations = None

    def is_ready(self):
        return self.contrast_step.is_ready()
