import tkinter as tk

BUTTON_WIDTH = 10
RADIO_PADDING = 5


class ParticleAdjustmentFrame(tk.LabelFrame):

    def __init__(self, master, text):
        super().__init__(master, text=text, bd=1)
        for i in range(15):
            if i < 4:
                self.rowconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

        self.particle_selection = []
        for i in range(13):
            self.particle_selection.append(
                tk.Radiobutton(self, text=f"{i+1}")
            )
            self.particle_selection[i].grid(
                row=0, column=i+1, padx=RADIO_PADDING
            )

        self.up_button = tk.Button(
            self, text="Up", width=BUTTON_WIDTH
        )
        self.up_button.grid(
            row=1, column=3, columnspan=3
        )
        self.left_button = tk.Button(
            self, text="Left", width=BUTTON_WIDTH
        )
        self.left_button.grid(
            row=2, column=0, columnspan=3
        )
        self.down_button = tk.Button(
            self, text="Down", width=BUTTON_WIDTH
        )
        self.down_button.grid(
            row=3, column=3, columnspan=3
        )
        self.right_button = tk.Button(
            self, text="Right", width=BUTTON_WIDTH
        )
        self.right_button.grid(
            row=2, column=6, columnspan=3
        )

        self.particle_position = tk.Label(self)
        self.particle_position.grid(
            row=2, column=3, columnspan=3
        )

        self.new_track_button = tk.Button(
            self, text="New Track", width=BUTTON_WIDTH
        )
        self.new_track_button.grid(
            row=1, column=9, columnspan=3
        )
        self.delete_track_button = tk.Button(
            self, text="Delete Track", width=BUTTON_WIDTH
        )
        self.delete_track_button.grid(
            row=3, column=9, columnspan=3
        )

        self.save_button = tk.Button(
            self, text="Save", width=BUTTON_WIDTH
        )
        self.save_button.grid(
            row=1, column=12, columnspan=3
        )
        self.reset_button = tk.Button(
            self, text="Reset", width=BUTTON_WIDTH
        )
        self.reset_button.grid(
            row=2, column=12, columnspan=3
        )
        self.all_reset_button = tk.Button(
            self, text="All Reset", width=BUTTON_WIDTH
        )
        self.all_reset_button.grid(
            row=3, column=12, columnspan=3
        )
