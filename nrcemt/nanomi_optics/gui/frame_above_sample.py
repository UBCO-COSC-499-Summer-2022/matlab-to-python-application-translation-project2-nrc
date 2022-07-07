from tkinter import ttk
from .widget_templates import DropDownWidget, SliderLayout

PAD_Y = 5


# widgets configuration for the settings above the sample
class AboveSampleFrame(ttk.LabelFrame):

    def __init__(self, master):
        super().__init__(master, text="Settings above sample", borderwidth=5)

        mode_widget = DropDownWidget(self)
        mode_widget.pack(side="top", anchor="nw")

        # label for sliders
        sliders_label = ttk.Label(self, text="Lens settings (nm):")
        sliders_label.pack(side="top", pady=PAD_Y)

        # #call 3 slider layouts and label their names
        c1_slider = SliderLayout(self, "Lens C1: ")
        c1_slider.pack(side="top", anchor="ne", pady=PAD_Y)

        c2_slider = SliderLayout(self, "Lens C2: ")
        c2_slider.pack(side="top", anchor="ne", pady=PAD_Y)

        c3_slider = SliderLayout(self, "Lens C3: ")
        c3_slider.pack(side="top", anchor="ne", pady=PAD_Y)
