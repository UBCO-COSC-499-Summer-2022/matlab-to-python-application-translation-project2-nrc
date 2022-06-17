import tkinter as tk
from tkinter import ttk

INPUT_WIDTH = 10
PADDING = 5


class ContrastToolFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=2)
        self.rowconfigure(0, weight=1)

        # Frame for Data Range
        data_range = tk.LabelFrame(self, bd=1, text="Data Range")
        data_range.grid(row=0, column=0, sticky="nwse")
        self.fill_data_range(data_range)

        # Frame for Window
        window = tk.LabelFrame(self, bd=1, text="Window")
        window.grid(row=0, column=1, sticky="nwse")
        self.fill_window(window)

        # Frame for Scale Display Range
        scale_display = tk.LabelFrame(self, bd=1, text="Scale Display")
        scale_display.grid(row=0, column=2, sticky="nwse")
        self.fill_scale_display(scale_display)

    def fill_data_range(self, frame):
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        inner_frame = tk.Frame(frame)
        inner_frame.columnconfigure(0, weight=1)
        inner_frame.columnconfigure(1, weight=1)
        inner_frame.rowconfigure(0, weight=1)
        inner_frame.rowconfigure(1, weight=1)
        inner_frame.grid(row=0, column=0, sticky="nwe")

        # Minimum data
        min_label = ttk.Label(inner_frame, text="Minimum:")
        min_label.grid(row=0, column=0, pady=PADDING)
        min_range = tk.Frame(inner_frame)
        self.min_range_val = ttk.Label(min_range, text="0")
        self.min_range_val.pack()
        min_range.grid(row=0, column=1, pady=PADDING)

        # Max Data
        max_label = ttk.Label(inner_frame, text="Maximum:")
        max_label.grid(row=1, column=0, pady=PADDING)
        max_range = tk.Frame(inner_frame)
        self.max_range_val = ttk.Label(max_range, text="1")
        self.max_range_val.pack()
        max_range.grid(row=1, column=1, pady=PADDING)

    def fill_window(self, frame):
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        inner_frame = tk.Frame(frame)
        inner_frame.columnconfigure(0, weight=1)
        inner_frame.columnconfigure(1, weight=1)
        inner_frame.columnconfigure(2, weight=1)
        inner_frame.columnconfigure(3, weight=1)
        inner_frame.rowconfigure(0, weight=1)
        inner_frame.rowconfigure(1, weight=1)
        inner_frame.grid(row=0, column=0, sticky="nwe")

        # Minimum
        min_label = ttk.Label(inner_frame, text="Minimum:")
        min_label.grid(row=0, column=0, pady=PADDING)
        min_val = tk.Entry(inner_frame, width=INPUT_WIDTH)
        min_val.grid(row=0, column=1, pady=PADDING)

        # Max
        max_label = ttk.Label(inner_frame, text="Maximum:")
        max_label.grid(row=1, column=0, pady=PADDING)
        max_val = tk.Entry(inner_frame, width=INPUT_WIDTH)
        max_val.grid(row=1, column=1, pady=PADDING)

        # Width
        width_label = ttk.Label(inner_frame, text="Width:")
        width_label.grid(row=0, column=2, pady=PADDING)
        width_val = tk.Entry(inner_frame, width=INPUT_WIDTH)
        width_val.grid(row=0, column=3, pady=PADDING)

        # Center
        center_label = ttk.Label(inner_frame, text="Center:")
        center_label.grid(row=1, column=2, pady=PADDING)
        center_val = tk.Entry(inner_frame, width=INPUT_WIDTH)
        center_val.grid(row=1, column=3, pady=PADDING)

    def fill_scale_display(self, frame):
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        inner_frame = tk.Frame(frame)
        inner_frame.columnconfigure(0, weight=1)
        inner_frame.columnconfigure(1, weight=1)
        inner_frame.rowconfigure(0, weight=1)
        inner_frame.rowconfigure(1, weight=1)
        inner_frame.rowconfigure(2, weight=1)
        inner_frame.grid(column=0, row=0, sticky="nwe")

        # Match Data Range
        match_data = ttk.Radiobutton(
            inner_frame, text="Match Data Range"
        )
        match_data.grid(row=0, column=0, pady=PADDING)

        # Eliminate outliers
        eliminate_outliers = ttk.Radiobutton(
            inner_frame, text="Match Data Range"
        )
        eliminate_outliers.grid(row=1, column=0, pady=PADDING)
        outlier_percentage = ttk.Entry(inner_frame, width=INPUT_WIDTH)
        outlier_percentage.grid(row=1, column=1, pady=PADDING)

        # Apply
        apply = ttk.Button(inner_frame, text="Apply")
        apply.grid(row=2, column=0, pady=PADDING)
