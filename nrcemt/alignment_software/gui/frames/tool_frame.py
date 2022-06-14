from tkinter import ttk
from tkinter import filedialog
from nrcemt.alignment_software.gui.windows.contrast_adjustment_window import ContrastAdjustmentWindow
from nrcemt.alignment_software.gui.frames.image_adjustment_frame import ImageAdjustmentFrame


class ToolFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        # Setting up grid
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=19)

        # Loop to label steps
        for i in range(7):
            ttk.Label(
                self,
                text="({0})".format(i+1)
            ).grid(
                column=0,
                row=i
            )
        # Call function to add widget in GUI, column 1
        self.__create_widgets()

    def __create_widgets(self):
        # Step 1, Button to select directory
        self.file_discovery = ttk.Button(
            self,
            text="Open First Image in Set",
            command=self.open_home_base
        )
        self.file_discovery.grid(column=1, row=0)

        # Step 2, Button to open Contrast Adjustment Window
        self.contrast_adjustment = ttk.Button(
            self,
            text="Contrast Adjustment",
            command=self.open_contrast_adjustment_window
        )
        self.contrast_adjustment.grid(column=1, row=1)

        # Step 3, Frame to adjust image properties
        self.image_properties = ImageAdjustmentFrame(self)
        self.image_properties.grid(column=1, row=2)

        # Step 4, Buttom to open Coarse Alignment Window
        self.coarse_alignment = ttk.Button(
            self,
            text="Coarse Alignment",
            command=self.open_coarse_alignment_window
        )
        self.coarse_alignment.grid(column=1, row=3)

        # Step 5, Buttom to open Auto Detection Window
        self.auto_detection = ttk.Button(
            self,
            text="Auto Detection",
            command=self.open_auto_detection_window
        )
        self.auto_detection.grid(column=1, row=4)

        # Step 6, Buttom to open Manual Detection Window
        self.auto_detection = ttk.Button(
            self,
            text="Manual Detection",
            command=self.open_manual_detection_window
        )
        self.auto_detection.grid(column=1, row=5)

        # Step 7, Buttom to open Optimization Window
        self.auto_detection = ttk.Button(
            self,
            text="Optimization",
            command=self.open_optimization_window
        )
        self.auto_detection.grid(column=1, row=6)

    def open_home_base(self):
        filedialog.askopenfilename()

    def open_contrast_adjustment_window(self):
        ca_window = ContrastAdjustmentWindow()
        ca_window.mainloop()

    def open_coarse_alignment_window(self):
        ca_window = ContrastAdjustmentWindow()
        ca_window.mainloop()

    def open_auto_detection_window(self):
        ca_window = ContrastAdjustmentWindow()
        ca_window.mainloop()

    def open_manual_detection_window(self):
        ca_window = ContrastAdjustmentWindow()
        ca_window.mainloop()

    def open_optimization_window(self):
        ca_window = ContrastAdjustmentWindow()
        ca_window.mainloop()
