import tkinter as tk


class OptimizationSettingsFrame(tk.LabelFrame):

    def __init__(self, master, text):
        super().__init__(master, text=text, bd=1)
        self.columnconfigure(1, weight=1)

        self.cvs_file = tk.Radiobutton(self, text="Csv file")
        self.cvs_file.grid(row=0, column=0, sticky="w")

        self.constant_step = tk.Radiobutton(self, text="Constant step")
        self.constant_step.grid(row=1, column=0, sticky="w")

        start_angle_label = tk.Label(self, text="Start angle:")
        start_angle_label.grid(row=0, column=2)
        self.start_angle_input = tk.Entry(self)
        self.start_angle_input.grid(row=0, column=3)

        step_angle_label = tk.Label(self, text="Step angle:")
        step_angle_label.grid(row=1, column=2)
        self.step_angle_input = tk.Entry(self)
        self.step_angle_input.grid(row=1, column=3)
