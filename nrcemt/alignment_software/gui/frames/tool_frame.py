from tkinter import ttk
from .image_adjustment_frame import ImageAdjustmentFrame


class ToolFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        # Setting up grid
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=19)

        # Adding labels to each step
        for i in range(7):
            ttk.Label(
                self,
                text="({0})".format(i+1)
            ).grid(
                column=0,
                row=i
            )

        # Step 1, Button to select directory
        file_discovery = ttk.Button(
            self,
            text="Open First Image in Set",
            width=20
        )
        file_discovery.grid(column=1, row=0)

        # Step 2, Button to open Contrast Adjustment Window
        contrast_adjustment = ttk.Button(
            self,
            text="Contrast Adjustment",
            width=20
        )
        contrast_adjustment.grid(column=1, row=1)

        # Step 3, Frame to adjust image properties
        image_properties = ImageAdjustmentFrame(self)
        image_properties.grid(column=1, row=2)

        # Step 4, Buttom to open Coarse Alignment Window
        coarse_alignment = ttk.Button(
            self,
            text="Coarse Alignment",
            width=20
        )
        coarse_alignment.grid(column=1, row=3)

        # Step 5, Buttom to open Auto Detection Window
        auto_detection = ttk.Button(
            self,
            text="Auto Detection",
            width=20
        )
        auto_detection.grid(column=1, row=4)

        # Step 6, Buttom to open Manual Detection Window
        auto_detection = ttk.Button(
            self,
            text="Manual Detection",
            width=20
        )
        auto_detection.grid(column=1, row=5)

        # Step 7, Buttom to open Optimization Window
        auto_detection = ttk.Button(
            self,
            text="Optimization",
            width=20
        )
        auto_detection.grid(column=1, row=6)
