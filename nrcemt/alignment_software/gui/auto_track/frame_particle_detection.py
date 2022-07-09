import tkinter as tk


class ParticleDetectionFrame(tk.Frame):

    def __init__(self, master, particle_count):
        super().__init__(master)

        table_header = ["X1", "Y1", "IM1", "IM2"]
        for i, header in enumerate(table_header):
            header = tk.Label(self, text=header)
            header.grid(row=0, column=i+1)
            self.columnconfigure(i+1, weight=1)

        self.particle_select_var = tk.IntVar(0)
        self.track_checkboxes = []

        for i in range(particle_count):

            particle_select = tk.Radiobutton(
                self, text=f"{i+1}", value=i,
                variable=self.particle_select_var
            )
            particle_select.grid(row=i+1, column=0)

            for c in range(1, 5):
                label = tk.Label(self, bd=1, relief="solid", text="0")
                label.grid(row=i+1, column=c, sticky="nswe")

            end_button = tk.Button(self, text="Mark End")
            end_button.grid(row=i+1, column=5)

            self.track_checkboxes.append(
                tk.Checkbutton(self, text="Track")
            )
            self.track_checkboxes[i].grid(row=i+1, column=6)

        # self.track_button = tk.Button(
        #     self, text="Track Selected Particles"
        # )
        # self.track_button.grid(
        #     row=16, column=1, columnspan=7,
        #     sticky="wse", pady=10
        # )
