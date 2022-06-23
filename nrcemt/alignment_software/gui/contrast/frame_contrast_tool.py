import tkinter as tk
from tkinter import ttk

INPUT_WIDTH = 10
PADDING = 4


class ContrastToolFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        # Frame for Data Range
        data_range = tk.LabelFrame(self, bd=1, text="Data Range")
        data_range.grid(row=0, column=0, sticky="nwse")
        self.fill_data_range(data_range)

        # # Frame for Window
        # window = tk.LabelFrame(self, bd=1, text="Window")
        # window.grid(row=0, column=1, sticky="nwse")
        # self.fill_window(window)

        # Frame for Scale Display Range
        scale_display = tk.LabelFrame(self, bd=1, text="Scale Display")
        scale_display.grid(row=0, column=1, sticky="nwse")
        self.fill_scale_display(scale_display)

    def fill_data_range(self, frame):

        # Minimum data
        min_label = ttk.Label(frame, text="Minimum:")
        min_label.grid(row=0, column=0, pady=PADDING)
        min_range = tk.Frame(frame)
        self.min_range_val = ttk.Label(min_range, text="0")
        self.min_range_val.pack()
        min_range.grid(row=0, column=1, pady=PADDING)

        # Max Data
        max_label = ttk.Label(frame, text="Maximum:")
        max_label.grid(row=1, column=0, pady=PADDING)
        max_range = tk.Frame(frame)
        self.max_range_val = ttk.Label(max_range, text="1")
        self.max_range_val.pack()
        max_range.grid(row=1, column=1, pady=PADDING)

    # def fill_window(self, frame):

    #     # Minimum
    #     min_label = ttk.Label(frame, text="Minimum:")
    #     min_label.grid(row=0, column=0)
    #     min_val = tk.Entry(frame, width=INPUT_WIDTH)
    #     min_val.grid(row=0, column=1)

    #     # Max
    #     max_label = ttk.Label(frame, text="Maximum:")
    #     max_label.grid(row=1, column=0)
    #     max_val = tk.Entry(frame, width=INPUT_WIDTH)
    #     max_val.grid(row=1, column=1)

    #     # Width
    #     width_label = ttk.Label(frame, text="Width:")
    #     width_label.grid(row=0, column=2)
    #     width_val = tk.Entry(frame, width=INPUT_WIDTH)
    #     width_val.grid(row=0, column=3)

    #     # Center
    #     center_label = ttk.Label(frame, text="Center:")
    #     center_label.grid(row=1, column=2)
    #     center_val = tk.Entry(frame, width=INPUT_WIDTH)
    #     center_val.grid(row=1, column=3)

    def fill_scale_display(self, frame):

        self.discrete_var = tk.BooleanVar(value=True)
        apply_discretely = ttk.Checkbutton(
            frame, text="Adjust discretely",
            variable=self.discrete_var
        )
        apply_discretely.grid(row=1, column=0)

        eliminate_outliers = ttk.Label(frame, text="Rejection percentile")
        eliminate_outliers.grid(row=0, column=0)
        self.percentile_var = tk.DoubleVar(value=2.0)
        outlier_percentile = ttk.Entry(
            frame, textvariable=self.percentile_var, width=INPUT_WIDTH
        )
        outlier_percentile.grid(row=0, column=1)

        self.apply = ttk.Button(frame, text="Apply")
        self.apply.grid(row=1, column=1)
