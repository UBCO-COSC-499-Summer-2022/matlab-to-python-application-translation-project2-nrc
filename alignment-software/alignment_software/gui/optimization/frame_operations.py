import tkinter as tk

from common.gui.numericspinbox import NumericSpinbox

ENTRY_WIDTH = 5


class OperationsFrame(tk.LabelFrame):

    def __init__(self, master, text):
        super().__init__(master, text=text, bd=1)
        self.columnconfigure(0, weight=1)

        self.operation_var = tk.StringVar(self, "fixrot-fixmag")

        fixed_rotation = tk.Radiobutton(
            self, text="Fixed rotation and magnification:",
            value="fixrot-fixmag", variable=self.operation_var
        )
        fixed_rotation.grid(row=0, column=0, sticky="w")
        one_rotation = tk.Radiobutton(
            self, text="One rotation and fixed magnification",
            value="onerot-fixmag", variable=self.operation_var
        )
        one_rotation.grid(row=1, column=0, sticky="w")
        groupm_one_rotation = tk.Radiobutton(
            self, text="Group magnifications and one rotation",
            value="onerot-groupmag", variable=self.operation_var
        )
        groupm_one_rotation.grid(row=2, column=0, sticky="w")

        groupm_group_rotation = tk.Radiobutton(
            self, text="Group magnifications and group rotations",
            value="grouprot-groupmag", variable=self.operation_var
        )
        groupm_group_rotation.grid(row=3, column=0, sticky="w")

        self.input_angle = NumericSpinbox(
            self, value_default=0, value_range=(0, 360), value_type=float,
            width=ENTRY_WIDTH
        )
        self.input_angle.grid(row=0, column=1)

        self.azimuth_var = tk.BooleanVar(self, False)
        azimuth_check = tk.Checkbutton(
            self, text="Adjust azimuth angle amount:",
            variable=self.azimuth_var
        )
        azimuth_check.grid(row=4, column=0, sticky="w")
        self.azimuth_input_angle = NumericSpinbox(
            self, value_default=0, value_range=(0, 360), value_type=float,
            width=ENTRY_WIDTH
        )
        self.azimuth_input_angle.grid(row=4, column=1)

        self.tilt_group_var = tk.BooleanVar(self, False)
        group_tilt_angles = tk.Checkbutton(
            self, text="Group tilt angles", variable=self.tilt_group_var
        )
        group_tilt_angles.grid(row=5, column=0, sticky="w")

        accuracy_label = tk.Label(self, text="Accuracy")
        accuracy_label.grid(row=6, column=0, sticky="e")
        self.accuracy_result = tk.Label(
            self, text="0", bd=1, relief="solid",
            bg="white", fg="black", width=ENTRY_WIDTH
        )
        self.accuracy_result.grid(row=6, column=1)
