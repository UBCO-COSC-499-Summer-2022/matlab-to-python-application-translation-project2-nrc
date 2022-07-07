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

        self.slider_values = []

        # #call 3 slider layouts, link slider with spinbox, label their names,
        # set their inital focal lengths

        # slider for c1 lens
        self.c1_slider = SliderLayout(self, "Lens C1: ")
        ScaleSpinboxLink(
            self.c1_slider.slider,
            self.c1_slider.entry,
            0, (0, 50)
        )
        self.c1_slider.slider.configure(
            command=lambda value, name="c1": self.update_cf(name, value)
        )
        self.c1_slider.slider.set(13)
        self.c1_slider.pack(anchor="ne", side="top", pady=PAD_Y)

        # slider for C2 lens
        self.c2_slider = SliderLayout(self, "Lens C2: ")
        ScaleSpinboxLink(
            self.c2_slider.slider,
            self.c2_slider.entry,
            0, (0, 50)
        )
        self.c2_slider.slider.configure(
            command=lambda value, name="c2": self.update_cf(name, value)
        )
        self.c2_slider.slider.set(35)
        self.c2_slider.pack(side="top", anchor="ne", pady=PAD_Y)

        # Slider for C3 lens
        self.c3_slider = SliderLayout(self, "Lens C3: ")
        ScaleSpinboxLink(
            self.c3_slider.slider,
            self.c3_slider.entry,
            0, (0, 50)
        )
        self.c3_slider.slider.set(10.68545)
        self.c3_slider.slider.configure(
            command=lambda value, name="c3": self.update_cf(name, value)
        )
        self.c3_slider.pack(side="top", anchor="ne", pady=PAD_Y)

    def update_cf(self, name, value):
        if name.__eq__("c1"):
            self.update_slider_values(
                value,
                self.c2_slider.slider.get(),
                self.c3_slider.slider.get(),
            )
        elif name == "c2":
            self.update_slider_values(
                self.c1_slider.slider.get(),
                value,
                self.c3_slider.slider.get(),)
        elif name == "c3":
            self.update_slider_values(
                self.c1_slider.slider.get(),
                self.c2_slider.slider.get(),
                value)

    def update_slider_values(self, c1, c2, c3):
        self.slider_values = [float(c1), float(c2), float(c3)]
        print(self.slider_values)
