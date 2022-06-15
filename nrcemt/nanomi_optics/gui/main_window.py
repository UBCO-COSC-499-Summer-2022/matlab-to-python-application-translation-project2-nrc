import tkinter as tk
from tkinter import ttk
from .above_sample import AboveSampleConfiguration
from .below_sample import BelowSampleConfiguration


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        # Frame that holds the settings
        settings_frame = ttk.Frame(self)
        settings_frame.pack(side="top", anchor="nw")

        # Upper Settings
        upper_menu = AboveSampleConfiguration(settings_frame)
        upper_menu.pack(side="top", anchor="nw", padx=20, pady=20, fill="x",
                        expand=True)

        # Lower Settings
        lower_menu = BelowSampleConfiguration(settings_frame)
        lower_menu.pack(side="top", anchor="nw", padx=20)
