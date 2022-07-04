import tkinter as tk
from .frame_table import TableFrame

TABLE_ROWS = 13
TABLE_COLUMNS = 6
INIT_ROWS = [0, 0, 0, 0, 1, 61]


class ParticleDetectionFrame(tk.LabelFrame):

    def __init__(self, master, text):
        super().__init__(master, text=text, bd=1)

        table_header = [
            "X1", "Y1",
            "X2", "Y2",
            "IM1", "IM2"
        ]
        for i, header in enumerate(table_header):
            header = tk.Label(self, text=header)
            header.grid(row=0, column=i+1)

        self.select_radio_button = []
        self.lost_radio_button = []
        self.track_radio_button = []
        self.particles_data = []

        for i in range(TABLE_ROWS):
            self.rowconfigure(i + 1, weight=1)
            self.select_radio_button.append(
                tk.Checkbutton(self, text=f"{i+1}")
            )
            self.select_radio_button[i].grid(
                row=i+1, column=0
            )

            self.lost_radio_button.append(
                tk.Checkbutton(self, text="Lost")
            )
            self.lost_radio_button[i].grid(
                row=i+1, column=7
            )

            self.track_radio_button.append(
                tk.Checkbutton(self, text="Track")
            )
            self.track_radio_button[i].grid(
                row=i+1, column=8
            )

            self.particles_data.append(INIT_ROWS)

        for i in range(13):
            if i < 6:
                self.columnconfigure(i+1, weight=1)
            self.rowconfigure(i, weight=1)

        self.data = TableFrame(
            self, TABLE_ROWS,
            TABLE_COLUMNS, self.particles_data
        )
        self.data.grid(
            row=1, column=1, sticky="nwse",
            rowspan=TABLE_ROWS, columnspan=TABLE_COLUMNS,
        )

        self.track_button = tk.Button(
            self, text="Track Selected Particles"
        )
        self.track_button.grid(
            row=16, column=1, columnspan=7,
            sticky="wse", pady=10
        )
