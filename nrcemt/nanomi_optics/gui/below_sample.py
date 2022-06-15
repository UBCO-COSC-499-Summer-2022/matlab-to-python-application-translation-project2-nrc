from tkinter import ttk
from .widget_templates import SliderLayout, RadioLayout


# widgets configuration for the settings below the sample
class BelowSampleConfiguration(ttk.LabelFrame):

    def __init__(self, master):
        super().__init__(master, text="Settings below sample", borderwidth=5)

        # radio buttons for image mode
        image_options = ["Diffraction", "Image"]
        image_mode_buttons = RadioLayout(self, "Image Mode", image_options)
        image_mode_buttons.pack(side="top", anchor="nw")

        # radio buttons for auto setting
        auto_options = ["Objective", "Intermediate", "Projective", "None"]
        auto_mode_buttons = RadioLayout(self, "Auto Setting", auto_options)
        auto_mode_buttons.pack(side="top", anchor="nw", pady=5)

        # label for sliders
        sliders_label = ttk.Label(self, text="Lens settings (nm):")
        sliders_label.pack(side="top", pady=5)

        # call 4 slider layouts for lens settings
        distance_slider = SliderLayout(self, "Distance:")
        distance_slider.pack(side="top", anchor="ne", pady=5)

        objective_slider = SliderLayout(self, "Objective:")
        objective_slider.pack(side="top", anchor="ne", pady=5)

        intermediate_slider = SliderLayout(self, "Intermediate:")
        intermediate_slider.pack(side="top", anchor="ne", pady=5)

        projective_slider = SliderLayout(self, "Projective:")
        projective_slider.pack(side="top", anchor="ne", pady=5)

