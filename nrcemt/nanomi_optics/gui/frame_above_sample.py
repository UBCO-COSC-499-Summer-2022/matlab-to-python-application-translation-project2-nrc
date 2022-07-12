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

        # stores the values of the lenses
        self.lens_values = []

        # stores the status of the lenses on/off
        self.lens_status = [True, True, True]

        # frame that hold c1 slider, spinbox, and button
        c1_frame = ttk.Frame(self)
        c1_frame.pack(side="top", anchor="nw")

        c1_slider = SliderLayout(c1_frame, "Lens C1: ")
        self.c1_link = ScaleSpinboxLink(
            c1_slider.slider,
            c1_slider.entry,
            13, (0, 50)
        )
        self.c1_link.set_command(self.update_cf)
        c1_slider.pack(anchor="w", side="left", pady=PAD_Y)

        c1_toggle = ToggleButton(c1_frame, "C1")
        c1_toggle.set_command(self.slider_status)
        c1_toggle.pack(side="left", pady=PAD_Y)

        # frame that hold c2 slider, spinbox, and button
        c2_frame = ttk.Frame(self)
        c2_frame.pack(side="top", anchor="nw")

        c2_slider = SliderLayout(c2_frame, "Lens C2: ")
        self.c2_link = ScaleSpinboxLink(
            c2_slider.slider,
            c2_slider.entry,
            35, (0, 50)
        )
        self.c2_link.set_command(self.update_cf)
        c2_slider.pack(anchor="w", side="left", pady=PAD_Y)

        c2_toggle = ToggleButton(c2_frame, "C2")
        c2_toggle.set_command(self.slider_status)
        c2_toggle.pack(side="left", pady=PAD_Y)

        # frame that hold c3 slider, spinbox, and button
        c3_frame = ttk.Frame(self)
        c3_frame.pack(side="top", anchor="nw")

        c3_slider = SliderLayout(c3_frame, "Lens C3: ")
        self.c3_link = ScaleSpinboxLink(
            c3_slider.slider,
            c3_slider.entry,
            10.68545, (0, 50)
        )
        self.c3_link.set_command(self.update_cf)
        c3_slider.pack(anchor="w", side="left", pady=PAD_Y)

        c3_toggle = ToggleButton(c3_frame, "C3")
        c3_toggle.set_command(self.slider_status)
        c3_toggle.pack(side="left", pady=PAD_Y)

    # gets the values from all the slides and update list
    def update_cf(self, value):
        self.lens_values = (
            float(self.c1_link.get()),
            float(self.c2_link.get()),
            float(self.c3_link.get())
            )

    # turns slider on and off based on toggle status + name
    def slider_status(self, toggle_status, name):
        if toggle_status:
            if name == "C1":
                self.c1_link.set_disabled(False)
                self.lens_status[0] = True
            elif name == "C2":
                self.c2_link.set_disabled(False)
                self.lens_status[1] = True
            else:
                self.c3_link.set_disabled(False)
                self.lens_status[2] = True
        else:
            if name == "C1":
                self.c1_link.set_disabled(True)
                self.lens_status[0] = False
            elif name == "C2":
                self.c2_link.set_disabled(True)
                self.lens_status[1] = False
            else:
                self.c3_link.set_disabled(True)
                self.lens_status[2] = False
