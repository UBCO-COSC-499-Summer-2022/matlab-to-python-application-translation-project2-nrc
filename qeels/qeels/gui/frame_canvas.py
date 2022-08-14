import tkinter as tk
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle


class CanvasFrame(tk.Frame):
    """
    Creates canvas used to display spectrum
    """
    def __init__(self, master, click_command=None):
        super().__init__(master)
        self.click_command = click_command

        # Setting up frame for rendering spectrogram
        self.figure = Figure(figsize=(8, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master)
        self.axis = self.figure.add_subplot()
        self.axis.set_axis_off()
        spectrogram_widget = self.canvas.get_tk_widget()
        # Adding spectrogram to frame
        spectrogram_widget.pack()
        self.axis.set_xlabel("ev")
        self.axis.set_ylabel("micro rad")
        self.axis.set_axis_on()
        self.point_lines = []

    def on_click(self, event):
        """On click event for canvas"""
        y = event.y
        x = event.x

        # Transforms location from screen coordinates to data coordinaes
        x, y = self.axis.transData.inverted().transform((x, y))

        # If location falls in bounds plot it
        in_bounds = (
            x > self.x_min and y > self.y_min
            and x < self.x_max and y < self.y_max
        )
        if in_bounds and self.click_command is not None:
            self.click_command(x, y)

    def render_spectrogram(self, spectrogram, contrast_min, contrast_max):
        """Renders passed in spectrogram"""
        self.axis.clear()
        mininum = spectrogram.min()
        maximum = spectrogram.max()
        dynamic_range = maximum - mininum
        vmin = mininum + contrast_min * dynamic_range
        vmax = mininum + contrast_max * dynamic_range
        self.axis.imshow(spectrogram, vmin=vmin, vmax=vmax)
        self.canvas.draw()

        # Binding to click to canvas(setup bind when image opened)
        self.canvas.mpl_connect("button_press_event", self.on_click)

        # Storing min/max values for later on
        self.y_max, self.y_min = self.axis.get_ylim()
        self.x_min, self.x_max = self.axis.get_xlim()

        # Prevents image from being resized
        self.axis.set_xlim(self.x_min, self.x_max)
        self.axis.set_ylim(self.y_max, self.y_min)

    def render_point(self, x, y, label):
        """
        Draws the provided point on the spectrogram with the provided label
        """
        in_bounds = (
            x > self.x_min and y > self.y_min
            and x < self.x_max and y < self.y_max
        )
        if not in_bounds:
            return
        self.axis.plot(
            [x], [y],
            marker="o",
            color="red"
        )
        self.axis.annotate(
            label,
            (x-10, y-10),
            color="red",
        )

    def update(self):
        """Re-draws the canvas"""
        self.canvas.draw()

    def render_rect(self, pos1, pos2, width):
        """Draws a rectangle on the canvas"""
        delta_x = (pos1[0] - pos2[0])
        delta_y = (pos1[1] - pos2[1])
        square_angle = math.atan2(delta_y, delta_x)
        hypotenuse = math.sqrt(
            math.pow(delta_x, 2) +
            math.pow(delta_y, 2)
        )
        x = pos1[0] + math.sin(square_angle) * (width/2)
        y = pos1[1] - math.cos(square_angle) * (width/2)

        square_angle = 90+(180/math.pi)*(square_angle)
        rect = Rectangle(
            (x, y),
            width, hypotenuse,
            edgecolor='red',
            facecolor='none',
            angle=square_angle
        )
        self.axis.add_patch(rect)
