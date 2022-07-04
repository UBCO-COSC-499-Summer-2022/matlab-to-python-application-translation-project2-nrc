import tkinter as tk
from tkinter import ttk
from .manual_detection.window_manual_detection import ManualDetectionWindow
from .auto_track.window_auto_track \
    import AutoTrackWindow
from .optimization.window_optimization import OptimizationWindow

BUTTON_WIDTH = 20
STEP_PADDING = 5


class StepsFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        # Adding labels to each step
        for i in range(7):
            label = ttk.Label(self, text=f"({i+1})")
            self.rowconfigure(0, weight=1)
            label.grid(column=0, row=i, pady=STEP_PADDING)

        # Step 1, Button to select directory
        self.load_button = ttk.Button(
            self,
            text="Open First Image in Set",
            width=BUTTON_WIDTH
        )
        self.load_button.grid(column=1, row=0, pady=STEP_PADDING)

        # Step 2, Button to open Contrast Adjustment Window
        self.contrast_button = ttk.Button(
            self,
            text="Contrast Adjustment",
            width=BUTTON_WIDTH
        )
        self.contrast_button.grid(column=1, row=1, pady=STEP_PADDING)

        # Step 3, Button to open Transform Image Window
        self.transform_button = ttk.Button(
            self,
            text="Transform Image",
            width=BUTTON_WIDTH
        )
        self.transform_button.grid(column=1, row=2, pady=STEP_PADDING)

        # Step 4, Buttom to open Coarse Alignment Window
        self.coarse_align_button = ttk.Button(
            self,
            text="Coarse Alignment",
            width=BUTTON_WIDTH
        )
        self.coarse_align_button.grid(column=1, row=3, pady=STEP_PADDING)

        # Step 5, Buttom to open Auto Detection Window
        auto_detection = ttk.Button(
            self,
            text="Auto Detection",
            width=BUTTON_WIDTH,
            command=self.auto_detection_window
        )
        auto_detection.grid(column=1, row=4, pady=STEP_PADDING)

        # Step 6, Buttom to open Manual Detection Window
        auto_detection = ttk.Button(
            self,
            text="Manual Detection",
            width=BUTTON_WIDTH,
            command=self.manual_detection_window
        )
        auto_detection.grid(column=1, row=5, pady=STEP_PADDING)

        # Step 7, Buttom to open Optimization Window
        auto_detection = ttk.Button(
            self,
            text="Optimization",
            width=BUTTON_WIDTH,
            command=self.optimization_window
        )
        auto_detection.grid(column=1, row=6, pady=STEP_PADDING)

    def auto_detection_window(self):
        AutoTrackWindow(self)

    def manual_detection_window(self):
        ManualDetectionWindow(self)

    def optimization_window(self):
        OptimizationWindow(self)
