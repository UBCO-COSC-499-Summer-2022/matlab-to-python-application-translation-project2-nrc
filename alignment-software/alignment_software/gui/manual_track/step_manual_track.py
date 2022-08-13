import os
from tkinter.messagebox import showerror
from alignment_software.engine.csv_io import (
    write_marker_csv
)
from .window_manual_track import ManualTrackWindow


MAX_PARTICLES = 13


class ManualTrackStep:
    """Step that handles manual particle tracking."""

    def __init__(
        self, main_window, loading_step, coarse_align_step, particle_positions
    ):
        """
        Create manual tracking step.
        Depends on loading step to get the output path.
        Depends on coarse alignment to load coarse aligned images.
        Depends on particle positions for shared particle data.
        """
        self.main_window = main_window
        self.loading_step = loading_step
        self.coarse_align_step = coarse_align_step
        self.manual_track_window = None
        self.particle_positions = particle_positions
        self.selected_particle = None

    def open(self, close_callback):
        """Opens the step and calls close_callback when done."""

        self.selected_particle = 0
        self.particle_positions.resize(MAX_PARTICLES, self.image_count())

        self.manual_track_window = ManualTrackWindow(
            self.main_window, MAX_PARTICLES,
            self.select_particle, self.interpolate, self.move,
            self.delete, self.reset
        )
        self.render_graphs()

        # cleanup
        def close():
            self.save()
            self.manual_track_window.destroy()
            self.manual_track_window = None
            close_callback(reset=True)
        self.manual_track_window.protocol("WM_DELETE_WINDOW", close)

    def save(self):
        """Save marker data to csv."""
        marker_csv = os.path.join(
            self.loading_step.get_output_path(),
            "marker_data.csv"
        )
        write_marker_csv(marker_csv, self.particle_positions.array)

    def load_image(self, i):
        """Load image from coarse align step."""
        return self.coarse_align_step.load_image(i)

    def image_count(self):
        """Returns the number of frames in the sequence."""
        return self.coarse_align_step.image_count()

    def select_image(self, i):
        """
        Renders coarse aligned images, along with markers and graphs.
        """
        image = self.load_image(i)
        self.main_window.image_frame.render_image(image)
        self.render_markers()
        self.main_window.image_frame.update()
        if self.manual_track_window is not None:
            self.manual_track_window.adjustment.update_particle_status(
                self.particle_positions
            )
            self.render_graphs()

    def select_particle(self, p):
        """Called when selected particle is updated."""
        self.selected_particle = p
        self.select_image(self.main_window.selected_image())

    def render_markers(self):
        """Renders dots on the image in particle locations."""
        i = self.main_window.selected_image()
        for p in range(self.particle_positions.particle_count()):
            particle_position = self.particle_positions.get_position(p, i)
            if particle_position is not None:
                if self.selected_particle == p:
                    color = "#FFC107"
                else:
                    color = "#03a9f4"
                self.main_window.image_frame.render_point(
                    particle_position, color
                )
                self.main_window.image_frame.render_text(
                    particle_position, p+1
                )

    def render_graphs(self):
        """Render the both x and y position graphs."""
        i = self.main_window.selected_image()
        p = self.selected_particle
        self.manual_track_window.x_position.render(
            self.particle_positions[p, :, 0], i
        )
        self.manual_track_window.y_position.render(
            self.particle_positions[p, :, 1], i
        )

    def canvas_click(self, x, y):
        """Handle click on the image, and update the particle position."""
        i = self.main_window.selected_image()
        p = self.selected_particle
        self.particle_positions[p, i] = (x, y)
        self.select_image(i)

    def move(self, x, y):
        """Called when directional controls are used."""
        i = self.main_window.selected_image()
        p = self.selected_particle
        position = self.particle_positions.get_previous_position(p, i)
        if position is None:
            showerror("Move error", "click the image to indicate a position")
        else:
            px, py = position
            self.particle_positions[p, i] = (px+x, py+y)
            self.select_image(i)

    def delete(self):
        """Deletes current selected particle position."""
        i = self.main_window.selected_image()
        p = self.selected_particle
        self.particle_positions.delete_position(p, i)
        self.select_image(i)

    def reset(self):
        """Resets all positions for selected particle."""
        i = self.main_window.selected_image()
        p = self.selected_particle
        self.particle_positions.reset(p)
        self.select_image(i)

    def interpolate(self, particle_index):
        """Interpolates positions on the selected particle."""
        success = self.particle_positions.attempt_interpolation(
            particle_index, "quadratic"
        )
        if not success:
            showerror("Interpolation error", "interpolation failed")
        else:
            self.select_image(self.main_window.selected_image())

    def focus(self):
        """Brings the optimization window to the top."""
        self.manual_track_window.lift()
