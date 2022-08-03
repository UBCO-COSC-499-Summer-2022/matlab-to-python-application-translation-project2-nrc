from tkinter.messagebox import showerror, showinfo

import os
import numpy as np
from nrcemt.alignment_software.engine.csv_io import (
    load_marker_csv, write_marker_csv
)
from nrcemt.alignment_software.engine.particle_tracking import (
    create_particle_mask,
    particle_search
)
from .window_auto_track import AutoTrackWindow


MAX_PARTICLES = 13


class AutoTrackStep:

    def __init__(
        self, main_window, loading_step, coarse_align_step, particle_positions
    ):
        self.main_window = main_window
        self.loading_step = loading_step
        self.coarse_align_step = coarse_align_step
        self.auto_track_window = None
        self.particle_positions = particle_positions
        self.tracking_positions = None
        self.tracking_start_frames = np.zeros((MAX_PARTICLES,), dtype=np.int32)
        self.tracking_end_frames = np.empty((MAX_PARTICLES,), dtype=np.int32)
        self.properties = None

    def open(self, close_callback):
        self.particle_positions.resize(MAX_PARTICLES, self.image_count())
        self.tracking_start_frames[:] = 0
        self.tracking_end_frames[:] = self.image_count() - 1
        self.tracking_positions = [None for i in range(MAX_PARTICLES)]

        # get some default search parameters based on the image resolution
        # for a 1024x1024 image search_size should 80
        # and marker_radius should be 20
        if self.properties is None:
            resolution = self.load_image(0).shape[0]
            search_size = round(resolution / 1024 * 80)
            marker_radius = round(resolution / 1024 * 20)
            self.properties = {
                "search_size": (search_size, search_size),
                "marker_radius": marker_radius
            }

        self.auto_track_window = AutoTrackWindow(
            self.main_window, MAX_PARTICLES
        )
        # register callbacks
        self.auto_track_window.properties.set_properties(self.properties)
        self.auto_track_window.table.set_mark_end_command(self.mark_end)
        self.auto_track_window.table.set_reset_command(self.reset_particle)
        self.auto_track_window.properties.set_command(self.update_properties)
        self.auto_track_window.track_button.config(command=self.track_selected)
        self.auto_track_window.interpolate_button.config(
            command=self.interpolate_selected
        )
        self.auto_track_window.reset_button.config(command=self.reset_all)

        # reset back to first image, because most particles should be tracked
        # starting from image 1
        self.main_window.image_select.set(1)

        # cleanup
        def close():
            self.save()
            self.auto_track_window.destroy()
            self.auto_track_window = None
            close_callback(reset=True)
        self.auto_track_window.protocol("WM_DELETE_WINDOW", close)

    def save(self):
        marker_csv = os.path.join(
            self.loading_step.get_output_path(),
            "marker_data.csv"
        )
        write_marker_csv(marker_csv, self.particle_positions.array)

    def restore(self):
        marker_csv = os.path.join(
            self.loading_step.get_output_path(),
            "marker_data.csv"
        )
        try:
            marker_data = load_marker_csv(marker_csv)
            if len(marker_data) == 0:
                return False
            if marker_data.shape[1] != self.image_count():
                return False
            self.reset_all()
            self.particle_positions.replace(marker_data)
            return True
        except FileNotFoundError:
            return False

    def load_image(self, i):
        return self.coarse_align_step.load_image(i)

    def image_count(self):
        return self.coarse_align_step.image_count()

    def select_image(self, i):
        image = self.load_image(i)
        self.main_window.image_frame.render_image(image)
        self.render_markers(i)
        self.main_window.image_frame.update()
        if self.auto_track_window is not None:
            self.auto_track_window.table.update_data(
                self.particle_positions,
                self.tracking_positions,
                self.tracking_start_frames,
                self.tracking_end_frames
            )

    def render_markers(self, i):
        if self.properties is None:
            search_size = 0
            marker_radius = 0
            marker_size = 0
        else:
            search_size = self.properties["search_size"]
            marker_radius = self.properties["marker_radius"]
            # TODO: avoid this call to create_particle_mask
            marker_size = create_particle_mask(marker_radius).shape
        for p in range(self.particle_positions.particle_count()):
            particle_position = self.particle_positions.get_position(p, i)
            # check whether a particle is beginnning tracking in this slot
            if self.tracking_start_frames[p] == i:
                tracking_position = self.tracking_positions[p]
            else:
                tracking_position = None
            # render some boxes to indicate search areas
            if tracking_position is not None:
                # search size rect
                self.main_window.image_frame.render_rect(
                    tracking_position, search_size, "#ff9800"
                )
                # marker size rect
                self.main_window.image_frame.render_rect(
                    tracking_position, marker_size, "#8bc34a"
                )
                # label
                self.main_window.image_frame.render_text(
                    tracking_position, p+1
                )
            elif particle_position is not None:
                # still draw the label even if no tracking_position
                self.main_window.image_frame.render_text(
                    particle_position, p+1
                )
            # render a blue bot for particle position
            if particle_position is not None:
                self.main_window.image_frame.render_point(
                    particle_position, "#03a9f4"
                )

    def track_selected(self):
        # create a circular particle mask
        particle_mask = create_particle_mask(
            self.properties["marker_radius"],
            self.auto_track_window.properties.get_invert_particle_color()
        )
        search_size = self.properties["search_size"]
        # hide the window temporarily so user can't interact with it
        self.auto_track_window.withdraw()
        try:
            particles = self.auto_track_window.table.get_tracked_particles()
            if len(particles) == 0:
                raise ValueError("no particles selected!")
            start_frames = np.choose(particles, self.tracking_start_frames)
            end_frames = np.choose(particles, self.tracking_end_frames)
            for i in range(start_frames.min(), end_frames.max()+1):
                image = self.load_image(i)
                for p in particles:
                    # check whether particle is persent on this frame
                    # otherwise skip it
                    if i < self.tracking_start_frames[p]:
                        continue
                    if i > self.tracking_end_frames[p]:
                        continue
                    # using tracking position if first frame
                    # otherwise use previous particle position
                    if i == self.tracking_start_frames[p]:
                        search_position = self.tracking_positions[p]
                    else:
                        search_position = self.particle_positions[p][i-1]
                    if search_position is None:
                        continue
                    # search for the particle and update its position!
                    self.particle_positions[p][i] = particle_search(
                        image, particle_mask, search_position, search_size
                    )
                # show the user progress
                self.main_window.image_select.set(i+1)
                self.main_window.update()
            for p in particles:
                if self.auto_track_window.table.get_selected_particle() != p:
                    self.auto_track_window.table.disable_tracking(p)
            showinfo("Automatic Tracking", "Tracking Completed!")
            # reset back to frame 1
            self.main_window.image_select.set(start_frames.min()+1)
        except Exception as e:
            showerror("Auto Track Error", str(e))
        finally:
            # bring the window back into view
            self.auto_track_window.deiconify()

    def interpolate_selected(self):
        particles = self.auto_track_window.table.get_tracked_particles()
        if len(particles) == 0:
            showerror("Interpolation Error", "No particles selected")
            return
        for p in particles:
            self.particle_positions.attempt_interpolation(p)
        showinfo("Interpolation", "Interpolation Completed!")
        self.select_image(self.main_window.selected_image())

    def update_properties(self):
        self.properties = self.auto_track_window.properties.get_properties()
        self.select_image(self.main_window.selected_image())

    def mark_end(self, particle_index):
        """Marks the final frame a particle appears on."""
        selected_image = self.main_window.selected_image()
        if selected_image < self.tracking_start_frames[particle_index]:
            self.tracking_start_frames[particle_index] = 0
        self.tracking_end_frames[particle_index] = selected_image
        self.particle_positions.trim(particle_index, selected_image)
        self.select_image(selected_image)

    def canvas_click(self, x, y):
        """User indicates where to track the particle by clicking."""
        selected_image = self.main_window.selected_image()
        selected_particle = (
            self.auto_track_window.table.get_selected_particle()
        )
        self.tracking_positions[selected_particle] = (x, y)
        self.tracking_start_frames[selected_particle] = selected_image
        if selected_image >= self.tracking_end_frames[selected_particle]:
            self.tracking_end_frames[selected_particle] = self.image_count()-1
        self.auto_track_window.table.enable_tracking(selected_particle)
        self.select_image(selected_image)

    def reset_all(self):
        """Nuke all particle data."""
        self.particle_positions.reset_all()
        self.tracking_positions = [None for i in range(MAX_PARTICLES)]
        if self.auto_track_window is not None:
            for i in range(MAX_PARTICLES):
                self.auto_track_window.table.disable_tracking(i)
            self.select_image(self.main_window.selected_image())

    def reset_particle(self, particle_index):
        """Nuke specific particle data."""
        self.particle_positions.reset(particle_index)
        self.tracking_positions[particle_index] = None
        self.tracking_start_frames[particle_index] = 0
        self.tracking_end_frames[particle_index] = self.image_count() - 1
        self.select_image(self.main_window.selected_image())
