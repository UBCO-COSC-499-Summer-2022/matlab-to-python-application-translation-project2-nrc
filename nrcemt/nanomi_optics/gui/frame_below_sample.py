from tkinter import ttk
from .widget_templates import SliderLayout, RadioLayout, ToggleButton

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

        # frame that holds distance slider and button
        distance_frame = ttk.Frame(self)
        distance_frame.pack(side="top", anchor="nw")

        distance_slider = SliderLayout(distance_frame, "Distance:")
        distance_slider.pack(side="left", pady=PAD_Y)

        distance_toggle = ToggleButton(distance_frame, "Distance")
        distance_toggle.pack(side="left", pady=PAD_Y)

        # frame that holds objective slider and button
        objective_frame = ttk.Frame(self)
        objective_frame.pack(side="top", anchor="nw")

        objective_slider = SliderLayout(objective_frame, "Objective:")
        objective_slider.pack(side="left", pady=PAD_Y)

        objective_toggle = ToggleButton(objective_frame, "Objective")
        objective_toggle.pack(side="left", pady=PAD_Y)

        # frame that holds intermediate slider and button
        intermediate_frame = ttk.Frame(self)
        intermediate_frame.pack(side="top", anchor="nw")

        intermediate_slider = SliderLayout(intermediate_frame, "Intermediate:")
        intermediate_slider.pack(side="left", pady=PAD_Y)

        intermediate_toggle = ToggleButton(intermediate_frame, "Intermediate")
        intermediate_toggle.pack(side="left", pady=PAD_Y)

        # frame that holds projective slider and button
        projective_frame = ttk.Frame(self)
        projective_frame.pack(side="top", anchor="nw")

        projective_slider = SliderLayout(projective_frame, "Projective:")
        projective_slider.pack(side="left", pady=PAD_Y)

        projective_toggle = ToggleButton(projective_frame, "Projective")
        projective_toggle.pack(side="left", pady=PAD_Y)
