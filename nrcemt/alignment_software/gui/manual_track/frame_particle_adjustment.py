import tkinter as tk

BUTTON_WIDTH = 3
RADIO_PADDING = 5


class ParticleAdjustmentFrame(tk.LabelFrame):

    def __init__(self, master, particle_count):
        super().__init__(master, text="Particle selection and ajustment", bd=1)

        selection_frame = tk.Frame(self)
        selection_frame.grid(row=0, column=0, sticky="we")
        for i in range(particle_count):
            radio = tk.Radiobutton(selection_frame, text=f"{i+1}")
            radio.grid(row=0, column=i)

        control_frame = tk.Frame(self)
        control_frame.grid(row=1, column=0, sticky="we")
        self.up_button = tk.Button(control_frame, text="▲", width=3)
        self.up_button.grid(row=0, column=1)
        self.left_button = tk.Button(control_frame, text="◀", width=3)
        self.left_button.grid(row=1, column=0)
        self.down_button = tk.Button(control_frame, text="▼", width=3)
        self.down_button.grid(row=2, column=1)
        self.right_button = tk.Button(control_frame, text="▶", width=3)
        self.right_button.grid(row=1, column=2)

        # self.particle_position = tk.Label(self)
        # self.particle_position.grid(
        #     row=2, column=3, columnspan=3
        # )

        # self.new_track_button = tk.Button(
        #     self, text="New Track", width=BUTTON_WIDTH
        # )
        # self.new_track_button.grid(
        #     row=1, column=9, columnspan=3
        # )
        # self.delete_track_button = tk.Button(
        #     self, text="Delete Track", width=BUTTON_WIDTH
        # )
        # self.delete_track_button.grid(
        #     row=3, column=9, columnspan=3
        # )

        # self.save_button = tk.Button(
        #     self, text="Save", width=BUTTON_WIDTH
        # )
        # self.save_button.grid(
        #     row=1, column=12, columnspan=3
        # )
        # self.reset_button = tk.Button(
        #     self, text="Reset", width=BUTTON_WIDTH
        # )
        # self.reset_button.grid(
        #     row=2, column=12, columnspan=3
        # )
        # self.all_reset_button = tk.Button(
        #     self, text="All Reset", width=BUTTON_WIDTH
        # )
        # self.all_reset_button.grid(
        #     row=3, column=12, columnspan=3
        # )
