import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

BUTTON_WIDTH = 20


class ToolFrame(tk.Frame):

    def __init__(self, master):
        super().__init__(master)

        top_frame = tk.Frame(self)
        top_frame.pack(side="left", anchor="n", fill="y", expand=True)

        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=3)
        top_frame.columnconfigure(2, weight=1)

        data_range = tk.Frame(top_frame, bd=1, relief="ridge")
        data_range.grid(column=0, row=0)
        min_label = ttk.Label(data_range, text="Minimum:")
        min_label.grid(column=0, row=0)
        min_range = tk.Frame(data_range)
        self.min_range_val = ttk.Label(min_range, text="0")
        self.min_range_val.pack()
        min_range.grid(column=1, row=0)

        max_range = tk.Frame(data_range)
        self.max_range_val = ttk.Label(max_range, text="1")

