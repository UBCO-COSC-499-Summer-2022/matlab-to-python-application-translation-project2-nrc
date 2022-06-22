import tkinter as tk
from tkinter import ttk
from .frame_above_sample import AboveSampleFrame
from .frame_below_sample import BelowSampleFrame
from .frame_results import ResultsFrame
from .frame_diagram import DiagramFrame


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        # Frame that holds the settings
        settings_frame = ttk.Frame(self)
        settings_frame.pack(side="left", anchor="nw")

        # Upper Settings
        upper_menu = AboveSampleFrame(settings_frame)
        upper_menu.pack(side="top", anchor="nw", padx=20, pady=20, fill="x",
                        expand=True)

        # Lower Settings
        lower_menu = BelowSampleFrame(settings_frame)
        lower_menu.pack(side="top", anchor="nw", padx=20, fill="x",
                        expand=True)

        # Frame that holds the results, diagram, diagram controls
        results_frame = ttk.Frame(self)
        results_frame.pack(side="top", anchor="nw")

        # Results Window
        numerical_results = ResultsFrame(results_frame)
        numerical_results.pack(
            side="top", anchor="nw",
            padx=20, pady=20,
            fill="x", expand=True
            )

        # Diagram
        diagram = DiagramFrame(results_frame)
        diagram.pack(
            side="top", anchor="nw",
            padx=20, pady=20,
            fill="x", expand=True
            )
