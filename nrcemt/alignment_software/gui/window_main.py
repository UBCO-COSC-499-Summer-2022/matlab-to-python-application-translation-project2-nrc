import tkinter as tk
from .frame_steps import StepsFrame
from .frame_image import ImageFrame
from .frame_sequence_selector import SequenceSelector

class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Alignment Main Window")
        self.minsize(600, 450)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        side_frame = tk.Frame()
        side_frame.grid(column=0, row=0, sticky="nswe")
        self.steps = StepsFrame(side_frame)
        self.steps.pack(side="top")
        self.image_select = SequenceSelector(side_frame, "Image displayed")
        self.image_select.pack(side="bottom", fill="x")

        self.image = ImageFrame(self)
        self.image.grid(column=1, row=0)
