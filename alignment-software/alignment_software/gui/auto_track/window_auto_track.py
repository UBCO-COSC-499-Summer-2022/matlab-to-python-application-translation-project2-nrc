import tkinter as tk
from tkinter import ttk
from .frame_particle_table import ParticleTableFrame
from .frame_particle_properties import ParticlePropertiesFrame


class AutoTrackWindow(tk.Toplevel):
    """Create the automatic tracking window witth a table and controls."""

    def __init__(self, master, particle_count):
        """Create the window."""
        super().__init__(master)
        self.title("Automatic Detection Window")

        # Adding widgets to the window
        self.table = ParticleTableFrame(self, particle_count)
        self.table.grid(column=0, row=0, sticky="we")

        self.track_button = ttk.Button(self, text="Track all selected")
        self.track_button.grid(column=0, row=1, sticky="we")
        self.interpolate_button = ttk.Button(self, text="Interpolate selected")
        self.interpolate_button.grid(column=0, row=2, sticky="we")

        self.properties = ParticlePropertiesFrame(self)
        self.properties.grid(column=0, row=3, sticky="we")

        self.reset_button = ttk.Button(self, text="Reset all particles")
        self.reset_button.grid(column=0, row=4, sticky="we")
