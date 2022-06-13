import tkinter as tk
from tkinter import ttk
from nrcemt.qeels.engine import qeels_engine_greeting


class PlasmonSelect(ttk.Frame):
    # initializing
    def __init__(self, master, name):
        # padding
        self.xpad = 5
        self.ypad = 5
        super().__init__(master)
        self.name = name
        # new frame
        frm = ttk.Frame(self)

        # creates styling for radio buttons
        # creates the radio button
        self.radio_btn = ttk.Radiobutton(self, text=name, width=25)
        self.radio_btn.pack(anchor=tk.W)

        # creates label
        self.lbl = ttk.Label(frm, text="X: ")
        self.lbl.pack(side="left", padx=self.xpad, pady=self.ypad)

        # Creates entry box
        self.x_entry = ttk.Entry(frm, width=7)
        self.x_entry.pack(side="left", padx=self.xpad, pady=self.ypad)

        # creates label
        self.lbl = ttk.Label(frm, text="Y: ")
        self.lbl.pack(side="left", padx=self.xpad, pady=self.ypad)

        # Creates entry box
        self.x_entry = ttk.Entry(frm, width=7)
        self.x_entry.pack(side="left", padx=self.xpad, pady=self.ypad)
        frm.pack()


class ResultBoxes(ttk.Frame):
    def __init__(self, master, name):
        super().__init__(master)
        ev_label = ttk.Label(self, text=name + ": ", width=20)
        ev_entry = ttk.Entry(self, width=7)
        ev_label.pack(side="left")
        ev_entry.pack(side="left")
