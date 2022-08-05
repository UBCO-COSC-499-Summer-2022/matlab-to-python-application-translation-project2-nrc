import tkinter as tk
from tkinter import ttk
from .widget_templates import DropDownWidget, SliderLayout, ToggleButton
from nrcemt.common.gui import ScaleSpinboxLink
from nrcemt.nanomi_optics.engine.lens_excitation import (
    ur_symmetric, ur_asymmetric, cf_symmetric, cf_asymmetric
)
PAD_Y = 5


# widgets configuration for the settings above the sample
class AboveSampleFrame(tk.LabelFrame):

    def __init__(self, master):
        super().__init__(master, text="Settings above sample")
        self.columnconfigure(1, weight=1)

        self.mode_widget = DropDownWidget(self)
        self.mode_widget.grid(row=0, column=0, sticky="we")

        # label for sliders
        sliders_label = ttk.Label(self, text="Lens settings (mm):")
        sliders_label.grid(row=1, column=0, sticky="we")

        # stores the values of the lenses
        self.focal_values = [67.29, 22.94, 39.88]

        self.lens_type = [True, False, False]

        # stores the status of the lenses on/off
        self.lens_status = [True, True, True]

        self.sliders = []
        self.links = []
        self.toggles = []
        self.slider_text = [
            "Lens C1: ", "Lens C2: ", "Lens C3: "
        ]

        for i, txt in enumerate(self.slider_text):
            self.sliders.append(SliderLayout(self, "Lens C1: "))
            self.links.append(
                ScaleSpinboxLink(
                    self.sliders[i].slider,
                    self.sliders[i].entry,
                    self.focal_values[i], (6, 300)
                )
            )
            self.sliders[i].grid(
                row=2 + i, column=0, columnspan=2, sticky="nwse"
            )

            self.toggles.append(ToggleButton(self))
            self.toggles[i].grid(row=2 + i, column=2)

    def set_mode(self, mode):
        if mode:
            print("Cf")
        else:
            print("Ur")
