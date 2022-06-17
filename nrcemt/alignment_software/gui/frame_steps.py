import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from .frame_image_adjustment import ImageAdjustmentFrame
from .frame_sequence_selector import SequenceSelector
from .contrast_adjustment.window_contrast_adjustment \
    import ContrastAdjustmentWindow

BUTTON_WIDTH = 20
STEP_PADDING = 5


class StepsFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        frame = tk.Frame(self)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.grid(row=0, column=0, rowspan=7, columnspan=2, sticky="nwe")

        # Adding labels to each step
        for i in range(7):
            label = ttk.Label(frame, text=f"({i+1})")
            frame.rowconfigure(0, weight=1)
            label.grid(column=0, row=i, pady=STEP_PADDING)

        # Step 1, Button to select directory
        file_discovery = ttk.Button(
            frame,
            text="Open First Image in Set",
            width=BUTTON_WIDTH,
            command=self.open_home_base
        )
        frame.rowconfigure(0, weight=1)
        file_discovery.grid(column=1, row=0, pady=STEP_PADDING)

        # Step 2, Button to open Contrast Adjustment Window
        contrast_adjustment = ttk.Button(
            frame,
            text="Contrast Adjustment",
            width=BUTTON_WIDTH,
            command=self.contrast_adjustment_window
        )
        frame.rowconfigure(1, weight=1)
        contrast_adjustment.grid(column=1, row=1, pady=STEP_PADDING)

        # Step 3, Frame to adjust image properties
        image_properties = ImageAdjustmentFrame(frame)
        frame.rowconfigure(2, weight=5)
        image_properties.grid(column=1, row=2, pady=STEP_PADDING)

        # Step 4, Buttom to open Coarse Alignment Window
        coarse_alignment = ttk.Button(
            frame,
            text="Coarse Alignment",
            width=BUTTON_WIDTH,
            command=self.dummy_function
        )
        frame.rowconfigure(3, weight=1)
        coarse_alignment.grid(column=1, row=3, pady=STEP_PADDING)

        # Step 5, Buttom to open Auto Detection Window
        auto_detection = ttk.Button(
            frame,
            text="Auto Detection",
            width=BUTTON_WIDTH,
            command=self.dummy_function
        )
        frame.rowconfigure(4, weight=1)
        auto_detection.grid(column=1, row=4, pady=STEP_PADDING)

        # Step 6, Buttom to open Manual Detection Window
        auto_detection = ttk.Button(
            frame,
            text="Manual Detection",
            width=BUTTON_WIDTH,
            command=self.dummy_function
        )
        frame.rowconfigure(5, weight=1)
        auto_detection.grid(column=1, row=5, pady=STEP_PADDING)

        # Step 7, Buttom to open Optimization Window
        auto_detection = ttk.Button(
            frame,
            text="Optimization",
            width=BUTTON_WIDTH,
            command=self.dummy_function
        )
        frame.rowconfigure(6, weight=1)
        auto_detection.grid(column=1, row=6, pady=STEP_PADDING)

        sequence_selector = SequenceSelector(self, "Image Displayed")
        sequence_selector.set_length(30)
        self.rowconfigure(7, weight=1)
        sequence_selector.grid(column=1, row=7, sticky="wse")

    def open_home_base(self):
        filedialog.askopenfilename()

    def contrast_adjustment_window(self):
        ca_window = ContrastAdjustmentWindow()
        ca_window.mainloop()

    def dummy_function():
        pass
