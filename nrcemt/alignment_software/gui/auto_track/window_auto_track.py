import tkinter as tk
from .frame_particle_table import ParticleTableFrame
from .frame_particle_properties import ParticlePropertiesFrame


class AutoTrackWindow(tk.Toplevel):

    def __init__(self, master, particle_count):
        super().__init__(master)
        self.title("Automatic Detection Window")

        # Adding widgets to the window
        self.particle_table = ParticleTableFrame(self, particle_count)
        self.particle_table.grid(column=0, row=0, sticky="nwse")

        self.particle_properties = ParticlePropertiesFrame(self)
        self.particle_properties.grid(column=0, row=1, sticky="nwse")

    def get_selected_particle(self):
        return self.particle_table.particle_select_var.get()
