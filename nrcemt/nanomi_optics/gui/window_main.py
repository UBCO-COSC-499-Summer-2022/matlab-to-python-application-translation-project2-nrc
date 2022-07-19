import tkinter as tk
from .frame_above_sample import AboveSampleFrame
from .frame_below_sample import BelowSampleFrame
from .frame_results import ResultsFrame
from .frame_diagram import DiagramFrame

PAD_X = 20
PAD_Y = 20


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        # set title of window
        self.title('Nanomi Optics')
        # set window size
        self.geometry('1200x800')
        self.minsize(600, 450)


        # Upper Settings
        self.upper_menu = AboveSampleFrame(self)
        self.upper_menu.pack(
            side="top", anchor="nw",
            padx=PAD_X, pady=PAD_Y,
            fill="x", expand=True
        )
        self.upper_menu.c1_link.set_command(self.update_cf_c)
        self.upper_menu.c1_toggle.set_command(self.slider_status_c)
        self.upper_menu.c2_link.set_command(self.update_cf_c)
        self.upper_menu.c2_toggle.set_command(self.slider_status_c)
        self.upper_menu.c3_link.set_command(self.update_cf_c)
        self.upper_menu.c3_toggle.set_command(self.slider_status_c)

        # Lower Settings
        self.lower_menu = BelowSampleFrame(self)
        self.lower_menu.pack(
            side="top", anchor="nw",
            padx=PAD_X, fill="x",
            expand=True
        )

        self.lower_menu.distance_link.set_command(self.update_cf_b)
        self.lower_menu.objective_link.set_command(self.update_cf_b)
        self.lower_menu.objective_toggle.set_command(self.slider_status_b)
        self.lower_menu.intermediate_link.set_command(self.update_cf_b)
        self.lower_menu.intermediate_toggle.set_command(self.slider_status_b)
        self.lower_menu.projective_link.set_command(self.update_cf_b)
        self.lower_menu.projective_toggle.set_command(self.slider_status_b)

        # Results Window
        numerical_results = ResultsFrame(self)
        numerical_results.pack(
            side="top", anchor="nw",
            padx=PAD_X, pady=PAD_Y,
            fill="x", expand=True
        )

        # Diagram
        self.diagram = DiagramFrame(self)
        self.diagram.pack(
            side="top", anchor="nw",
            padx=PAD_X, pady=PAD_Y,
            fill="x", expand=True
        )

    # gets the values from all the slides and update lists
    def update_cf_c(self, value):
        self.upper_menu.focal_values = [
            float(self.upper_menu.c1_link.get()),
            float(self.upper_menu.c2_link.get()),
            float(self.upper_menu.c3_link.get())
        ]
        self.diagram.update_c_lenses(
            self.upper_menu.focal_values, self.upper_menu.lens_status
        )

    # turns slider on and off based on toggle status + name
    def slider_status_c(self, value):
        self.upper_menu.lens_status = [
            self.upper_menu.c1_toggle.get_status(),
            self.upper_menu.c2_toggle.get_status(),
            self.upper_menu.c3_toggle.get_status()
        ]
        self.diagram.update_c_lenses(
            self.upper_menu.focal_values, self.upper_menu.lens_status
        )

    def update_cf_b(self, value):
        self.lower_menu.slider_values = [
            float(self.lower_menu.distance_link.get()),
            float(self.lower_menu.objective_link.get()),
            float(self.lower_menu.intermediate_link.get()),
            float(self.lower_menu.projective_link.get()),
        ]
        self.diagram.update_b_lenses(
            self.lower_menu.slider_values, self.lower_menu.lens_status
        )

    def slider_status_b(self, value):
        self.lower_menu.lens_status = [
            self.lower_menu.objective_toggle.get_status(),
            self.lower_menu.intermediate_toggle.get_status(),
            self.lower_menu.projective_toggle.get_status(),
        ]
        self.diagram.update_b_lenses(
            self.lower_menu.slider_values, self.lower_menu.lens_status
        )
