import tkinter as tk
from .frame_optimization_settings import OptimizationSettingsFrame
from .frame_image_set import ImageSetFrame
from .frame_operations import OperationsFrame


class OptimizationWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("350x800")
        self.minsize(350, 600)
        self.title("Optimization Window")

        self.optimization_settings = OptimizationSettingsFrame(
            self, text="Optimization Settings"
        )
        self.optimization_settings.grid(row=0, column=0, sticky="nwse")
        self.image_set = ImageSetFrame(
            self, text="Image Set"
        )
        self.image_set.grid(row=1, column=0, sticky="nwse")
        self.operations = OperationsFrame(
            self, text="Operations"
        )
        self.operations.grid(row=2, column=0, sticky="nwse")
