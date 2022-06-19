import tkinter as tk
from tkinter import ttk


class ImageAdjustmentFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master, borderwidth=1, relief="ridge")

        # Create input widgets
        input_labels = [
            "Offset X (pixel)",
            "Offset Y (pixel)",
            "Angle (degree)"
        ]
        for i, label in enumerate(input_labels):
            label = ttk.Label(self, text=label)
            label.grid(row=i, column=0)
            input = ttk.Entry(self, width=10)
            input.grid(row=i, column=1)

        # Create slider widget
        self.__create_radio("Binning", 3)

        # Create checkbox widget
        sobel = tk.Checkbutton(self, text="Use Sobel")
        sobel.grid(column=0, row=4)

        self.grid(column=0, row=0)

    def __create_radio(self, text, i):
        label = ttk.Label(self, text=text)
        label.grid(column=0, row=i)

        # Create frame to contain radio buttons
        radio_frame = ttk.Frame(self)
        radio_frame.grid(column=1, row=i)
        for i in range(4):
            radio = tk.Radiobutton(
                radio_frame,
                text=f"{2**(i+1)}"
            )
            radio.grid(column=i, row=0)
