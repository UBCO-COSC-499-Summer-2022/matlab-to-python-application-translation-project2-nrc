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
        self.geometry('1200x600')
        self.minsize(1200, 600)
        self.columnconfigure(0, weight=1)
        # Results Window
        numerical_results = ResultsFrame(self)
        numerical_results.grid(row=0, column=0, sticky="we")
        # Diagram
        self.diagram = DiagramFrame(self)
        self.diagram.grid(row=1, column=0, sticky="nwse")
        self.rowconfigure(1, weight=4)

        settings_frame = tk.Frame(self)
        settings_frame.grid(row=2, column=0, sticky="nwse")
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)
        # Upper Settings
        self.upper_menu = AboveSampleFrame(settings_frame)
        self.upper_menu.grid(row=0, column=0, sticky="nwse")
        self.upper_menu.c1_link.set_command(self.update_cf_c)
        self.upper_menu.c1_toggle.set_command(self.slider_status_c)
        self.upper_menu.c2_link.set_command(self.update_cf_c)
        self.upper_menu.c2_toggle.set_command(self.slider_status_c)
        self.upper_menu.c3_link.set_command(self.update_cf_c)
        self.upper_menu.c3_toggle.set_command(self.slider_status_c)

        # Lower Settings
        self.lower_menu = BelowSampleFrame(settings_frame)
        self.lower_menu.grid(row=0, column=1, sticky="nwse")
        self.lower_menu.distance_link.set_command(self.update_cf_b)
        self.lower_menu.objective_link.set_command(self.update_cf_b)
        self.lower_menu.objective_toggle.set_command(self.slider_status_b)
        self.lower_menu.intermediate_link.set_command(self.update_cf_b)
        self.lower_menu.intermediate_toggle.set_command(self.slider_status_b)
        self.lower_menu.projective_link.set_command(self.update_cf_b)
        self.lower_menu.projective_toggle.set_command(self.slider_status_b)
        self.lower_menu.opt_sel.trace(
            "w", lambda a, b, c: self.optimization_mode()
        )
        self.lower_menu.lens_sel.trace(
            "w", lambda a, b, c: self.optimization_mode()
        )

    # gets the values from all the slides and update lists
    def update_cf_c(self, value):
        self.diagram.cf_c = [
            float(self.upper_menu.c1_link.get()),
            float(self.upper_menu.c2_link.get()),
            float(self.upper_menu.c3_link.get())
        ]
        self.diagram.update_c_lenses()

    # turns slider on and off based on toggle status + name
    def slider_status_c(self, value):
        self.diagram.active_lenses_c = [
            self.upper_menu.c1_toggle.get_status(),
            self.upper_menu.c2_toggle.get_status(),
            self.upper_menu.c3_toggle.get_status()
        ]
        self.diagram.update_c_lenses()

    def update_cf_b(self, value):
        self.diagram.distance_from_optical = \
            float(self.lower_menu.distance_link.get()) * (10**-6)
        self.diagram.cf_b = [
            float(self.lower_menu.objective_link.get()),
            float(self.lower_menu.intermediate_link.get()),
            float(self.lower_menu.projective_link.get()),
        ]
        self.diagram.update_b_lenses(
            self.lower_menu.lens_sel.get() != -1,
            self.lower_menu.opt_sel.get(), self.lower_menu.lens_sel.get()
        )

    def slider_status_b(self, value):
        self.diagram.active_lenses_b = [
            self.lower_menu.objective_toggle.get_status(),
            self.lower_menu.intermediate_toggle.get_status(),
            self.lower_menu.projective_toggle.get_status(),
        ]
        self.diagram.update_b_lenses(
            self.self.lower_menu.lens_sel.get() != -1
        )

    def optimization_mode(self):
        if self.lower_menu.lens_sel.get() != -1:
            self.diagram.update_b_lenses(
                True, self.lower_menu.opt_sel.get(),
                self.lower_menu.lens_sel.get()
            )
