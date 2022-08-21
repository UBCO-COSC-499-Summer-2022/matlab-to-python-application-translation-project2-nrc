"""Automic particle tracking step module."""

import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo
import numpy as np
from .common import NumericSpinbox
from alignment_software.engine.csv_io import (
    load_marker_csv, write_marker_csv
)
from alignment_software.engine.particle_tracking import (
    create_particle_mask,
    particle_search
)


MAX_PARTICLES = 13
INPUT_WIDTH = 10


class AutoTrackStep:
    """Step that handles automatic particle tracking."""

    def __init__(
        self, main_window, loading_step, coarse_align_step, particle_positions
    ):
        """
        Create optimization step.
        Depends on loading step to get the output path.
        Depends on coarse alignment step to get coarse aligned images.
        Depends on particle positions for shared particle data.
        """
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
        """Opens the step and calls close_callback when done."""

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
        """Save marker data to csv."""
        marker_csv = os.path.join(
            self.loading_step.get_output_path(),
            "marker_data.csv"
        )
        write_marker_csv(marker_csv, self.particle_positions.array)

    def restore(self):
        """Restore marker data from csv."""
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
        """Load image from corase alignment step."""
        return self.coarse_align_step.load_image(i)

    def image_count(self):
        """Returns the number of frames in the sequence."""
        return self.coarse_align_step.image_count()

    def select_image(self, i):
        """Render an image and markers with given index."""
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
        """Render dots and rectangular markers for given frame."""
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
        """Follow all selected particles."""
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
        """Try to interpolate missing positions for selected particles."""
        particles = self.auto_track_window.table.get_tracked_particles()
        if len(particles) == 0:
            showerror("Interpolation Error", "No particles selected")
            return
        for p in particles:
            self.particle_positions.attempt_interpolation(p)
        showinfo("Interpolation", "Interpolation Completed!")
        self.select_image(self.main_window.selected_image())

    def update_properties(self):
        """Update the search and marker radius."""
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
        if self.auto_track_window is None:
            return
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

    def focus(self):
        """Brings the automatic tracking window to the top."""
        self.auto_track_window.lift()


class AutoTrackWindow(tk.Toplevel):
    """Create the automatic tracking window witth a table and controls."""

    def __init__(self, master, particle_count):
        """Create the window."""
        super().__init__(master)
        self.title("Automatic Detection Window")

        # Adding widgets to the window
        self.table = ParticleTableFrame(self, particle_count)
        self.table.grid(column=0, row=0, sticky="we")

        self.track_button = ttk.Button(self, text="Track all selected")
        self.track_button.grid(column=0, row=1, sticky="we")
        self.interpolate_button = ttk.Button(self, text="Interpolate selected")
        self.interpolate_button.grid(column=0, row=2, sticky="we")

        self.properties = ParticlePropertiesFrame(self)
        self.properties.grid(column=0, row=3, sticky="we")

        self.reset_button = ttk.Button(self, text="Reset all particles")
        self.reset_button.grid(column=0, row=4, sticky="we")


class ParticlePropertiesFrame(tk.Frame):
    """
    Frame for tracking properties such as marker radius, search radious and
    particle color.
    """

    def __init__(self, master):
        """Create the frame."""
        super().__init__(master)

        self.command = None

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        particle_color = tk.LabelFrame(self, text="Particle Color")
        particle_color.grid(row=0, column=0, sticky="nwse")
        self.particle_color_var = tk.IntVar(self, 0)
        black_particle_color = tk.Radiobutton(
            particle_color, text="Black",
            variable=self.particle_color_var, value=0
        )
        black_particle_color.grid(row=0, column=0)
        white_particle_color = tk.Radiobutton(
            particle_color, text="White",
            variable=self.particle_color_var, value=1
        )
        white_particle_color.grid(row=0, column=1)

        search_areas_frame = tk.LabelFrame(self, text="Shift Search Areas")
        search_areas_frame.grid(row=0, column=1, sticky="nwse")

        marker_radius_label = ttk.Label(
            search_areas_frame, text="Marker radius (pixel)"
        )
        marker_radius_label.grid(row=0, column=0)
        self.marker_radius_input = NumericSpinbox(
            search_areas_frame, width=INPUT_WIDTH,
            value_default=80, value_range=[1, 999],
            command=self.update
        )
        self.marker_radius_input.grid(row=0, column=1)

        search_area_width_label = ttk.Label(
            search_areas_frame, text="Search width (pixel)"
        )
        search_area_width_label.grid(row=1, column=0)
        self.search_area_width_input = NumericSpinbox(
            search_areas_frame, width=INPUT_WIDTH,
            value_default=80, value_range=[1, 999],
            command=self.update
        )
        self.search_area_width_input.grid(row=1, column=1)

        search_area_height_label = ttk.Label(
            search_areas_frame, text="Search height (pixel)"
        )
        search_area_height_label.grid(row=2, column=0)
        self.search_area_height_input = NumericSpinbox(
            search_areas_frame, width=INPUT_WIDTH,
            value_default=80, value_range=[1, 999],
            command=self.update
        )
        self.search_area_height_input.grid(row=2, column=1)

    def set_command(self, command):
        """Set the command to be called when properties update."""
        self.command = command

    def update(self):
        """Call the command when properties are updated."""
        if self.command is not None:
            self.command()

    def set_properties(self, properties):
        """Set the properties from dictionary."""
        self.search_area_width_input.set(properties["search_size"][0])
        self.search_area_height_input.set(properties["search_size"][1])
        self.marker_radius_input.set(properties["marker_radius"])

    def get_properties(self):
        """Get properties as dictionary."""
        return {
            "search_size": (
                self.search_area_width_input.get(),
                self.search_area_height_input.get()
            ),
            "marker_radius": self.marker_radius_input.get()
        }

    def get_invert_particle_color(self):
        """
        Get whether the particle color is inverted.
        Default is dark, inverted is bright.
        """
        return self.particle_color_var.get() == 1



