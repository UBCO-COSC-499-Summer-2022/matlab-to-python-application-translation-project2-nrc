from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import matplotlib.patheffects as pe


class ImageFrame(ttk.Frame):
    """Matplotlib canvas for rendering images and marking them up."""

    def __init__(self, master, **kwargs):
        """Create the canvas."""
        super().__init__(master, **kwargs)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.figure = Figure(figsize=(8, 8), dpi=100)
        self.axis = self.figure.add_subplot()
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().grid(column=0, row=0, sticky="nwse")
        self.click_command = None
        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.y_min, self.y_max = 0, 0
        self.x_min, self.x_max = 0, 0

    def set_click_command(self, command):
        """Sets the command to be called when the image is clicked."""
        self.click_command = command

    def on_click(self, event):
        """Handle the click event."""
        if self.click_command is not None:
            x, y = self.axis.transData.inverted().transform((event.x, event.y))
            x, y = int(x), int(y)
            if x < self.x_min or x >= self.x_max:
                return
            if y < self.y_min or y >= self.y_max:
                return
            self.click_command(int(x), int(y))

    def render_image(self, img, vmin=0.0, vmax=1.0):
        """Render an image with a given dynamic range."""
        self.axis.clear()
        self.axis.imshow(img, cmap="gray", vmin=vmin, vmax=vmax)
        self.y_max, self.y_min = self.axis.get_ylim()
        self.x_min, self.x_max = self.axis.get_xlim()
        self.axis.set_xlim(self.x_min, self.x_max)
        self.axis.set_ylim(self.y_max, self.y_min)

    def render_point(self, location, color="red"):
        """Draw a single point on the image."""
        self.axis.plot(
            [location[0]], [location[1]],
            marker="o",
            markersize=4,
            color=color
        )

    def render_rect(self, center, size, color="red"):
        """Draw a rectangle centered on a point."""
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

    def render_text(self, position, text, color="white", outline="black"):
        """Render text with an outline."""
        self.axis.text(
            *position, text, size=12, color=color, ha='center', va='bottom',
            path_effects=[pe.withStroke(linewidth=2, foreground=outline)]
        )

    def update(self):
        """Update the canvas and display it."""
        self.canvas.draw()
