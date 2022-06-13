import tkinter as tk
from .widget_config import UpperWidgets


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        # Upper Settings
        upper_menu = UpperWidgets(self)
        upper_menu.pack(side="top", anchor="nw")
