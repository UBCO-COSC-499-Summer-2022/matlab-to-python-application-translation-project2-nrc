import tkinter as tk
from tkinter import ttk
from .frame_settings import OptimizationSettingsFrame
from .frame_operations import OperationsFrame


class OptimizationWindow(tk.Toplevel):
    """The main tomography optimization window."""

    def __init__(self, master):
        """Create the window."""
        super().__init__(master)
        self.title("Optimization Window")
        self.resizable(False, False)

        self.settings = OptimizationSettingsFrame(self)
        self.settings.grid(row=0, column=0, sticky="nwse")

        self.operations = OperationsFrame(self, text="Operations")
        self.operations.grid(row=1, column=0, sticky="nwse")

        self.optimize_button = ttk.Button(self, text="Optimize")
        self.optimize_button.grid(row=2, column=0, sticky="nwse")
