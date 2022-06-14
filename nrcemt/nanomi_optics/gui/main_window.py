import tkinter as tk
from .above_sample import AboveSampleConfiguration


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        # Upper Settings
        upper_menu = AboveSampleConfiguration(self)
        upper_menu.pack(side="top", anchor="nw", padx=20, pady=20)
