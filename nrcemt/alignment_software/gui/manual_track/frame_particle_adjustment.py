import tkinter as tk

from nrcemt.common.gui.numericspinbox import NumericSpinbox

BUTTON_WIDTH = 3
RADIO_PADDING = 5


class ParticleAdjustmentFrame(tk.LabelFrame):

    def __init__(
        self, master, particle_count,
        select_command=None, interpolate_command=None, move_command=None,
        delete_command=None, reset_command=None
    ):
        super().__init__(master, text="Particle selection and ajustment", bd=1)
        self.move_command = move_command

        selection_frame = tk.Frame(self)
        selection_frame.grid(row=0, column=0, sticky="we")
        self.selection_var = tk.IntVar(self, 0)
        if select_command is not None:
            self.selection_var.trace(
                'w', lambda a, b, c: select_command(self.selection_var.get())
            )
        for i in range(particle_count):
            radio = tk.Radiobutton(
                selection_frame, text=f"{i+1}",
                variable=self.selection_var, value=i
            )
            radio.pack(side="left")

        control_frame = tk.Frame(self)
        control_frame.grid(row=1, column=0, sticky="we")

        self.step_entry = NumericSpinbox(control_frame, 5, (1, 100), width=5)
        self.step_entry.grid(row=1, column=1)

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

    def move(self, x, y):
        if self.move_command is not None:
            step = self.step_entry.get()
            self.move_command(x * step, y * step)
