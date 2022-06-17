import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from .frame_image_adjustment import ImageAdjustmentFrame
from .frame_sequence_selector import SequenceSelector
from .contrast_adjustment.window_contrast_adjustment \
    import ContrastAdjustmentWindow

BUTTON_WIDTH = 20


class StepsFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # Adding labels to each step
        for i in range(7):
            label = ttk.Label(self, text=f"({i+1})")
            label.grid(column=0, row=i)

        # Step 1, Button to select directory
        file_discovery = ttk.Button(
            self,
            text="Open First Image in Set",
            width=BUTTON_WIDTH,
            command=self.open_home_base
        )
        self.rowconfigure(0, weight=1)
        file_discovery.grid(column=1, row=0)

        # Step 2, Button to open Contrast Adjustment Window
        contrast_adjustment = ttk.Button(
            self,
            text="Contrast Adjustment",
            width=BUTTON_WIDTH,
            command=self.contrast_adjustment_window
        )
        self.rowconfigure(1, weight=1)
        contrast_adjustment.grid(column=1, row=1)

        # Step 3, Frame to adjust image properties
        image_properties = ImageAdjustmentFrame(self)
        self.rowconfigure(2, weight=5)
        image_properties.grid(column=1, row=2)

        # Step 4, Buttom to open Coarse Alignment Window
        coarse_alignment = ttk.Button(
            self,
            text="Coarse Alignment",
            width=BUTTON_WIDTH,
            command=self.dummy_function
        )
        self.rowconfigure(3, weight=1)
        coarse_alignment.grid(column=1, row=3)

        # Step 5, Buttom to open Auto Detection Window
        auto_detection = ttk.Button(
            self,
            text="Auto Detection",
            width=BUTTON_WIDTH,
            command=self.dummy_function
        )
        self.rowconfigure(4, weight=1)
        auto_detection.grid(column=1, row=4)

        # Step 6, Buttom to open Manual Detection Window
        auto_detection = ttk.Button(
            self,
            text="Manual Detection",
            width=BUTTON_WIDTH,
            command=self.dummy_function
        )
        self.rowconfigure(5, weight=1)
        auto_detection.grid(column=1, row=5)

        # Step 7, Buttom to open Optimization Window
        auto_detection = ttk.Button(
            self,
            text="Optimization",
            width=BUTTON_WIDTH,
            command=self.dummy_function
        )
        self.rowconfigure(6, weight=1)
        auto_detection.grid(column=1, row=6)

        sequence_selector = SequenceSelector(self, "Image Displayed")
        sequence_selector.set_length(30)
        self.rowconfigure(7, weight=1)
        sequence_selector.grid(column=1, row=7)

    def open_home_base(self):
        filedialog.askopenfilename()

    def contrast_adjustment_window(self):
        ca_window = ContrastAdjustmentWindow()
        ca_window.mainloop()

    def dummy_function():
        pass
