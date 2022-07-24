import tkinter as tk
from .frame_optimization_settings import OptimizationSettingsFrame
from .frame_operations import OperationsFrame


class OptimizationWindow(tk.Toplevel):

    def __init__(self, master):
        super().__init__(master)
        self.title("Optimization Window")
        self.resizable(False, False)

        self.optimization_settings = OptimizationSettingsFrame(
            self, text="Optimization Settings"
        )
        self.optimization_settings.grid(row=0, column=0, sticky="nwse")
        self.operations = OperationsFrame(
            self, text="Operations"
        )
        self.operations.grid(row=1, column=0, sticky="nwse")
