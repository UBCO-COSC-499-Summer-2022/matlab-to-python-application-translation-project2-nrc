import tkinter as tk

BUTTON_WIDTH = 20
PADDING = 2
ENTRY_WIDTH = 5


class SelectedAreaFrame(tk.LabelFrame):

    def __init__(self, master, text):
        super().__init__(master, text=text)
        self.crop_area = tk.Checkbutton(
            self, text="Crop area"
        )
        self.crop_area.grid(row=0, column=0, columnspan=5, sticky="w")

        selected_particles = []

        row = 0
        for i in range(13):
            selected_particles.append(
                tk.Radiobutton(self, text=f"{i+1}")
            )
            row = int(i / 7) + 1
            column = int(i % 7)
            selected_particles[i].grid(
                row=row, column=column, padx=PADDING, pady=PADDING
            )
        row = row + 1

        selected_x_label = tk.Label(
            self, text="Selected X (pixel):", anchor="w"
        )
        self.x_value = tk.StringVar(self, value="64")
        self.selected_x_input = tk.Entry(
            self, bd=1, relief="solid",
            bg="white", fg="black", width=ENTRY_WIDTH,
            textvariable=self.x_value
        )
        selected_x_label.grid(row=row, column=2, columnspan=4)
        self.selected_x_input.grid(
            row=row, column=6, columnspan=2, sticky="w"
        )

        selected_y_label = tk.Label(
            self, text="Selected Y (pixel):", anchor="w"
        )
        self.y_value = tk.StringVar(self, value="64")
        self.selected_y_input = tk.Entry(
            self, bd=1, relief="solid",
            bg="white", fg="black", width=ENTRY_WIDTH,
            textvariable=self.y_value
        )
        selected_y_label.grid(row=row+1, column=2, columnspan=4)
        self.selected_y_input.grid(
            row=row+1, column=6, columnspan=2, sticky="w"
        )
