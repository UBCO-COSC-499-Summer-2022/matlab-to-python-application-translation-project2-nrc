import tkinter as tk
from tkinter import ttk
from .frame_contrast_tool import ContrastToolFrame
from .frame_histogram import HistogramFrame


class ContrastWindow(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.title("Contrast Adjustment Window")
        self.geometry("360x360")
        self.minsize(480, 360)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.tools = ContrastToolFrame(self)
        self.tools.grid(row=0, column=0, sticky="w")
        self.histogram = HistogramFrame(self)
        self.histogram.grid(row=1, column=0, sticky="nswe")
        self.progress_var = tk.DoubleVar(value=0.0)
        progress = ttk.Progressbar(
            self, orient="horizontal", variable=self.progress_var, max=1.0
        )
        progress.grid(row=2, column=0, sticky="we")
