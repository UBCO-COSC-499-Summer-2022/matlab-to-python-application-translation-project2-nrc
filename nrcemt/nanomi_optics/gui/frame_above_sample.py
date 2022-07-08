from tkinter import ttk
from .widget_templates import DropDownWidget, SliderLayout
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

        # #call 3 slider layouts, link slider with spinbox, label their names,
        # set their inital focal lengths

        # slider for c1 lens
        c1_slider = SliderLayout(self, "Lens C1: ")
        self.c1_link = ScaleSpinboxLink(
            c1_slider.slider,
            c1_slider.entry,
            13, (0, 50)
        )
        self.c1_link.set_command(self.update_cf)
        c1_slider.pack(anchor="ne", side="top", pady=PAD_Y)

        # slider for C2 lens
        c2_slider = SliderLayout(self, "Lens C2: ")
        self.c2_link = ScaleSpinboxLink(
            c2_slider.slider,
            c2_slider.entry,
            35, (0, 50)
        )
        self.c2_link.set_command(self.update_cf)
        c2_slider.pack(side="top", anchor="ne", pady=PAD_Y)

        # Slider for C3 lens
        c3_slider = SliderLayout(self, "Lens C3: ")
        self.c3_link = ScaleSpinboxLink(
            c3_slider.slider,
            c3_slider.entry,
            10.68545, (0, 50)
        )
        self.c3_link.set_command(self.update_cf)
        c3_slider.pack(side="top", anchor="ne", pady=PAD_Y)

    def update_cf(self, value):
        self.update_slider_values(
            self.c1_link.get(),
            self.c2_link.get(),
            self.c3_link.get(),
        )

    def update_slider_values(self, c1, c2, c3):
        self.slider_values = [float(c1), float(c2), float(c3)]
