import tkinter as tk
from tkinter import ttk


class PlasmonSelect(ttk.Frame):
    # initializing
    def __init__(self, master, name):

        # padding
        self.xpad = 2
        self.ypad = 2
        super().__init__(master)

        # new frame that contains labels and entry boxes
        entry_frame = ttk.Frame(self)

        # creates styling for radio buttons
        # creates the radio button
        self.radio_btn = ttk.Radiobutton(self, text=name, width=25)
        self.radio_btn.pack(anchor=tk.W)

        # creates label
        self.x_label = ttk.Label(entry_frame, text="X: ")
        self.x_label.pack(side="left", padx=self.xpad, pady=self.ypad)

        # Creates entry box
        self.x_entry = ttk.Entry(entry_frame, width=7)
        self.x_entry.pack(side="left", padx=self.xpad, pady=self.ypad)

        # creates label
        self.y_label = ttk.Label(entry_frame, text="Y: ")
        self.y_label.pack(side="left", padx=self.xpad, pady=self.ypad)

        # Creates entry box
        self.y_entry = ttk.Entry(entry_frame, width=7)
        self.y_entry.pack(side="left", padx=self.xpad, pady=self.ypad)
        entry_frame.pack()


class ResultBoxes(ttk.Frame):
    def __init__(self, master, name):
        super().__init__(master)
        ev_label = ttk.Label(self, text=name + ": ", width=20)
        ev_entry = ttk.Entry(self, width=7)
        ev_label.pack(side="left", pady=2)
        ev_entry.pack(side="left", pady=2)
