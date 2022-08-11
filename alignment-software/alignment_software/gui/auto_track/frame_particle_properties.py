import tkinter as tk
from tkinter import ttk

from ..numericspinbox import NumericSpinbox

INPUT_WIDTH = 10


class ParticlePropertiesFrame(tk.Frame):

    def __init__(self, master):
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

        shift_search_areas = tk.LabelFrame(self, text="Shift Search Areas")
        shift_search_areas.grid(row=0, column=1, sticky="nwse")
        self.shift_search_areas_frame(shift_search_areas)

    def shift_search_areas_frame(self, frame):
        marker_radius_label = ttk.Label(
            frame, text="Marker radius (pixel)"
        )
        marker_radius_label.grid(row=0, column=0)
        self.marker_radius_input = NumericSpinbox(
            frame, width=INPUT_WIDTH,
            value_default=80, value_range=[1, 999],
            command=self.update
        )
        self.marker_radius_input.grid(row=0, column=1)

        search_area_width_label = ttk.Label(
            frame, text="Search width (pixel)"
        )
        search_area_width_label.grid(row=1, column=0)
        self.search_area_width_input = NumericSpinbox(
            frame, width=INPUT_WIDTH,
            value_default=80, value_range=[1, 999],
            command=self.update
        )
        self.search_area_width_input.grid(row=1, column=1)

        search_area_height_label = ttk.Label(
            frame, text="Search height (pixel)"
        )
        search_area_height_label.grid(row=2, column=0)
        self.search_area_height_input = NumericSpinbox(
            frame, width=INPUT_WIDTH,
            value_default=80, value_range=[1, 999],
            command=self.update
        )
        self.search_area_height_input.grid(row=2, column=1)

    def set_command(self, command):
        self.command = command

    def update(self):
        if self.command is not None:
            self.command()

    def set_properties(self, properties):
        self.search_area_width_input.set(properties["search_size"][0])
        self.search_area_height_input.set(properties["search_size"][1])
        self.marker_radius_input.set(properties["marker_radius"])

    def get_properties(self):
        return {
            "search_size": (
                self.search_area_width_input.get(),
                self.search_area_height_input.get()
            ),
            "marker_radius": self.marker_radius_input.get()
        }

    def get_invert_particle_color(self):
        return self.particle_color_var.get() == 1
