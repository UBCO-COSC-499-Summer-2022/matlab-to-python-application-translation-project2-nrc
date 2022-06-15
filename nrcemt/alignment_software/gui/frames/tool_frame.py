from tkinter import ttk
from .image_adjustment_frame import ImageAdjustmentFrame
from .sequence_selector import SequenceSelector


BUTTON_WIDTH = 20


class ToolFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)

        frame = ttk.Frame(self)
        frame.pack(side="top")

        # Adding labels to each step
        for i in range(7):
            ttk.Label(
                frame,
                text="({0})".format(i+1)
            ).grid(
                column=0,
                row=i
            )

        # Step 1, Button to select directory
        file_discovery = ttk.Button(
            frame,
            text="Open First Image in Set",
            width=BUTTON_WIDTH
        )
        file_discovery.grid(column=1, row=0)

        # Step 2, Button to open Contrast Adjustment Window
        contrast_adjustment = ttk.Button(
            frame,
            text="Contrast Adjustment",
            width=BUTTON_WIDTH
        )
        contrast_adjustment.grid(column=1, row=1)

        # Step 3, Frame to adjust image properties
        image_properties = ImageAdjustmentFrame(frame)
        image_properties.grid(column=1, row=2)

        # Step 4, Buttom to open Coarse Alignment Window
        coarse_alignment = ttk.Button(
            frame,
            text="Coarse Alignment",
            width=BUTTON_WIDTH
        )
        coarse_alignment.grid(column=1, row=3)

        # Step 5, Buttom to open Auto Detection Window
        auto_detection = ttk.Button(
            frame,
            text="Auto Detection",
            width=BUTTON_WIDTH
        )
        auto_detection.grid(column=1, row=4)

        # Step 6, Buttom to open Manual Detection Window
        auto_detection = ttk.Button(
            frame,
            text="Manual Detection",
            width=BUTTON_WIDTH
        )
        auto_detection.grid(column=1, row=5)

        # Step 7, Buttom to open Optimization Window
        auto_detection = ttk.Button(
            frame,
            text="Optimization",
            width=BUTTON_WIDTH
        )
        auto_detection.grid(column=1, row=6)

        sequence_selector = SequenceSelector(self, "Image Displayed")
        sequence_selector.set_length(30)
        sequence_selector.pack(side="bottom", anchor="s", fill="x", expand=True)
