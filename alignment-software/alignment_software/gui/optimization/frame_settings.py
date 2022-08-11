import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename

from common.gui.numericspinbox import NumericSpinbox

ENTRY_WIDTH = 5


class OptimizationSettingsFrame(tk.LabelFrame):

    def __init__(self, master, text):
        super().__init__(master, text=text, bd=1)
        self.columnconfigure(2, weight=1)

        self.tilt_var = tk.StringVar(self, "constant")
        self.tilt_var.trace('w', lambda a, b, c: self.update_selection())
        constant_step = tk.Radiobutton(
            self, text="Constant step", value="constant",
            variable=self.tilt_var
        )
        constant_step.grid(row=0, column=0, sticky="w")
        csv_file = tk.Radiobutton(
            self, text="Csv file", value="csv", variable=self.tilt_var
        )
        csv_file.grid(row=1, column=0, sticky="w")

        start_angle_label = tk.Label(self, text="Start angle:")
        start_angle_label.grid(row=0, column=2)
        self.start_angle = NumericSpinbox(
            self, value_default=0, value_range=(0, 360), value_type=float,
            width=ENTRY_WIDTH
        )
        self.start_angle.grid(row=0, column=3)

        step_angle_label = tk.Label(self, text="Step angle:")
        step_angle_label.grid(row=1, column=2)
        self.step_angle = NumericSpinbox(
            self, value_default=3, value_range=(0, 60), value_type=float,
            width=ENTRY_WIDTH
        )
        self.step_angle.grid(row=1, column=3)

        self.csv_button = ttk.Button(
            self, text="open csv", command=self.open_csv
        )
        self.csv_button.grid(row=2, column=0, columnspan=2, sticky="we")
        self.csv_path_var = tk.StringVar(self, "")
        self.csv_entry = ttk.Entry(self, textvariable=self.csv_path_var)
        self.csv_entry.grid(row=2, column=2, columnspan=2, sticky="we")
        self.update_selection()

    def update_selection(self):
        tilt_mode = self.tilt_var.get()
        if tilt_mode == "csv":
            self.csv_button.config(state="normal")
            self.csv_entry.config(state="normal")
        else:
            self.csv_button.config(state="disabled")
            self.csv_entry.config(state="disabled")

    def open_csv(self):
        filename = askopenfilename(filetypes=[("CSV File", "*.csv")])
        if filename:
            self.csv_path_var.set(filename)
