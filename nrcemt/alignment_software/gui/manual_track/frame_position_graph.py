import tkinter as tk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PositionGraphFrame(tk.LabelFrame):

    def __init__(self, master, text):
        super().__init__(master, text=text)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.figure = Figure(figsize=(100, 100), dpi=100)
        self.axis = self.figure.add_subplot()
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(column=0, row=0, sticky="nwse")

    def render_positions(self, positions):
        self.axis.clear()
        self.axis.plot(positions)

    def update(self):
        self.canvas.draw()
