from tkinter import ttk
from .widget_templates import DropDownWidget, SliderLayout, ToggleButton
from nrcemt.common.gui import ScaleSpinboxLink

PAD_Y = 5


# widgets configuration for the settings above the sample
class AboveSampleFrame(ttk.LabelFrame):

    def __init__(self, master):
        super().__init__(master, text="Settings above sample", borderwidth=5)
        self.columnconfigure(1, weight=1)

        mode_widget = DropDownWidget(self)
        mode_widget.grid(row=0, column=0, sticky="we")

        # label for sliders
        sliders_label = ttk.Label(self, text="Lens settings (mm):")
        sliders_label.grid(row=1, column=0, sticky="we")

        # stores the values of the lenses
        self.focal_values = [67.29, 22.94, 39.88]

        # stores the status of the lenses on/off
        self.lens_status = [True, True, True]

        self.c1_slider = SliderLayout(self, "Lens C1: ")
        self.c1_link = ScaleSpinboxLink(
            self.c1_slider.slider,
            self.c1_slider.entry,
            self.focal_values[0], (6, 300)
        )
        self.c1_slider.grid(row=2, column=0, columnspan=2, sticky="nwse")

        self.c1_toggle = ToggleButton(self)
        self.c1_toggle.grid(row=2, column=2)

        c2_slider = SliderLayout(self, "Lens C2: ")
        self.c2_link = ScaleSpinboxLink(
            c2_slider.slider,
            c2_slider.entry,
            self.focal_values[1], (6, 300)
        )
        c2_slider.grid(row=3, column=0, columnspan=2, sticky="nwse")

        self.c2_toggle = ToggleButton(self)
        self.c2_toggle.grid(row=3, column=2)

        c3_slider = SliderLayout(self, "Lens C3: ")
        self.c3_link = ScaleSpinboxLink(
            c3_slider.slider,
            c3_slider.entry,
            self.focal_values[2], (6, 300)
        )
        c3_slider.grid(row=4, column=0, columnspan=2, sticky="nwse")
        self.c3_toggle = ToggleButton(self)
        self.c3_toggle.grid(row=4, column=2)
