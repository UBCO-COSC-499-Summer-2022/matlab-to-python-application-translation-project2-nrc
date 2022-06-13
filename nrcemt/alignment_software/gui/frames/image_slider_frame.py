import tkinter as tk
from tkinter import ttk


class ImageSliderFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.__create_widgets()

    def __create_widgets(self):
        self.label = ttk.Label(self, text="Image Displayed")
        self.label.grid(column=0, row=0)
        self.scale = tk.Scale(
            self,
            from_=1,
            to=61,
            tickinterval=1,
            orient=tk.HORIZONTAL
        )
        self.scale.grid(column=0, row=1, columnspan=2)

    def open_window(self):
        pass
