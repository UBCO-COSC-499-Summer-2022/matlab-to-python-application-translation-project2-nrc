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

        # Frame that holds the settings
        settings_frame = tk.Frame(self)
        settings_frame.pack(side="left", anchor="nw")

        # Upper Settings
        self.upper_menu = AboveSampleFrame(settings_frame)
        self.upper_menu.pack(
            side="top", anchor="nw",
            padx=PAD_X, pady=PAD_Y,
            fill="x", expand=True
        )
        self.upper_menu.c1_link.set_command(self.update_cf)
        self.upper_menu.c1_toggle.set_command(self.slider_status)
        self.upper_menu.c2_link.set_command(self.update_cf)
        self.upper_menu.c2_toggle.set_command(self.slider_status)
        self.upper_menu.c3_link.set_command(self.update_cf)
        self.upper_menu.c3_toggle.set_command(self.slider_status)

        # Lower Settings
        lower_menu = BelowSampleFrame(settings_frame)
        lower_menu.pack(
            side="top", anchor="nw",
            padx=PAD_X, fill="x",
            expand=True
        )

        # Frame that holds the results, diagram, diagram controls
        results_frame = tk.Frame(self)
        results_frame.pack(side="top", anchor="nw")

        # Results Window
        numerical_results = ResultsFrame(results_frame)
        numerical_results.pack(
            side="top", anchor="nw",
            padx=PAD_X, pady=PAD_Y,
            fill="x", expand=True
        )

        # Diagram
        self.diagram = DiagramFrame(results_frame)
        self.diagram.pack(
            side="top", anchor="nw",
            padx=PAD_X, pady=PAD_Y,
            fill="x", expand=True
        )

    # gets the values from all the slides and update list
    def update_cf(self, value):
        focal_values = [
            float(self.upper_menu.c1_link.get()),
            float(self.upper_menu.c2_link.get()),
            float(self.upper_menu.c3_link.get())
        ]
        self.diagram.update_focal_length(focal_values)

    # turns slider on and off based on toggle status + name
    def slider_status(self, toggle_status, name):
        if toggle_status:
            if name == "C1":
                self.upper_menu.c1_link.set_disabled(False)
                self.upper_menu.lens_status[0] = True
            elif name == "C2":
                self.upper_menu.c2_link.set_disabled(False)
                self.upper_menu.lens_status[1] = True
            else:
                self.upper_menu.c3_link.set_disabled(False)
                self.upper_menu.lens_status[2] = True
        else:
            if name == "C1":
                self.upper_menu.c1_link.set_disabled(True)
                self.upper_menu.lens_status[0] = False
            elif name == "C2":
                self.upper_menu.c2_link.set_disabled(True)
                self.upper_menu.lens_status[1] = False
            else:
                self.upper_menu.c3_link.set_disabled(True)
                self.upper_menu.lens_status[2] = False
        # self.diagram.update_active_lenses(self.upper_menu.lens_status)