import tkinter as tk
from tkinter import ttk

INPUT_WIDTH = 10
PADDING = 4


class ContrastToolFrame(tk.Frame):
    """Frame for the controls at the top of the contrast window."""

    def __init__(self, master):
        """Create the frame."""
        super().__init__(master)

        # Frame for Data Range
        data_frame = tk.LabelFrame(self, bd=1, text="Data Range")
        data_frame.grid(row=0, column=0, sticky="nwse")

        # Frame for Scale Display Range
        scale_frame = tk.LabelFrame(self, bd=1, text="Scale Display")
        scale_frame.grid(row=0, column=1, sticky="nwse")

        # Minimum data
        min_label = ttk.Label(scale_frame, text="Minimum:")
        min_label.grid(row=0, column=0, pady=PADDING)
        min_range = tk.Frame(scale_frame)
        self.min_range_val = ttk.Label(min_range, text="0")
        self.min_range_val.pack()
        min_range.grid(row=0, column=1, pady=PADDING)

        # Max Data
        max_label = ttk.Label(scale_frame, text="Maximum:")
        max_label.grid(row=1, column=0, pady=PADDING)
        max_range = tk.Frame(scale_frame)
        self.max_range_val = ttk.Label(max_range, text="1")
        self.max_range_val.pack()
        max_range.grid(row=1, column=1, pady=PADDING)

        self.discrete_var = tk.BooleanVar(value=True)
        apply_discretely = ttk.Checkbutton(
            data_frame, text="Adjust discretely",
            variable=self.discrete_var
        )
        apply_discretely.grid(row=1, column=0)

        eliminate_outliers = ttk.Label(data_frame, text="Rejection percentile")
        eliminate_outliers.grid(row=0, column=0)
        self.percentile_var = tk.DoubleVar(value=2.0)
        outlier_percentile = ttk.Entry(
            data_frame, textvariable=self.percentile_var, width=INPUT_WIDTH
        )
        outlier_percentile.grid(row=0, column=1)

        slider_frame = tk.LabelFrame(self, bd=1, text="Manual adjustment")
        slider_frame.grid(row=1, column=0)
        label_min = ttk.Label(slider_frame, text="min: ")
        label_min.grid(row=0, column=0)
        self.slider_min = ttk.Scale(slider_frame, length=200, value=0.0)
        self.slider_min.grid(row=0, column=1)
        label_max = ttk.Label(slider_frame, text="max: ")
        label_max.grid(row=1, column=0)
        self.slider_max = ttk.Scale(slider_frame, length=200, value=1.0)
        self.slider_max.grid(row=1, column=1)

        self.apply = ttk.Button(data_frame, text="Apply")
        self.apply.grid(row=1, column=1)
