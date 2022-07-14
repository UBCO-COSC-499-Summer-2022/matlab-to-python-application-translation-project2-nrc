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
        self.lower_menu = BelowSampleFrame(settings_frame)
        self.lower_menu.pack(
            side="top", anchor="nw",
            padx=PAD_X, fill="x",
            expand=True
        )

        self.lower_menu.distance_link.set_command(self.update_cf)
        self.lower_menu.objective_link.set_command(self.update_cf)
        self.lower_menu.objective_toggle.set_command(self.slider_status)
        self.lower_menu.intermediate_link.set_command(self.update_cf)
        self.lower_menu.intermediate_toggle.set_command(self.slider_status)
        self.lower_menu.projective_link.set_command(self.update_cf)
        self.lower_menu.projective_toggle.set_command(self.slider_status)

        # Frame that holds the results, diagram, diagram controls
        results_frame = tk.Frame(self)
        results_frame.pack(side="top", anchor="nw")

        # Results Window
        self.numerical_results = ResultsFrame(results_frame)
        self.numerical_results.pack(
            side="top", anchor="nw",
            padx=PAD_X, pady=PAD_Y,
            fill="x", expand=True
        )
        self.numerical_results.save_button.set_command(self.save_results)

        # Diagram
        self.diagram = DiagramFrame(results_frame)
        self.diagram.pack(
            side="top", anchor="nw",
            padx=PAD_X, pady=PAD_Y,
            fill="x", expand=True
        )

    # gets the values from all the slides and update lists
    def update_cf(self, value):
        self.upper_menu.focal_values = [
            float(self.upper_menu.c1_link.get()),
            float(self.upper_menu.c2_link.get()),
            float(self.upper_menu.c3_link.get())
        ]
        self.diagram.update_lenses(
            self.upper_menu.focal_values, self.upper_menu.lens_status
        )
        self.lower_menu.slider_values = [
            float(self.lower_menu.distance_link.get()),
            float(self.lower_menu.objective_link.get()),
            float(self.lower_menu.intermediate_link.get()),
            float(self.lower_menu.projective_link.get()),
        ]

    # turns slider on and off based on toggle status + name
    def slider_status(self, value):
        self.upper_menu.lens_status = [
            self.upper_menu.c1_toggle.get_status(),
            self.upper_menu.c2_toggle.get_status(),
            self.upper_menu.c3_toggle.get_status()
        ]
        self.diagram.update_lenses(
            self.upper_menu.focal_values, self.upper_menu.lens_status
        )
        self.lower_menu.lens_status = [
            self.lower_menu.objective_toggle.get_status(),
            self.lower_menu.intermediate_toggle.get_status(),
            self.lower_menu.projective_toggle.get_status(),
        ]

    # save results
    def save_results(self):
        print("reached")
        save_path = tk.filedialog.asksaveasfile(
            mode='w',
            defaultextension=".csv",
            filetypes=[("CSV File", "*.csv")]
        )
        if save_path is not None:
            save_path = save_path.name
