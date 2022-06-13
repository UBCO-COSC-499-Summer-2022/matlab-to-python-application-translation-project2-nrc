import tkinter as tk
from .widget_config import UpperWidgets


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        # Upper Settings
        upper_menu = UpperWidgets(self)
        upper_menu.pack(side="top", anchor="nw")

        # Lower Settings
        # lower_menu = LowerWidgets(inputs)
        # lower_menu.grid(row=1, column=0, padx=2, pady=2)

        # Display Results
