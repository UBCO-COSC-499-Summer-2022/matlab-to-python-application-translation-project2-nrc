import tkinter as tk
from tkinter import ttk
from .widget_templates import SliderLayout, RadioLayout, ToggleButton
from nrcemt.common.gui import ScaleSpinboxLink

PAD_Y = 5


# widgetsfor the settings below the sample
class BelowSampleFrame(ttk.LabelFrame):

    def __init__(self, master):
        super().__init__(master, text="Settings below sample", borderwidth=5)
        self.columnconfigure(1, weight=1)

        # stores the values of the sliders
        self.slider_values = [10, 19.670, 6.498, 6]

        # stores the status of the lenses on/off
        self.lens_status = [True, True, True]

        # radio buttons for image mode
        self.opt_sel = tk.StringVar()
        opt_options = ["Diffraction", "Image"]
        self.opt_sel.set(opt_options[1])
        self.opt_mode_buttons = RadioLayout(
            self, "Image Mode", opt_options, self.opt_sel
        )
        self.opt_mode_buttons.grid(row=0, column=0)

        # radio buttons for auto setting
        self.lens_sel = tk.IntVar()
        auto_options = [
            "Objective", "Intermediate", "Projective", "None"
        ]
        self.lens_sel.set(-1)
        auto_mode_buttons = RadioLayout(
            self, "Auto Setting", auto_options, self.lens_sel
        )
        auto_mode_buttons.grid(row=0, column=1, columnspan=2, sticky="w")
        # label for sliders
        sliders_label = ttk.Label(self, text="Lens settings (nm):")
        sliders_label.grid(row=1, column=0, sticky="we")

        self.distance_slider = SliderLayout(self, "Distance:")
        self.distance_link = ScaleSpinboxLink(
            self.distance_slider.slider,
            self.distance_slider.entry,
            self.slider_values[0], (0.1, 100)
        )
        self.distance_slider.grid(row=2, column=0, columnspan=2, sticky="nwse")

        self.objective_slider = SliderLayout(self, "Objective:")
        self.objective_link = ScaleSpinboxLink(
            self.objective_slider.slider,
            self.objective_slider.entry,
            self.slider_values[1], (6, 300)
        )
        self.objective_slider.grid(
            row=3, column=0, columnspan=2, sticky="nwse"
        )

        self.objective_toggle = ToggleButton(self)
        self.objective_toggle.grid(row=3, column=2)

        self.intermediate_slider = SliderLayout(self, "Intermediate:")
        self.intermediate_link = ScaleSpinboxLink(
            self.intermediate_slider.slider,
            self.intermediate_slider.entry,
            self.slider_values[2], (6, 300)
        )
        self.intermediate_slider.grid(
            row=4, column=0, columnspan=2, sticky="nwse"
        )

        self.intermediate_toggle = ToggleButton(self)
        self.intermediate_toggle.grid(row=4, column=2)

        self.projective_slider = SliderLayout(self, "Projective:")
        self.projective_link = ScaleSpinboxLink(
            self.projective_slider.slider,
            self.projective_slider.entry,
            self.slider_values[3], (6, 300)
        )
        self.projective_slider.grid(
            row=5, column=0, columnspan=2, sticky="nwse"
        )
        self.projective_toggle = ToggleButton(self)
        self.projective_toggle.grid(row=5, column=2)