class ParticleTableFrame(tk.Frame):
    """Create a table which shows tracking locations, and frame ranges."""

    def __init__(self, master, particle_count):
        """Create the table frame with a given number of particles."""
        super().__init__(master)

        table_header = ["X", "Y", "IM1", "IM2"]
        for i, header in enumerate(table_header):
            header = tk.Label(self, text=header)
            header.grid(row=0, column=i+2)

        self.mark_end_command = None
        self.reset_command = None
        self.particle_select_var = tk.IntVar(self, 0)
        self.data_vars = [[None] * 5 for i in range(particle_count)]
        self.track_vars = []

        for i in range(particle_count):

            particle_select = tk.Radiobutton(
                self, text=f"{i+1}", value=i,
                variable=self.particle_select_var
            )
            particle_select.grid(row=i+1, column=0)

            data_var = tk.StringVar(self, "o")
            label = tk.Label(self, textvariable=data_var)
            label.grid(row=i+1, column=1, sticky="nswe")
            self.data_vars[i][0] = data_var

            for c in range(4):
                data_var = tk.StringVar(self, "-")
                label = tk.Label(
                    self, textvariable=data_var,
                    width=8, bd=1, relief="solid"
                )
                label.grid(row=i+1, column=c+2, sticky="nswe")
                self.data_vars[i][c+1] = data_var

            end_button = tk.Button(
                self, text="Mark End",
                command=lambda particle_index=i: self.mark_end(particle_index)
            )
            end_button.grid(row=i+1, column=6)

            reset_button = tk.Button(
                self, text="Reset",
                command=lambda particle_index=i: self.reset(particle_index)
            )
            reset_button.grid(row=i+1, column=7)

            track_var = tk.BooleanVar(self, False)
            self.track_vars.append(track_var)
            track_checkbox = tk.Checkbutton(
                self, text="Select", variable=track_var
            )
            track_checkbox.grid(row=i+1, column=8)

    def update_data(
        self, particle_positions,
        tracking_positions, tracking_start_frames, tracking_end_frames
    ):
        """Update the contents of the table."""
        for i, position in enumerate(tracking_positions):
            status = particle_positions.get_status(i)
            if status == "complete":
                icon = "●"
            elif status == "partial":
                icon = "◒"
            else:
                icon = "○"
            self.data_vars[i][0].set(icon)
            if position is not None:
                self.data_vars[i][1].set(position[0])
                self.data_vars[i][2].set(position[1])
            else:
                self.data_vars[i][1].set("-")
                self.data_vars[i][2].set("-")
            self.data_vars[i][3].set(tracking_start_frames[i]+1)
            self.data_vars[i][4].set(tracking_end_frames[i]+1)

    def get_selected_particle(self):
        """Get the index of the particle selected by the radio button"""
        return self.particle_select_var.get()

    def get_tracked_particles(self):
        """Get particles selected for tracking."""
        tracked = []
        for i, variable in enumerate(self.track_vars):
            if variable.get():
                tracked.append(i)
        return tracked

    def enable_tracking(self, particle_index):
        """Selects a particle for tracking."""
        self.track_vars[particle_index].set(True)

    def disable_tracking(self, particle_index):
        """Deselects a particle for tracking."""
        self.track_vars[particle_index].set(False)

    def set_mark_end_command(self, command):
        """Sets a command that gets called when mark end is clicked."""
        self.mark_end_command = command

    def mark_end(self, particle_index):
        """Called when a mark button is clicked with a given index."""
        if self.mark_end_command is not None:
            self.mark_end_command(particle_index)

    def set_reset_command(self, command):
        """Sets a command that gets called when reset is clicked."""
        self.reset_command = command

    def reset(self, particle_index):
        """Called when a reset button is clicked with a given index."""
        self.disable_tracking(particle_index)
        if self.reset_command is not None:
            self.reset_command(particle_index)
