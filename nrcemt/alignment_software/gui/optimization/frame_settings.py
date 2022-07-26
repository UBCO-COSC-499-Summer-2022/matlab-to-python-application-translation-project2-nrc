import tkinter as tk

from nrcemt.common.gui.numericspinbox import NumericSpinbox

ENTRY_WIDTH = 5


class OptimizationSettingsFrame(tk.LabelFrame):

    def __init__(self, master, text):
        super().__init__(master, text=text, bd=1)
        self.columnconfigure(2, weight=1)

        self.tilt_var = tk.StringVar(self, "constant")
        csv_file = tk.Radiobutton(
            self, text="Csv file", value="csv", variable=self.tilt_var
        )
        csv_file.grid(row=0, column=0, sticky="w")
        constant_step = tk.Radiobutton(
            self, text="Constant step", value="constant",
            variable=self.tilt_var
        )
        constant_step.grid(row=1, column=0, sticky="w")

        start_angle_label = tk.Label(self, text="Start angle:")
        start_angle_label.grid(row=0, column=2)
        self.start_angle_input = NumericSpinbox(
            self, value_default=0, value_range=(0, 360), value_type=float,
            width=ENTRY_WIDTH
        )
        self.start_angle_input.grid(row=0, column=3)

        step_angle_label = tk.Label(self, text="Step angle:")
        step_angle_label.grid(row=1, column=2)
        self.step_angle_input = NumericSpinbox(
            self, value_default=3, value_range=(0, 60), value_type=float,
            width=ENTRY_WIDTH
        )
        self.step_angle_input.grid(row=1, column=3)
