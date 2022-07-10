import tkinter as tk


class ParticleTableFrame(tk.Frame):

    def __init__(self, master, particle_count):
        super().__init__(master)

        table_header = ["X", "Y", "IM1", "IM2"]
        for i, header in enumerate(table_header):
            header = tk.Label(self, text=header)
            header.grid(row=0, column=i+1)

        self.mark_end_command = None
        self.reset_command = None
        self.particle_select_var = tk.IntVar(0)
        self.data_vars = [[None] * 4 for i in range(particle_count)]
        self.track_vars = []

        for i in range(particle_count):

            particle_select = tk.Radiobutton(
                self, text=f"{i+1}", value=i,
                variable=self.particle_select_var
            )
            particle_select.grid(row=i+1, column=0)

            for c in range(4):
                data_var = tk.StringVar(self, "-")
                label = tk.Label(
                    self, textvariable=data_var,
                    width=8, bd=1, relief="solid"
                )
                label.grid(row=i+1, column=c+1, sticky="nswe")
                self.data_vars[i][c] = data_var

            end_button = tk.Button(
                self, text="Mark End",
                command=lambda particle_index=i: self.mark_end(particle_index)
            )
            end_button.grid(row=i+1, column=5)

            reset_button = tk.Button(
                self, text="Reset",
                command=lambda particle_index=i: self.reset(particle_index)
            )
            reset_button.grid(row=i+1, column=6)

            track_var = tk.BooleanVar(False)
            self.track_vars.append(track_var)
            track_checkbox = tk.Checkbutton(
                self, text="Track", variable=track_var
            )
            track_checkbox.grid(row=i+1, column=7)

    def update_data(self, particle_locations, frame_index):
        for i, particle in enumerate(particle_locations):
            location = particle[frame_index]
            if location is not None:
                self.data_vars[i][0].set(location[0])
                self.data_vars[i][1].set(location[1])
            else:
                self.data_vars[i][0].set("-")
                self.data_vars[i][1].set("-")
            self.data_vars[i][2].set(particle.get_first_frame()+1)
            self.data_vars[i][3].set(particle.get_last_frame()+1)

    def get_selected_particle(self):
        return self.particle_select_var.get()

    def get_tracked_particles(self):
        tracked = []
        for i, variable in enumerate(self.track_vars):
            if variable.get():
                tracked.append(i)
        return tracked

    def enable_tracking(self, particle_index):
        self.track_vars[particle_index].set(True)

    def disable_tracking(self, particle_index):
        self.track_vars[particle_index].set(False)

    def set_mark_end_command(self, command):
        self.mark_end_command = command

    def mark_end(self, particle_index):
        if self.mark_end_command is not None:
            self.mark_end_command(particle_index)

    def set_reset_command(self, command):
        self.set_reset_command = command

    def reset(self, particle_index):
        self.disable_tracking(particle_index)
        if self.set_reset_command is not None:
            self.set_reset_command(particle_index)
