import tkinter as tk
from tkinter import ttk

from .common import NumericSpinbox

X_PADDING = 2
Y_PADDING = 2


class PlasmonSelect(ttk.Frame):
    """
    Creates the GUI widgets for each plasmon parts (i.e. bulk plasmon 1)
    """
    def __init__(self, master, name, radio_variable, radio_value):
        super().__init__(master)

        # creates styling for radio buttons
        # creates the radio button
        self.radio_value = radio_value
        radio_btn = ttk.Radiobutton(
            self, text=name,
            width=21,
            variable=radio_variable,
            value=radio_value
        )
        radio_btn.pack(anchor="w")

        # new frame that contains labels and entry boxes
        entry_frame = ttk.Frame(self)
        entry_frame.pack()

        # creates label
        x_label = ttk.Label(entry_frame, text="X: ")
        x_label.pack(side="left", padx=X_PADDING, pady=Y_PADDING)

        # Creates entry box
        self.x = NumericSpinbox(entry_frame, value_range=(0, 1024), width=5)
        self.x.pack(side="left", padx=X_PADDING, pady=Y_PADDING)

        # creates label
        y_label = ttk.Label(entry_frame, text="Y: ")
        y_label.pack(side="left", padx=X_PADDING, pady=Y_PADDING)

        # Creates entry box
        self.y = NumericSpinbox(entry_frame, value_range=(0, 1024), width=5)
        self.y.pack(side="left", padx=X_PADDING, pady=Y_PADDING)

    def set_image_size(self, width, height):
        self.x.set_value_range(0, width-1)
        self.y.set_value_range(0, height-1)


class ResultBox(ttk.Frame):
    """
    Creates GUI Widgets for each result feild (i.e. ev/pixel)
    """
    def __init__(self, master, name, value):
        super().__init__(master)
        self.result_var = tk.DoubleVar()
        result_label = ttk.Label(self, text=name + ": ", width=20)
        result_label.pack(side="left", pady=X_PADDING)
        self.result = NumericSpinbox(
            self, value, value_type=float, value_range=(0, 999999)
        )
        self.result.pack(side="left", pady=Y_PADDING)


class WidthComponent(ttk.Frame):
    """
    Creates the width and detect box widgets for each of the
    plasmons (i.e. bulk plasmon)
    """

    def __init__(self, master):
        super().__init__(master)

        # Creates variables
        self.detect = tk.BooleanVar()
        self.detect.set(False)

        # Creating width label and entry box
        width_label = ttk.Label(self, text="Width: ")
        self.width = NumericSpinbox(
            self, width=5, value_default=60, value_range=(1, 999)
        )

        # creating detect checkbox
        detect_checkbox = ttk.Checkbutton(
            self, text="Detect",
            variable=self.detect
        )

        # Placing above items
        width_label.pack(side="left", padx=X_PADDING, pady=Y_PADDING)
        self.width.pack(side="left", pady=Y_PADDING, padx=X_PADDING)
        detect_checkbox.pack(side="left", padx=X_PADDING, pady=Y_PADDING)
