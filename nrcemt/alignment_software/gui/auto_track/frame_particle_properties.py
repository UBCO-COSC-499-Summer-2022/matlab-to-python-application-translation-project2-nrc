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
        self.marker_radius_var = tk.IntVar(20)
        self.marker_radius_var.trace('w', lambda a, b, c: self.update())
        marker_radius_input = NumericSpinbox(
            frame, width=INPUT_WIDTH,
            value_default=20, value_range=[1, 999],
            textvariable=self.marker_radius_var
        )
        marker_radius_input.grid(row=0, column=1)

        search_area_width_label = ttk.Label(
            frame, text="Marker radius (pixel)"
        )
        search_area_width_label.grid(row=1, column=0)
        self.search_width_var = tk.IntVar(80)
        self.search_width_var.trace('w', lambda a, b, c: self.update())
        search_area_width_input = NumericSpinbox(
            frame, width=INPUT_WIDTH,
            value_default=80, value_range=[1, 999],
            textvariable=self.search_width_var
        )
        search_area_width_input.grid(row=1, column=1)

        search_area_height_label = ttk.Label(
            frame, text="Marker radius (pixel)"
        )
        search_area_height_label.grid(row=2, column=0)
        self.search_height_var = tk.IntVar(80)
        self.search_height_var.trace('w', lambda a, b, c: self.update())
        search_area_height_input = NumericSpinbox(
            frame, width=INPUT_WIDTH,
            value_default=80, value_range=[1, 999],
            textvariable=self.search_height_var
        )
        search_area_height_input.grid(row=2, column=1)

        control_frame = tk.Frame(frame)
        control_frame.grid(row=3, column=0, rowspan=3)
        for i in range(3):
            control_frame.rowconfigure(i, weight=1)
            control_frame.columnconfigure(i, weight=1)

        self.up_button = tk.Button(control_frame, text="Up")
        self.up_button.grid(row=0, column=1)
        self.left_button = tk.Button(control_frame, text="Left")
        self.left_button.grid(row=1, column=0)
        self.right_button = tk.Button(control_frame, text="Right")
        self.right_button.grid(row=1, column=2)
        self.down_button = tk.Button(control_frame, text="Down")
        self.down_button.grid(row=2, column=1)
        self.current_position = tk.Label(control_frame)
        self.current_position.grid(row=1, column=1)

        rs_frame = tk.Frame(frame)
        rs_frame.grid(row=3, column=1, rowspan=3)
        rs_frame.rowconfigure(0, weight=1)
        rs_frame.rowconfigure(1, weight=1)
        rs_frame.columnconfigure(0, weight=1)
        self.rs_button = tk.Button(rs_frame, text="RS")
        self.rs_button.grid(row=0, column=0)
        self.all_rs_button = tk.Button(rs_frame, text="All RS")
        self.all_rs_button.grid(row=1, column=0)

    def set_command(self, command):
        self.command = command

    def update(self):
        if self.command is not None:
            self.command()
