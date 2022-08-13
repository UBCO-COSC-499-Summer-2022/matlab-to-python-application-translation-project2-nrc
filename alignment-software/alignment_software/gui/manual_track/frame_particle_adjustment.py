import tkinter as tk
from tkinter import ttk

from ..common import NumericSpinbox

BUTTON_WIDTH = 3
RADIO_PADDING = 5


class ParticleAdjustmentFrame(tk.LabelFrame):
    """Frame with particle selector and directional controls."""

    def __init__(
        self, master, particle_count,
        select_command=None, interpolate_command=None, move_command=None,
        delete_command=None, reset_command=None
    ):
        """Create the frame."""
        super().__init__(master, text="Particle selection and adjustment")
        self.move_command = move_command

        selection_frame = tk.Frame(self)
        selection_frame.grid(row=0, column=0, sticky="we")
        self.selection_var = tk.IntVar(self, 0)
        if select_command is not None:
            self.selection_var.trace(
                'w', lambda a, b, c: select_command(self.selection_var.get())
            )
        self.status_vars = []
        for i in range(particle_count):
            radio = tk.Radiobutton(
                selection_frame, text=f"{i+1}",
                variable=self.selection_var, value=i
            )
            radio.grid(row=0, column=i)
            status_var = tk.StringVar(self, value="")
            status_label = ttk.Label(
                selection_frame, anchor="center", textvariable=status_var
            )
            status_label.grid(row=1, column=i, sticky="we")
            self.status_vars.append(status_var)

        control_frame = tk.Frame(self)
        control_frame.grid(row=1, column=0, sticky="we")

        self.step_entry = NumericSpinbox(control_frame, 5, (1, 100), width=5)
        self.step_entry.grid(row=1, column=1)

        # create all of the directional controls
        up_button = tk.Button(control_frame, text="▲", width=5)
        up_button.grid(row=0, column=1)
        up_button.config(command=lambda: self.move(0, -1))
        left_button = tk.Button(control_frame, text="◀", width=5)
        left_button.grid(row=1, column=0)
        left_button.config(command=lambda: self.move(-1, 0))
        down_button = tk.Button(control_frame, text="▼", width=5)
        down_button.grid(row=2, column=1)
        down_button.config(command=lambda: self.move(0, 1))
        right_button = tk.Button(control_frame, text="▶", width=5)
        right_button.grid(row=1, column=2)
        right_button.config(command=lambda: self.move(1, 0))
        up_left_button = tk.Button(control_frame, text="◤", width=5)
        up_left_button.grid(row=0, column=0)
        up_left_button.config(command=lambda: self.move(-1, -1))
        up_right_button = tk.Button(control_frame, text="◥", width=5)
        up_right_button.grid(row=0, column=2)
        up_right_button.config(command=lambda: self.move(1, -1))
        down_left_button = tk.Button(control_frame, text="◣", width=5)
        down_left_button.grid(row=2, column=0)
        down_left_button.config(command=lambda: self.move(-1, 1))
        down_right_button = tk.Button(control_frame, text="◢", width=5)
        down_right_button.grid(row=2, column=2)
        down_right_button.config(command=lambda: self.move(1, 1))

        self.interpolate_button = tk.Button(
            control_frame, text="Interpolate", width=10
        )
        self.interpolate_button.grid(row=0, column=3)
        if interpolate_command is not None:
            self.interpolate_button.config(
                command=lambda: interpolate_command(self.selection_var.get())
            )

        self.delete_button = tk.Button(
            control_frame, text="Delete", width=10
        )
        self.delete_button.grid(row=1, column=3)
        if delete_command is not None:
            self.delete_button.config(
                command=lambda: delete_command()
            )

        self.reset_button = tk.Button(
            control_frame, text="Reset", width=10
        )
        self.reset_button.grid(row=2, column=3)
        if reset_command is not None:
            self.reset_button.config(
                command=lambda: reset_command()
            )

    def update_particle_status(self, particle_positions):
        """Update particle status indicators."""
        for p in range(particle_positions.particle_count()):
            status = particle_positions.get_status(p)
            if status == "complete":
                icon = "●"
            elif status == "partial":
                icon = "◒"
            else:
                icon = "○"
            self.status_vars[p].set(icon)

    def move(self, x, y):
        """Call the move command when a directional input is pressed."""
        if self.move_command is not None:
            step = self.step_entry.get()
            self.move_command(x * step, y * step)
