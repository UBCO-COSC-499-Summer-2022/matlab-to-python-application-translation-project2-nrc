import tkinter as tk


class ParticleTableFrame(tk.Frame):
    """Create a table whihch shows tracking locations, and frame ranges."""

    def __init__(self, master, particle_count):
        """Create the table frame with a given number of particles."""
        super().__init__(master)

        table_header = ["X", "Y", "IM1", "IM2"]
        for i, header in enumerate(table_header):
            header = tk.Label(self, text=header)
            header.grid(row=0, column=i+2)

        self.mark_end_command = None
        self.reset_command = None
        self.particle_select_var = tk.IntVar(self, 0)
        self.data_vars = [[None] * 5 for i in range(particle_count)]
        self.track_vars = []

        for i in range(particle_count):

            particle_select = tk.Radiobutton(
                self, text=f"{i+1}", value=i,
                variable=self.particle_select_var
            )
            particle_select.grid(row=i+1, column=0)

            data_var = tk.StringVar(self, "o")
            label = tk.Label(self, textvariable=data_var)
            label.grid(row=i+1, column=1, sticky="nswe")
            self.data_vars[i][0] = data_var

            for c in range(4):
                data_var = tk.StringVar(self, "-")
                label = tk.Label(
                    self, textvariable=data_var,
                    width=8, bd=1, relief="solid"
                )
                label.grid(row=i+1, column=c+2, sticky="nswe")
                self.data_vars[i][c+1] = data_var

            end_button = tk.Button(
                self, text="Mark End",
                command=lambda particle_index=i: self.mark_end(particle_index)
            )
            end_button.grid(row=i+1, column=6)

            reset_button = tk.Button(
                self, text="Reset",
                command=lambda particle_index=i: self.reset(particle_index)
            )
            reset_button.grid(row=i+1, column=7)

            track_var = tk.BooleanVar(self, False)
            self.track_vars.append(track_var)
            track_checkbox = tk.Checkbutton(
                self, text="Select", variable=track_var
            )
            track_checkbox.grid(row=i+1, column=8)

    def update_data(
        self, particle_positions,
        tracking_positions, tracking_start_frames, tracking_end_frames
    ):
        """Update the contents of the table."""
        for i, position in enumerate(tracking_positions):
            status = particle_positions.get_status(i)
            if status == "complete":
                icon = "●"
            elif status == "partial":
                icon = "◒"
            else:
                icon = "○"
            self.data_vars[i][0].set(icon)
            if position is not None:
                self.data_vars[i][1].set(position[0])
                self.data_vars[i][2].set(position[1])
            else:
                self.data_vars[i][1].set("-")
                self.data_vars[i][2].set("-")
            self.data_vars[i][3].set(tracking_start_frames[i]+1)
            self.data_vars[i][4].set(tracking_end_frames[i]+1)

    def get_selected_particle(self):
        """Get the index of the particle selected by the radio button"""
        return self.particle_select_var.get()

    def get_tracked_particles(self):
        """Get particles selected for tracking."""
        tracked = []
        for i, variable in enumerate(self.track_vars):
            if variable.get():
                tracked.append(i)
        return tracked

    def enable_tracking(self, particle_index):
        """Selects a particle for tracking."""
        self.track_vars[particle_index].set(True)

    def disable_tracking(self, particle_index):
        """Deselects a particle for tracking."""
        self.track_vars[particle_index].set(False)

    def set_mark_end_command(self, command):
        """Sets a command that gets called when mark end is clicked."""
        self.mark_end_command = command

    def mark_end(self, particle_index):
        """Called when a mark button is clicked with a given index."""
        if self.mark_end_command is not None:
            self.mark_end_command(particle_index)

    def set_reset_command(self, command):
        """Sets a command that gets called when reset is clicked."""
        self.reset_command = command

    def reset(self, particle_index):
        """Called when a reset button is clicked with a given index."""
        self.disable_tracking(particle_index)
        if self.reset_command is not None:
            self.reset_command(particle_index)
