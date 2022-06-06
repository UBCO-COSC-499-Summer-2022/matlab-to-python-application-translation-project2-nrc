import time
import tkinter as tk
from nrcemt.common.gui import AsyncHandler
from .sequence_selector import SequenceSelector


class MainWindow(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.image_selector = SequenceSelector(
            self,
            "Image displayed",
            command=AsyncHandler(self.handle_scale)
        )
        self.image_selector.set_length(61)
        self.label = tk.Label(self)
        self.label.pack()
        self.image_selector.pack()

    def handle_scale(self, scale):
        time.sleep(0.5)
        print(scale)
        self.label.config(text=str(scale))
