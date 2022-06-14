import tkinter as tk
from tkinter import ttk
from.above_sample import SliderLayout


# widgets configuration for the settings below the sample
class BelowSampleConfiguration(ttk.LabelFrame):

    def __init__(self, master):
        super().__init__(master, text="Settings below sample", borderwidth=10)

        # radio buttons for image mode
        image_options = ["Diffraction", "Image"]
        image_mode_buttons = RadioLayout(self, "Image Mode", image_options)
        image_mode_buttons.pack(side="top", anchor="nw")

        # radio buttons for auto setting
        auto_options = ["Objective", "Intermediate", "Projective", "None"]
        auto_mode_buttons = RadioLayout(self, "Auto Setting", auto_options)
        auto_mode_buttons.pack(side="top", anchor="nw")


# radio button widgets layout
class RadioLayout(ttk.LabelFrame):

    def __init__(self, master, name, radio_names):
        super().__init__(master, text=name, borderwidth=5)
        for item in radio_names:
            button = ttk.Radiobutton(self, text=item)
            button.pack(side="left", anchor="nw")
