import tkinter as tk
from .frame_steps import StepsFrame
from .frame_image import ImageFrame


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Alignment Main Window")
        self.minsize(600, 450)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Adding widgets to the window
        self.tools = StepsFrame(self)
        self.tools.grid(column=0, row=0, sticky="wns")
        self.images = ImageFrame(self)
        self.images.grid(column=1, row=0)
