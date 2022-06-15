import tkinter as tk
from tkinter import ttk


class ImageAdjustmentFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)

        # Create input widgets
        input_label = [
            "Offset X (pixel)",
            "Offset Y (pixel)",
            "Angle (degree)"
        ]
        for i in range(3):
            self.__create_subwidget_input(
                self,
                input_label[i],
                i
            )

        # Create slider widget
        self.__create_subwidget_slider(
            self,
            "Binning",
            3
        )

        # Create checkbox widget
        self.__create_subwidget_checkbox(
            self,
            "Use Sobel",
            4
        )

        self.grid(column=0, row=0)

    def __create_subwidget_input(self, master, text, i):
        label = ttk.Label(
            master, text=text)
        label.grid(column=0, row=i)
        input = ttk.Entry(master, width=10)
        input.grid(column=1, row=i)

    def __create_subwidget_slider(self, master, text, i):
        label = ttk.Label(master, text=text)
        label.grid(column=0, row=i)

        # Couldn't find how to use tickinterval in ttk
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
