import tkinter as tk
from .frames.tool_frame import ToolFrame
from .frames.image_frame import ImageFrame


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Alignment Main Window")

        # Adding widgets to the window
        self.tools = ToolFrame(self)
        self.tools.pack(side="left", anchor="w", fill="y", expand=True)
        self.images = ImageFrame(self)
        self.images.pack(side="left")
