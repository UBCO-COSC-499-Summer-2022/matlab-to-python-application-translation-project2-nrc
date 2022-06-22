import tkinter as tk
from .frame_particle_detection import ParticleDetectionFrame
from .frame_particle_properties import ParticlePropertiesFrame


class AutoDetectionWindow(tk.Toplevel):

    def __init__(self):
        super().__init__()
        self.geometry("500x800")
        self.title("Automatic Detection Window")
        self.minsize(500, 800)

        # Configuring the grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=3)

        # Adding widgets to the window
        self.particle_detection = ParticleDetectionFrame(
            self, "Particle Detection"
        )
        self.particle_detection.grid(
            column=0, row=0, sticky="nwse"
        )

        self.particle_properties = ParticlePropertiesFrame(self)
        self.particle_properties.grid(column=0, row=1, sticky="nwse")
