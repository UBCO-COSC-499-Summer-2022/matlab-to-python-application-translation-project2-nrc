import tkinter as tk
from tkinter import ttk

X_PADDING = 2
Y_PADDING = 2


class PlasmonSelect(ttk.Frame):

    def __init__(self, master, name, radio_variable, radio_value):
        super().__init__(master)

        # creating variables
        self.x_var = tk.IntVar()
        self.x_var.set(0)
        self.y_var = tk.IntVar()
        self.y_var.set(0)
        self.radio_value = radio_value

        # new frame that contains labels and entry boxes
        entry_frame = ttk.Frame(self)

        # creates styling for radio buttons
        # creates the radio button
        radio_btn = ttk.Radiobutton(
            self, text=name,
            width=21,
            variable=radio_variable,
            value=radio_value
        )
        radio_btn.pack(anchor="w")

        # creates label
        x_label = ttk.Label(entry_frame, text="X: ")
        x_label.pack(side="left", padx=X_PADDING, pady=Y_PADDING)

        # Creates entry box
        x_entry = ttk.Entry(entry_frame, width=5, textvariable=self.x_var)
        x_entry.pack(side="left", padx=X_PADDING, pady=Y_PADDING)

        # creates label
        y_label = ttk.Label(entry_frame, text="Y: ")
        y_label.pack(side="left", padx=X_PADDING, pady=Y_PADDING)

        # Creates entry box
        y_entry = ttk.Entry(entry_frame, width=5, textvariable=self.y_var)
        y_entry.pack(side="left", padx=X_PADDING, pady=Y_PADDING)
        entry_frame.pack()


class ResultBoxes(ttk.Frame):

    def __init__(self, master, name):
        super().__init__(master)
        # Creating variables
        self.result_var = tk.DoubleVar()
        ev_label = ttk.Label(self, text=name + ": ", width=20)
        ev_entry = ttk.Entry(self, width=10, textvariable=self.result_var)
        ev_label.pack(side="left", pady=X_PADDING)
        ev_entry.pack(side="left", pady=Y_PADDING)


class WidthComponent(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)

        # Creates variables
        self.width_var = tk.IntVar()
        self.detect_var = tk.BooleanVar()
        self.width_var.set(60)
        self.detect_var.set(False)

        # Creating width label and entry box
        width_label = ttk.Label(self, text="Width: ")
        width_entry = ttk.Entry(self, width=5, textvariable=self.width_var)

        # creating detect checkbox
        detect_checkbox = ttk.Checkbutton(
            self, text="Detect",
            variable=self.detect_var
        )

        # Placing above items
        width_label.pack(side="left", padx=X_PADDING, pady=Y_PADDING)
        width_entry.pack(side="left", pady=Y_PADDING, padx=X_PADDING)
        detect_checkbox.pack(side="left", padx=X_PADDING, pady=Y_PADDING)
