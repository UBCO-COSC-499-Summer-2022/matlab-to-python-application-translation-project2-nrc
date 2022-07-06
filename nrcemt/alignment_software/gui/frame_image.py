from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class ImageFrame(ttk.Frame):

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.figure = Figure(figsize=(8, 8), dpi=100)
        self.axis = self.figure.add_subplot()
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(column=0, row=0, sticky="nwse")
        self.click_command = None
        self.canvas.mpl_connect("button_press_event", self.on_click)

    def set_click_command(self, command):
        self.click_command = command

    def on_click(self, event):
        if self.click_command is not None:
            x, y = self.axis.transData.inverted().transform((event.x, event.y))
            self.click_command(x, y)

    def render_image(self, img, vmin=None, vmax=None):
        self.axis.clear()
        self.axis.imshow(img, cmap="gray", vmin=vmin, vmax=vmax)
        self.canvas.draw()
