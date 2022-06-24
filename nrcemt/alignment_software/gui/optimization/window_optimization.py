import tkinter as tk
from .frame_optimization_settings import OptimizationSettingsFrame
from .frame_image_set import ImageSetFrame
from .frame_operations import OperationsFrame
from .frame_selected_area import SelectedAreaFrame


class OptimizationWindow(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
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
        self.selected_areas = SelectedAreaFrame(
            self, text="Selected Area"
        )
        self.selected_areas.grid(row=3, column=0, sticky="nwse")
