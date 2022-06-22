import tkinter as tk
from .frame_particle_adjustment import ParticleAdjustmentFrame
from .frame_position import PositionFrame


class ManualDetectionWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("800x400")
        self.minsize(800, 400)
        self.title("Manual Detection Window")
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        # Adding widgets to window
        self.particle_adjustment = ParticleAdjustmentFrame(
            self, "Particle selection and ajustment"
        )
        self.particle_adjustment.grid(row=0, column=0, sticky="nwse")
        self.y_position = PositionFrame(self)
        self.y_position.grid(row=1, column=0, sticky="nwse")
        self.x_position = PositionFrame(self)
        self.x_position.grid(row=2, column=0, sticky="nwse")
