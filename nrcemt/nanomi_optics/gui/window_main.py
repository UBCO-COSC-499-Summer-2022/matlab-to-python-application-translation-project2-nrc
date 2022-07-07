import tkinter as tk
from tkinter import ttk
from .frame_above_sample import AboveSampleFrame
from .frame_below_sample import BelowSampleFrame
from .frame_results import ResultsFrame
from .frame_diagram import DiagramFrame

PAD_X = 20
PAD_Y = 20


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        # set title of window
        self.title('Nanomi Optics')
        # set window size
        self.geometry('1200x800')

        # Frame that holds the settings
        settings_frame = tk.Frame(self)
        settings_frame.pack(side="left", anchor="nw")

        # Upper Settings
        upper_menu = AboveSampleFrame(settings_frame)
        upper_menu.pack(
            side="top", anchor="nw",
            padx=PAD_X, pady=PAD_Y,
            fill="x", expand=True
        )

        # Lower Settings
        lower_menu = BelowSampleFrame(settings_frame)
        lower_menu.pack(
            side="top", anchor="nw",
            padx=PAD_X, fill="x",
            expand=True
        )

        # Frame that holds the results, diagram, diagram controls
        results_frame = tk.Frame(self)
        results_frame.pack(side="top", anchor="nw")

        # Results Window
        numerical_results = ResultsFrame(results_frame)
        numerical_results.pack(
            side="top", anchor="nw",
            padx=PAD_X, pady=PAD_Y,
            fill="x", expand=True
            )

        # Diagram
        diagram = DiagramFrame(results_frame)
        diagram.pack(
            side="top", anchor="nw",
            padx=PAD_X, pady=PAD_Y,
            fill="x", expand=True
            )
