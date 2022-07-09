import tkinter as tk


class ParticleDetectionFrame(tk.Frame):

    def __init__(self, master, particle_count):
        super().__init__(master)

        table_header = [
            "X1", "Y1",
            "X2", "Y2",
            "IM1", "IM2"
        ]
        for i, header in enumerate(table_header):
            header = tk.Label(self, text=header)
            header.grid(row=0, column=i+1)
            self.columnconfigure(i+1, weight=1)

        self.lost_radio_button = []
        self.track_checkboxes = []

        for i in range(particle_count):
            particle_select = tk.Radiobutton(self, text=f"{i+1}")
            particle_select.grid(
                row=i+1, column=0
            )
            lost_button = tk.Button(self, text="Mark Lost")
            lost_button.grid(
                row=i+1, column=7
            )
            self.track_checkboxes.append(
                tk.Checkbutton(self, text="Track")
            )
            self.track_checkboxes[i].grid(
                row=i+1, column=8
            )

        # self.track_button = tk.Button(
        #     self, text="Track Selected Particles"
        # )
        # self.track_button.grid(
        #     row=16, column=1, columnspan=7,
        #     sticky="wse", pady=10
        # )
