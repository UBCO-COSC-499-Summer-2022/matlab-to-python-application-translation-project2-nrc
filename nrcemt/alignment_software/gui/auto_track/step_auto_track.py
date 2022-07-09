from nrcemt.alignment_software.engine.particle_tracking import ParticleLocationSeries
from .window_auto_track import AutoTrackWindow


MAX_PARTICLES = 13


class AutoTrackStep:

    def __init__(self, main_window, coarse_align_step):
        self.main_window = main_window
        self.coarse_align_step = coarse_align_step
        self.auto_track_window = None
        self.particle_locations = None
        self.tracking_locations = None

    def open(self, close_callback):
        if self.particle_locations is None:
            self.particle_locations = [
                ParticleLocationSeries(self.image_count())
                for i in range(MAX_PARTICLES)
            ]
            self.tracking_locations = [None for i in range(MAX_PARTICLES)]
            self.tracking_locations[0] = (100, 100)
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
        for p, particle in enumerate(self.particle_locations):
            particle_location = particle[i]
            if particle_location is not None:
                self.main_window.image_frame.render_point(particle_location)
            if particle.get_first_frame() == i:
                tracking_location = self.tracking_locations[p]
                if tracking_location is not None:
                    self.main_window.image_frame.render_rect(
                        tracking_location, (80, 80)
                    )

    def canvas_click(self, x, y):
        selected_image = self.main_window.selected_image()
        selected_particle = self.auto_track_window.get_selected_particle()
        self.tracking_locations[selected_particle] = (x, y)
        particle = self.particle_locations[selected_particle]
        particle.set_first_frame(selected_image)
        self.select_image(selected_image)

    def reset(self):
        self.particle_locations = None

    def is_ready(self):
        return self.contrast_step.is_ready()
