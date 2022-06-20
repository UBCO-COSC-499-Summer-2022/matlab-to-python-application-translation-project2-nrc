import tkinter as tk
from tkinter import ttk
from .frame_image_adjustment import ImageAdjustmentFrame
from .contrast_adjustment.window_contrast_adjustment \
    import ContrastAdjustmentWindow

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
        self.file_discovery = ttk.Button(
            self,
            text="Open First Image in Set",
            width=BUTTON_WIDTH
        )
        self.rowconfigure(0, weight=1)
        self.file_discovery.grid(column=1, row=0, pady=STEP_PADDING)

        # Step 2, Button to open Contrast Adjustment Window
        contrast_adjustment = ttk.Button(
            self,
            text="Contrast Adjustment",
            width=BUTTON_WIDTH,
            command=self.contrast_adjustment_window
        )
        self.rowconfigure(1, weight=1)
        contrast_adjustment.grid(column=1, row=1, pady=STEP_PADDING)

        # Step 3, Frame to adjust image properties
        image_properties = ImageAdjustmentFrame(self)
        self.rowconfigure(2, weight=5)
        image_properties.grid(column=1, row=2, pady=STEP_PADDING)

        # Step 4, Buttom to open Coarse Alignment Window
        coarse_alignment = ttk.Button(
            self,
            text="Coarse Alignment",
            width=BUTTON_WIDTH
        )
        self.rowconfigure(3, weight=1)
        coarse_alignment.grid(column=1, row=3, pady=STEP_PADDING)

        # Step 5, Buttom to open Auto Detection Window
        auto_detection = ttk.Button(
            self,
            text="Auto Detection",
            width=BUTTON_WIDTH
        )
        self.rowconfigure(4, weight=1)
        auto_detection.grid(column=1, row=4, pady=STEP_PADDING)

        # Step 6, Buttom to open Manual Detection Window
        auto_detection = ttk.Button(
            self,
            text="Manual Detection",
            width=BUTTON_WIDTH
        )
        self.rowconfigure(5, weight=1)
        auto_detection.grid(column=1, row=5, pady=STEP_PADDING)

        # Step 7, Buttom to open Optimization Window
        auto_detection = ttk.Button(
            self,
            text="Optimization",
            width=BUTTON_WIDTH
        )
        self.rowconfigure(6, weight=1)
        auto_detection.grid(column=1, row=6, pady=STEP_PADDING)

    def contrast_adjustment_window(self):
        ca_window = ContrastAdjustmentWindow()
        ca_window.mainloop()
