import tkinter as tk
from nrcemt.alignment_software.gui.frames.tool_frame import ToolFrame
from nrcemt.alignment_software.gui.frames.image_frame import ImageFrame


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.resizable(0, 0)

        # Setting up grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=4)

        # Adding widgets to the window
        self.tools = ToolFrame(self)
        self.tools.grid(column=0, row=0)
        self.images = ImageFrame(self)
        self.images.grid(column=1, row=0)
