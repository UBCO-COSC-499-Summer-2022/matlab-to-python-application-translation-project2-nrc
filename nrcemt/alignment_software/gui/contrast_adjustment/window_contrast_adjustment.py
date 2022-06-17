import tkinter as tk
from .frame_tool import ToolFrame


class ContrastAdjustmentWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("1200x300")
        self.title("Contrast Adjustment Window")

        # Adding widgets to the window
        self.data_range = ToolFrame(self)
        self.data_range.pack(side="left", anchor="w", fill="y", expand=True)
