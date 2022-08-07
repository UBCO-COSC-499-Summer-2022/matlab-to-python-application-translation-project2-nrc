import tkinter as tk
from .frame_particle_adjustment import ParticleAdjustmentFrame
from .frame_position_graph import PositionGraphFrame


class ManualTrackWindow(tk.Toplevel):

    def __init__(
        self, master, particle_count,
        select_command=None, interpolate_command=None, move_command=None,
        delete_command=None, reset_command=None
    ):
        super().__init__(master)
        self.geometry("500x600")
        self.minsize(500, 600)
        self.title("Manual Detection Window")
        self.wm_group(master)

        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        # Adding widgets to window
        self.adjustment = ParticleAdjustmentFrame(
            self, particle_count,
            select_command, interpolate_command, move_command,
            delete_command, reset_command
        )
        self.adjustment.grid(row=0, column=0, sticky="nwse")
        self.y_position = PositionGraphFrame(self, "y position")
        self.y_position.grid(row=1, column=0, sticky="nwse")
        self.x_position = PositionGraphFrame(self, "x position")
        self.x_position.grid(row=2, column=0, sticky="nwse")
