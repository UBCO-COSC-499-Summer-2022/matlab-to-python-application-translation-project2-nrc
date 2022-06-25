import tkinter as tk
from tkinter import ttk
from nrcemt.common.gui import ScaleSpinboxLink


class TranformWindow(tk.Toplevel):

    def __init__(self, master, max_x, max_y):
        super().__init__(master)
        self.title("Image Transformation Window")

        self.columnconfigure(1, weight=1)

        label = ttk.Label(self, text="Sobel Filter", justify="right")
        label.grid(row=0, column=0, sticky="e")
        check_button = ttk.Checkbutton(self)
        check_button.grid(row=0, column=1, sticky="w", padx=2)

        label = ttk.Label(self, text="Binning", justify="right")
        label.grid(row=1, column=0, sticky="e")
        binning_frame = ttk.Frame(self)
        binning_frame.grid(row=1, column=1, sticky="w")
        for i in range(4):
            radio_button = ttk.Radiobutton(binning_frame, text=2**i)
            radio_button.pack(side="left", padx=2)

        input_labels = [
            "Offset X (pixel)",
            "Offset Y (pixel)",
            "Scale (percent)",
            "Angle (degree)"
        ]
        for i, label in enumerate(input_labels):
            label = ttk.Label(self, text=label, justify="right")
            label.grid(row=2+i, column=0, sticky="e")
            scale = ttk.Scale(self, length=360)
            scale.grid(row=2+i, column=1, sticky="w")
            spinbox = ttk.Spinbox(self, width=10)
            spinbox.grid(row=2+i, column=2)
            if i == 0:
                self.offset_x = ScaleSpinboxLink(scale, spinbox, 0, (0, max_x))
            elif i == 1:
                self.offset_y = ScaleSpinboxLink(scale, spinbox, 0, (0, max_y))
            elif i == 2:
                self.scale = ScaleSpinboxLink(scale, spinbox, 0, (0, 200))
            elif i == 3:
                self.angle = ScaleSpinboxLink(scale, spinbox, 0, (0, 360))
