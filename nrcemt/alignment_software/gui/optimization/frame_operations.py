import tkinter as tk

ENTRY_WIDTH = 5


class OperationsFrame(tk.LabelFrame):

    def __init__(self, master, text):
        super().__init__(master, text=text, bd=1)
        self.columnconfigure(0, weight=1)

        self.fixed_rotation = tk.Radiobutton(
            self, text="Fixed rotation and magnification:"
        )
        self.fixed_rotation.grid(row=0, column=0, sticky="w")
        self.input_angle = tk.Entry(self, width=ENTRY_WIDTH)
        self.input_angle.grid(row=0, column=1)

        self.one_rotation = tk.Radiobutton(
            self, text="One rotation and fixed magnification:"
        )
        self.one_rotation.grid(row=1, column=0, sticky="w")

        self.groupm_one_rotation = tk.Radiobutton(
            self, text="Group magnifications and one rotation:"
        )
        self.groupm_one_rotation.grid(row=2, column=0, sticky="w")

        self.groupm_group_rotation = tk.Radiobutton(
            self, text="Group magnifications and group rotations:"
        )
        self.groupm_group_rotation.grid(row=3, column=0, sticky="w")

        self.azimuth_angle = tk.Checkbutton(
            self, text="Adjust azimuth angle amount:"
        )
        self.azimuth_angle.grid(row=4, column=0, sticky="w")
        self.azimuth_angle_input = tk.Entry(self, width=ENTRY_WIDTH)
        self.azimuth_angle_input.grid(row=4, column=1)

        self.group_tilt_angles = tk.Checkbutton(
            self, text="Group tilt angles:"
        )
        self.group_tilt_angles.grid(row=5, column=0, sticky="w")

        accuracy_label = tk.Label(self, text="Accuracy")
        accuracy_label.grid(row=6, column=0, sticky="e")
        self.accuracy_result = tk.Label(
            self, text="0", bd=1, relief="solid",
            bg="white", fg="black", width=ENTRY_WIDTH
        )
        self.accuracy_result.grid(row=6, column=1)
