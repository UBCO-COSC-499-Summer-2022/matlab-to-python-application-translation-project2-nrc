import tkinter as tk
import matplotlib.patches as patches
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class HistogramFrame(tk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.figure = Figure(figsize=(8, 8), dpi=100)
        self.axis = self.figure.add_subplot()
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(column=0, row=0, sticky="nwse")
        self.patch = None
        self.hist = None

    def render_histogram(self, image):
        image_flat = image.ravel()
        image_max = image.max()
        self.axis.clear()
        self.axis.hist(image_flat, bins=100, range=(0, image_max))
        self.axis.xaxis.set_ticks(
            [0.0, 0.25*image_max, 0.5*image_max, 0.75*image_max, image_max],
            labels=["0.0", "0.25", "0.5", "0.75", "1.0"]
        )
        self.axis.get_yaxis().set_visible(False)
        self.canvas.draw()

    def render_range(self, vmin, vmax):
        if self.patch is not None:
            self.patch.remove()
        self.patch = patches.Rectangle(
            (vmin, 0.1),
            vmax-vmin, 0.8,
            linewidth=1,
            edgecolor='r',
            facecolor='none',
            transform=self.axis.get_xaxis_transform()
        )
        self.axis.add_patch(self.patch)
        self.canvas.draw()
