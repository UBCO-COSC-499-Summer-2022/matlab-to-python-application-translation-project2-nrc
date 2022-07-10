from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle


# TODO: MAYBE REFACTOR THIS TO COMMON WITH QEELS CANVAS FRAME
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
            self.click_command(int(x), int(y))

    def render_image(self, img, vmin=None, vmax=None):
        self.axis.clear()
        self.axis.imshow(img, cmap="gray", vmin=vmin, vmax=vmax)
        self.canvas.draw()

    def render_point(self, location, color="red"):
        self.axis.plot(
            [location[0]], [location[1]],
            marker="o",
            color=color
        )

    def render_rect(self, center, size, color="red"):
        x = center[0] - size[0] / 2
        y = center[1] - size[1] / 2
        rect = Rectangle(
            (x, y),
            size[0], size[1],
            edgecolor=color,
            facecolor='none',
            linewidth=2
        )
        self.axis.add_patch(rect)

    def update(self):
        self.canvas.draw()
