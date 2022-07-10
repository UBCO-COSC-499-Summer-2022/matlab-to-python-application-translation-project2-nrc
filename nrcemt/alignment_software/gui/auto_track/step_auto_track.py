from nrcemt.alignment_software.engine.particle_tracking import ParticleLocationSeries, create_particle_mask
from .window_auto_track import AutoTrackWindow


MAX_PARTICLES = 13


class AutoTrackStep:

    def __init__(self, main_window, coarse_align_step):
        self.main_window = main_window
        self.coarse_align_step = coarse_align_step
        self.auto_track_window = None
        self.particle_locations = None
        self.tracking_locations = None
        self.properties = {
            "search_size": (80, 80),
            "marker_radius": 20
        }

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
        self.auto_track_window.properties.set_properties(self.properties)
        self.auto_track_window.table.set_mark_end_command(self.mark_end)
        self.auto_track_window.properties.set_command(self.update_properties)

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
        self.auto_track_window.table.update_data(
            self.particle_locations, i
        )

    def render_markers(self, i):
        search_size = self.properties["search_size"]
        marker_radius = self.properties["marker_radius"]
        # TODO: avoid this call to create_particle_mask
        marker_size = create_particle_mask(marker_radius).shape
        for p, particle in enumerate(self.particle_locations):
            particle_location = particle[i]
            if particle_location is not None:
                self.main_window.image_frame.render_point(
                    particle_location, "#03a9f4"
                )
            if particle.get_first_frame() == i:
                tracking_location = self.tracking_locations[p]
                if tracking_location is not None:
                    self.main_window.image_frame.render_rect(
                        tracking_location, search_size, "#ff9800"
                    )
                    self.main_window.image_frame.render_rect(
                        tracking_location, marker_size, "#8bc34a"
                    )

    def update_properties(self):
        self.properties = self.auto_track_window.properties.get_properties()
        self.select_image(self.main_window.selected_image())

    def mark_end(self, particle_index):
        selected_image = self.main_window.selected_image()
        particle = self.particle_locations[particle_index]
        particle.set_last_frame(selected_image)
        self.select_image(selected_image)

    def canvas_click(self, x, y):
        selected_image = self.main_window.selected_image()
        selected_particle = (
            self.auto_track_window.table.get_selected_particle()
        )
        self.tracking_locations[selected_particle] = (x, y)
        particle = self.particle_locations[selected_particle]
        particle.set_first_frame(selected_image)
        self.auto_track_window.table.enable_tracking(selected_particle)
        self.select_image(selected_image)

    def reset(self):
        self.particle_locations = None

    def is_ready(self):
        return self.contrast_step.is_ready()