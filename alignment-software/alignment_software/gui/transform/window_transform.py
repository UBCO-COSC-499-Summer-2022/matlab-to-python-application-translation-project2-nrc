import tkinter as tk
from tkinter import ttk
from ..common import ScaleSpinboxLink


class TransformWindow(tk.Toplevel):
    """Tkinter window for transformation, has a bunch of sliders."""

    def __init__(self, master):
        """Create transform window."""
        super().__init__(master)
        self.title("Image Transformation Window")
        self.resizable(True, False)

        self.command = None

        self.columnconfigure(1, weight=1)

        input_labels = [
            "Offset X (percent)",
            "Offset Y (percent)",
            "Scale (percent)",
            "Angle (degree)"
        ]
        for i, label in enumerate(input_labels):
            label = ttk.Label(self, text=label, justify="right")
            label.grid(row=i, column=0, sticky="e")
            scale = ttk.Scale(self, length=300)
            scale.grid(row=i, column=1, sticky="w")
            entry = ttk.Spinbox(self, width=10)
            entry.grid(row=i, column=2)
            if i == 0:
                self.offset_x = ScaleSpinboxLink(scale, entry, 0, (-1, 1))
            elif i == 1:
                self.offset_y = ScaleSpinboxLink(scale, entry, 0, (-1, 1))
            elif i == 2:
                self.scale = ScaleSpinboxLink(scale, entry, 1, (0, 2))
            elif i == 3:
                self.angle = ScaleSpinboxLink(scale, entry, 0, (0, 360))

        label = ttk.Label(self, text="Binning", justify="right")
        label.grid(row=4, column=0, sticky="e")
        binning_frame = ttk.Frame(self)
        binning_frame.grid(row=4, column=1, sticky="w")
        self.binning_var = tk.IntVar(self, 1)
        for i in range(4):
            radio_button = ttk.Radiobutton(
                binning_frame, text=2**i, variable=self.binning_var, value=2**i
            )
            radio_button.pack(side="left", padx=2)

        label = ttk.Label(self, text="Sobel Filter", justify="right")
        label.grid(row=5, column=0, sticky="e")
        self.sobel_var = tk.BooleanVar(self, False)
        sobel_check = ttk.Checkbutton(self, variable=self.sobel_var)
        sobel_check.grid(row=5, column=1, sticky="w", padx=2)

        reset_button = ttk.Button(self, text="Reset", command=self.reset)
        reset_button.grid(row=6, column=0, columnspan=3, sticky="we")

    def reset(self):
        """Reset all controls back to their defaults."""
        self.sobel_var.set(False)
        self.binning_var.set(1)
        self.offset_x.set(0)
        self.offset_y.set(0)
        self.scale.set(1)
        self.angle.set(0)
        if self.command is not None:
            self.command()

    def set_command(self, command):
        """Set command to be called when transform updates."""
        self.command = command
        self.sobel_var.trace('w', lambda a, b, c: command())
        self.binning_var.trace('w', lambda a, b, c: command())
        self.offset_x.set_command(lambda a: command())
        self.offset_y.set_command(lambda a: command())
        self.scale.set_command(lambda a: command())
        self.angle.set_command(lambda a: command())

    def set_transform(self, transform):
        """Set the parameters from a dictionary."""
        self.sobel_var.set(transform['sobel'])
        self.binning_var.set(transform['binning'])
        self.offset_x.set(transform['offset_x'])
        self.offset_y.set(transform['offset_y'])
        self.scale.set(transform['scale'])
        self.angle.set(transform['angle'])

    def get_tranform(self):
        """Returns the transform as a dictionary."""
        return {
            "sobel": self.sobel_var.get(),
            "binning": self.binning_var.get(),
            "offset_x": self.offset_x.get(),
            "offset_y": self.offset_y.get(),
            "scale": self.scale.get(),
            "angle": self.angle.get()
        }
