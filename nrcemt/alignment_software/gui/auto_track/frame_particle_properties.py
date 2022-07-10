import tkinter as tk
from tkinter import ttk

from nrcemt.common.gui.numericspinbox import NumericSpinbox

INPUT_WIDTH = 10


class ParticlePropertiesFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.command = None

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=4)

        self.particle_color = tk.LabelFrame(self, text="Particle Color")
        self.particle_color.grid(row=0, column=0, sticky="nwse")
        self.particle_color_frame(self.particle_color)

        self.shift_search_areas = tk.LabelFrame(
            self, text="Shift Search Areas"
        )
        self.shift_search_areas.grid(row=0, column=1, sticky="nwse")
        self.shift_search_areas_frame(self.shift_search_areas)

    def particle_color_frame(self, frame):
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=3)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        self.black_particle_color = tk.Radiobutton(
            frame, text="Black"
        )
        self.black_particle_color.grid(row=0, column=0)
        self.white_particle_color = tk.Radiobutton(
            frame, text="White"
        )
        self.white_particle_color.grid(row=0, column=1)

    def shift_search_areas_frame(self, frame):
        marker_radius_label = ttk.Label(
            frame, text="Marker radius (pixel)"
        )
        marker_radius_label.grid(row=0, column=0)
        self.marker_radius_var = tk.IntVar(self, 20)
        self.marker_radius_var.trace('w', lambda a, b, c: self.update())
        marker_radius_input = NumericSpinbox(
            frame, width=INPUT_WIDTH,
            value_default=20, value_range=[1, 999],
            textvariable=self.marker_radius_var
        )
        marker_radius_input.grid(row=0, column=1)

        search_area_width_label = ttk.Label(
            frame, text="Search width (pixel)"
        )
        search_area_width_label.grid(row=1, column=0)
        self.search_width_var = tk.IntVar(self, 80)
        self.search_width_var.trace('w', lambda a, b, c: self.update())
        search_area_width_input = NumericSpinbox(
            frame, width=INPUT_WIDTH,
            value_default=80, value_range=[1, 999],
            textvariable=self.search_width_var
        )
        search_area_width_input.grid(row=1, column=1)

        search_area_height_label = ttk.Label(
            frame, text="Search height (pixel)"
        )
        search_area_height_label.grid(row=2, column=0)
        self.search_height_var = tk.IntVar(self, 80)
        self.search_height_var.trace('w', lambda a, b, c: self.update())
        search_area_height_input = NumericSpinbox(
            frame, width=INPUT_WIDTH,
            value_default=80, value_range=[1, 999],
            textvariable=self.search_height_var
        )
        search_area_height_input.grid(row=2, column=1)

    def set_command(self, command):
        self.command = command

    def update(self):
        if self.command is not None:
            self.command()

    def set_properties(self, properties):
        self.search_width_var.set(properties["search_size"][0])
        self.search_height_var.set(properties["search_size"][1])
        self.marker_radius_var.set(properties["marker_radius"])

    def get_properties(self):
        return {
            "search_size": (
                self.search_width_var.get(),
                self.search_height_var.get()
            ),
            "marker_radius": self.marker_radius_var.get()
        }
