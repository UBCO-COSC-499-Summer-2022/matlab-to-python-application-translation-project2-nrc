import tkinter as tk


class ParticleDetectionFrame(tk.LabelFrame):

    def __init__(self, master, text):
        super().__init__(master, text=text, bd=1)

        for i in range(15):
            self.columnconfigure(i, weight=1)

        for i in range(9):
            self.rowconfigure(i, weight=1)

        table_header = [
            "X1", "Y1",
            "X2", "Y2",
            "IM1", "IM2"
        ]
        for i, header in enumerate(table_header):
            header = tk.Label(self, text=header)
            header.grid(row=0, column=i+1)

        self.select_radio_button = []
        for i in range(15):
            self.select_radio_button.append(
                tk.Checkbutton(self, text=f"{i+1}")
            )
            self.select_radio_button[i].grid(row=i+1, column=0)

        self.lost_radio_button = []
        for i in range(15):
            self.lost_radio_button.append(
                tk.Checkbutton(self, text="Lost")
            )
            self.lost_radio_button[i].grid(row=i+1, column=8)

        self.track_radio_button = []
        for i in range(15):
            self.track_radio_button.append(
                tk.Checkbutton(self, text="Track")
            )
            self.track_radio_button[i].grid(row=i+1, column=9)

        self.track_button = tk.Button(
            self, text="Track Selected Particles"
        )
