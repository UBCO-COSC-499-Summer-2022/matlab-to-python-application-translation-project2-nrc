import tkinter as tk
from .frame_particle_adjustment import ParticleAdjustmentFrame
from .frame_position_graph import PositionGraphFrame


class ManualTrackWindow(tk.Toplevel):

    def __init__(self, master, particle_count):
        super().__init__(master)
        self.geometry("600x600")
        self.minsize(600, 600)
        self.title("Manual Detection Window")
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        # Adding widgets to window
        self.particle_adjustment = ParticleAdjustmentFrame(
            self, particle_count
        )
        self.particle_adjustment.grid(row=0, column=0, sticky="nwse")
        self.y_position = PositionGraphFrame(self, "y position")
        self.y_position.render_positions([1, 2, 3, 0, 3, 2, 5])
        self.y_position.update()
        self.y_position.grid(row=1, column=0, sticky="nwse")
        self.x_position = PositionGraphFrame(self, "x position")
        self.x_position.render_positions([4, 9, 3, 4, 6, 2, 5])
        self.x_position.update()
        self.x_position.grid(row=2, column=0, sticky="nwse")
