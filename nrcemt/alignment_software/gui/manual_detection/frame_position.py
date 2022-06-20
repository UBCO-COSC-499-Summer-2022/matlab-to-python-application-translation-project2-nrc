import tkinter as tk


class PositionFrame(tk.LabelFrame):

    def __init__(self, master):
        super().__init__(master)
        tk.Label(
            self, text="Testing grid size"
        ).grid(row=0, column=0, sticky="nwse")
