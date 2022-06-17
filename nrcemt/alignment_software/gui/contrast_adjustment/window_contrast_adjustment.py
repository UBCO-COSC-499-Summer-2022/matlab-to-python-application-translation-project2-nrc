import tkinter as tk
from .frame_contrast_tool import ContrastToolFrame
from .frame_histogram import HistogramFrame


class ContrastAdjustmentWindow(tk.Toplevel):

    def __init__(self):
        super().__init__()
        self.geometry("1200x300")
        self.title("Contrast Adjustment Window")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=2)
        self.minsize(700, 450)

        # Adding widgets to the window
        self.data_range = ContrastToolFrame(self)
        self.data_range.grid(row=0, column=0, sticky="nwse")
        self.histogram = HistogramFrame(self)
        self.histogram.grid(row=1, column=0, sticky="nwse")
