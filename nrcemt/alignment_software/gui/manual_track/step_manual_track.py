import os
from nrcemt.alignment_software.engine.csv_io import (
    write_marker_csv
)
from .window_manual_track import ManualTrackWindow


MAX_PARTICLES = 13


class ManualTrackStep:

    def __init__(
        self, main_window, loading_step, coarse_align_step, particle_positions
    ):
        self.main_window = main_window
        self.loading_step = loading_step
        self.coarse_align_step = coarse_align_step
        self.manual_track_window = None
        self.particle_positions = particle_positions

    def open(self, close_callback):
        self.particle_positions.resize(MAX_PARTICLES, self.image_count())

        self.manual_track_window = ManualTrackWindow(
            self.main_window, MAX_PARTICLES
        )

        # cleanup
        def close():
            self.save()
            self.manual_track_window.destroy()
            self.manual_track_window = None
            close_callback(reset=True)
        self.manual_track_window.protocol("WM_DELETE_WINDOW", close)

    def save(self):
        marker_csv = os.path.join(
            self.loading_step.get_output_path(),
            "marker_data.csv"
        )
        write_marker_csv(marker_csv, self.particle_positions.array)

    def load_image(self, i):
        return self.coarse_align_step.load_image(i)

    def image_count(self):
        return self.coarse_align_step.image_count()

    def select_image(self, i):
        image = self.load_image(i)
        self.main_window.image_frame.render_image(image)
        self.render_markers(i)
        self.main_window.image_frame.update()

    def render_markers(self, i):
        for p in range(self.particle_positions.particle_count()):
            particle_position = self.particle_positions.get_position(p, i)
            if particle_position is not None:
                self.main_window.image_frame.render_point(
                    particle_position, "#03a9f4"
                )
                self.main_window.image_frame.render_text(
                    particle_position, p+1
                )

    def canvas_click(self, x, y):
        print(x, y)

    def reset_all(self):
        self.particle_positions.reset_all()

    def reset_particle(self, particle_index):
        self.particle_positions.reset(particle_index)
