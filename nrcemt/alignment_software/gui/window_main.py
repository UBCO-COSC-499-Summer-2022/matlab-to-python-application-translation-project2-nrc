import tkinter as tk
from .frame_tool import ToolFrame
from .frame_image import ImageFrame


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
