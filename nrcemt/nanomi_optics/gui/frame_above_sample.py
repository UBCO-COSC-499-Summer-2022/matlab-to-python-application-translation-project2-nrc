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

        # stores the values of the sliders
        self.slider_values = []

        # frame that hold c1 slider, spinbox, and button
        c1_frame = ttk.Frame(self)
        c1_frame.pack(side="top", anchor="nw")

        # slider for c1 lens
        c1_slider = SliderLayout(c1_frame, "Lens C1: ")
        self.c1_link = ScaleSpinboxLink(
            c1_slider.slider,
            c1_slider.entry,
            13, (0, 50)
        )
        self.c1_link.set_command(self.update_cf)
        c1_slider.pack(anchor="w", side="left", pady=PAD_Y)

        # toggle button for c1 lens
        c1_toggle = ToggleButton(c1_frame, "c1")
        c1_toggle.pack(side="left", pady=PAD_Y)

        # frame that hold c2 slider, spinbox, and button
        c2_frame = ttk.Frame(self)
        c2_frame.pack(side="top", anchor="nw")

        # slider for C2 lens
        c2_slider = SliderLayout(c2_frame, "Lens C2: ")
        self.c2_link = ScaleSpinboxLink(
            c2_slider.slider,
            c2_slider.entry,
            35, (0, 50)
        )
        self.c2_link.set_command(self.update_cf)
        c2_slider.pack(anchor="w", side="left", pady=PAD_Y)

        # toggle button for c2 lens
        c2_toggle = ToggleButton(c2_frame, "c2")
        c2_toggle.pack(side="left", pady=PAD_Y)

        # frame that hold c3 slider, spinbox, and button
        c3_frame = ttk.Frame(self)
        c3_frame.pack(side="top", anchor="nw")

        # Slider for C3 lens
        c3_slider = SliderLayout(c3_frame, "Lens C3: ")
        self.c3_link = ScaleSpinboxLink(
            c3_slider.slider,
            c3_slider.entry,
            10.68545, (0, 50)
        )
        self.c3_link.set_command(self.update_cf)
        c3_slider.pack(anchor="w", side="left", pady=PAD_Y)

        # toggle button for c3 lens
        c3_toggle = ToggleButton(c3_frame, "c3")
        c3_toggle.pack(side="left", pady=PAD_Y)

    def update_cf(self, value):
        self.update_slider_values(
            self.c1_link.get(),
            self.c2_link.get(),
            self.c3_link.get(),
        )

    def update_slider_values(self, c1, c2, c3):
        self.slider_values = [float(c1), float(c2), float(c3)]
