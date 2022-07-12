from tkinter import ttk
from .widget_templates import DropDownWidget, SliderLayout, ToggleButton
from nrcemt.common.gui import ScaleSpinboxLink

PAD_Y = 5


# widgets configuration for the settings above the sample
class AboveSampleFrame(ttk.LabelFrame):

    def __init__(self, master):
        super().__init__(master, text="Settings above sample", borderwidth=5)

        mode_widget = DropDownWidget(self)
        mode_widget.pack(side="top", anchor="nw")

        # label for sliders
        sliders_label = ttk.Label(self, text="Lens settings (mm):")
        sliders_label.pack(side="top", pady=PAD_Y)

        # stores the status of the lenses on/off
        self.lens_status = [True, True, True]

        # frame that hold c1 slider, spinbox, and button
        c1_frame = ttk.Frame(self)
        c1_frame.pack(side="top", anchor="nw")

        self.c1_slider = SliderLayout(c1_frame, "Lens C1: ")
        self.c1_link = ScaleSpinboxLink(
            self.c1_slider.slider,
            self.c1_slider.entry,
            13, (0, 50)
        )
        self.c1_slider.pack(anchor="w", side="left", pady=PAD_Y)

        self.c1_toggle = ToggleButton(c1_frame, "C1")
        self.c1_toggle.pack(side="left", pady=PAD_Y)

        # frame that hold c2 slider, spinbox, and button
        c2_frame = ttk.Frame(self)
        c2_frame.pack(side="top", anchor="nw")

        c2_slider = SliderLayout(c2_frame, "Lens C2: ")
        self.c2_link = ScaleSpinboxLink(
            c2_slider.slider,
            c2_slider.entry,
            35, (0, 50)
        )
        c2_slider.pack(anchor="w", side="left", pady=PAD_Y)

        self.c2_toggle = ToggleButton(c2_frame, "C2")
        self.c2_toggle.pack(side="left", pady=PAD_Y)

        # frame that hold c3 slider, spinbox, and button
        c3_frame = ttk.Frame(self)
        c3_frame.pack(side="top", anchor="nw")

        c3_slider = SliderLayout(c3_frame, "Lens C3: ")
        self.c3_link = ScaleSpinboxLink(
            c3_slider.slider,
            c3_slider.entry,
            10.68545, (0, 50)
        )
        c3_slider.pack(anchor="w", side="left", pady=PAD_Y)

        self.c3_toggle = ToggleButton(c3_frame, "C3")
        self.c3_toggle.pack(side="left", pady=PAD_Y)
