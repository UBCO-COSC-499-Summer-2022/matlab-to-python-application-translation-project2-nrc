from tkinter import ttk
from .widget_templates import SliderLayout, RadioLayout, ToggleButton
from nrcemt.common.gui import ScaleSpinboxLink

PAD_Y = 5


# widgetsfor the settings below the sample
class BelowSampleFrame(ttk.LabelFrame):

    def __init__(self, master):
        super().__init__(master, text="Settings below sample", borderwidth=5)

        # stores the values of the sliders
        self.slider_values = [10, 19.670, 6.498, 6]

        # stores the status of the lenses on/off
        self.lens_status = [True, True, True]

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

        self.distance_slider = SliderLayout(distance_frame, "Distance:")
        self.distance_link = ScaleSpinboxLink(
            self.distance_slider.slider,
            self.distance_slider.entry,
            self.slider_values[0], (0, 100)
        )
        self.distance_slider.pack(anchor="w", side="left", pady=PAD_Y)

        # frame that holds objective slider and button
        objective_frame = ttk.Frame(self)
        objective_frame.pack(side="top", anchor="nw")

        self.objective_slider = SliderLayout(objective_frame, "Objective:")
        self.objective_link = ScaleSpinboxLink(
            self.objective_slider.slider,
            self.objective_slider.entry,
            self.slider_values[1], (6, 300)
        )
        self.objective_slider.pack(anchor="w", side="left", pady=PAD_Y)

        objective_toggle = ToggleButton(objective_frame)
        objective_toggle.pack(side="left", pady=PAD_Y)

        # frame that holds intermediate slider and button
        intermediate_frame = ttk.Frame(self)
        intermediate_frame.pack(side="top", anchor="nw")

        self.intermediate_slider = SliderLayout(
            intermediate_frame, "Intermediate:"
        )
        self.intermediate_link = ScaleSpinboxLink(
            self.intermediate_slider.slider,
            self.intermediate_slider.entry,
            self.slider_values[2], (6, 300)
        )
        self.intermediate_slider.pack(anchor="w", side="left", pady=PAD_Y)

        intermediate_toggle = ToggleButton(intermediate_frame)
        intermediate_toggle.pack(side="left", pady=PAD_Y)

        # frame that holds projective slider and button
        projective_frame = ttk.Frame(self)
        projective_frame.pack(side="top", anchor="nw")

        self.projective_slider = SliderLayout(projective_frame, "Projective:")
        self.projective_link = ScaleSpinboxLink(
            self.projective_slider.slider,
            self.projective_slider.entry,
            self.slider_values[3], (6, 300)
        )
        self.projective_slider.pack(anchor="w", side="left", pady=PAD_Y)

        projective_toggle = ToggleButton(projective_frame)
        projective_toggle.pack(side="left", pady=PAD_Y)
