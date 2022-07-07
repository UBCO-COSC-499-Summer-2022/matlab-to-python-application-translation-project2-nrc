from tkinter import ttk
from .widget_templates import SliderLayout, RadioLayout

PAD_Y = 5


# widgetsfor the settings below the sample
class BelowSampleFrame(ttk.LabelFrame):

    def __init__(self, master):
        super().__init__(master, text="Settings below sample", borderwidth=5)

        # radio buttons for image mode
        image_options = ["Diffraction", "Image"]
        image_mode_buttons = RadioLayout(self, "Image Mode", image_options)
        image_mode_buttons.pack(side="top", anchor="nw")

        # radio buttons for auto setting
        auto_options = ["Objective", "Intermediate", "Projective", "None"]
        auto_mode_buttons = RadioLayout(self, "Auto Setting", auto_options)
        auto_mode_buttons.pack(side="top", anchor="nw", pady=PAD_Y)

        # label for sliders
        sliders_label = ttk.Label(self, text="Lens settings (nm):")
        sliders_label.pack(side="top", pady=PAD_Y)

        # call 4 slider layouts for lens settings
        distance_slider = SliderLayout(self, "Distance:")
        distance_slider.pack(side="top", anchor="ne", pady=PAD_Y)

        objective_slider = SliderLayout(self, "Objective:")
        objective_slider.pack(side="top", anchor="ne", pady=PAD_Y)

        intermediate_slider = SliderLayout(self, "Intermediate:")
        intermediate_slider.pack(side="top", anchor="ne", pady=PAD_Y)

        projective_slider = SliderLayout(self, "Projective:")
        projective_slider.pack(side="top", anchor="ne", pady=PAD_Y)
