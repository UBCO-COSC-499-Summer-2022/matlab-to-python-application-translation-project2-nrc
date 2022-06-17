import tkinter as tk
from tkinter import ttk


class ToolFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.columnconfigure(2, weight=2)
        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=1)

        # Frame for Data Range
        data_range = tk.Frame(self, bd=1, relief="ridge")
        data_range.grid(row=0, column=0, sticky="nwse")
        self.fill_data_range(data_range)

        # Frame for Window
        window = tk.Frame(self, bd=1, relief="ridge")
        window.grid(row=0, column=1, sticky="nwse")
        self.fill_window(window)

        # Frame for Scale Display Range
        scale_display = tk.Frame(self, bd=1, relief="ridge")
        scale_display.grid(row=0, column=2, rowspan=2, sticky="nwse")
        self.fill_scale_display(scale_display)

    def fill_data_range(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # Minimum data
        min_label = ttk.Label(frame, text="Minimum:")
        min_label.grid(row=0, column=0)
        min_range = tk.Frame(frame)
        self.min_range_val = ttk.Label(min_range, text="0")
        self.min_range_val.pack()
        min_range.grid(row=0, column=1)

        # Max Data
        max_label = ttk.Label(frame, text="Maximum:")
        max_label.grid(row=1, column=0)
        max_range = tk.Frame(frame)
        self.max_range_val = ttk.Label(max_range, text="1")
        self.max_range_val.pack()
        max_range.grid(row=1, column=1)

    def fill_window(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        frame.columnconfigure(3, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        # Minimum
        min_label = ttk.Label(frame, text="Minimum:")
        min_label.grid(row=0, column=0)
        min_val = tk.Entry(frame)
        min_val.grid(row=0, column=1)

        # Max
        max_label = ttk.Label(frame, text="Maximum:")
        max_label.grid(row=1, column=0)
        max_val = tk.Entry(frame)
        max_val.grid(row=1, column=1)

        # Width
        width_label = ttk.Label(frame, text="Width:")
        width_label.grid(row=0, column=2)
        width_val = tk.Entry(frame)
        width_val.grid(row=0, column=3)

        # Center
        center_label = ttk.Label(frame, text="Center:")
        center_label.grid(row=1, column=2)
        center_val = tk.Entry(frame)
        center_val.grid(row=1, column=3)

    def fill_scale_display(self, frame):
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)

        # Match Data Range
        match_data = ttk.Radiobutton(
            frame, text="Match Data Range"
        )
        match_data.grid(row=0, column=0)

        # Eliminate outliers
        eliminate_outliers = ttk.Radiobutton(
            frame, text="Match Data Range"
        )
        eliminate_outliers.grid(row=1, column=0)
        outlier_percentage = ttk.Entry(frame)
        outlier_percentage.grid(row=1, column=1)

        # Apply
        apply = ttk.Button(frame, text="Apply")
        apply.grid(row=2, column=0)
