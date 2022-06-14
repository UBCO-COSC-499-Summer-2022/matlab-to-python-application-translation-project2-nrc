import tkinter as tk
from tkinter import ttk


class ImageAdjustmentFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.__create_widgets()

    def __create_widgets(self):
        ttk.Style().configure(
            "F1.TFrame",
            background="#bebebe",
            borderwidth=5
        )
        self.frame = ttk.Frame(
            self,
            style="F1.TFrame"
        )
        self.frame.config()
        self.__create_subwidget_input(
            self.frame,
            "Offset X (pixel)",
            0
        )
        self.__create_subwidget_input(
            self.frame,
            "Offset Y (pixel)",
            1
        )
        self.__create_subwidget_input(
            self.frame,
            "Angle (degree)",
            2
        )
        self.__create_subwidget_slider(
            self.frame,
            "Binning",
            3
        )
        self.__create_subwidget_checkbox(
            self.frame,
            "Use Sobel",
            4
        )
        self.frame.grid(column=0, row=0)

    def __create_subwidget_input(self, master, text, i):
        label = ttk.Label(master, text=text)
        label.grid(column=0, row=i)
        input = ttk.Entry(master)
        input.grid(column=1, row=i)

    def __create_subwidget_slider(self, master, text, i):
        label = ttk.Label(master, text=text)
        label.grid(column=0, row=i)
        """
        Couldn't find how to use tickinterval in ttk
        """
        scale = tk.Scale(
            master,
            from_=1,
            to=4,
            tickinterval=1,
            orient=tk.HORIZONTAL
        )
        scale.grid(column=1, row=i)

    def __create_subwidget_checkbox(self, master, text, i):
        cb = ttk.Checkbutton(master, text=text)
        cb.grid(column=0, row=i)
