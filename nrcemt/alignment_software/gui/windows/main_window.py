import tkinter as tk
from nrcemt.alignment_software.gui.frames.tool_frame import ToolFrame
from nrcemt.alignment_software.gui.frames.image_frame import ImageFrame


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("800x600")

        # Setting up grid
        # self.columnconfigure(0, weight=1)
        # self.columnconfigure(1, weight=4)

        # Adding widgets to the window
        self.tools = ToolFrame(self)
        self.tools.pack(anchor="nw")
        self.images = ImageFrame(self)
        self.images.pack(side="left")
