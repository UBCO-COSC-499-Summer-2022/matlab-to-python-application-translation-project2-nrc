import tkinter as tk
import pickle
import matplotlib
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from nrcemt.qeels.engine.spectrogram import (
    load_spectrogram,
    process_spectrogram
)


class frame_canvas(tk.Frame):


    def __init__(self, master, radio_variable,x_array,y_array,plasmon_array):
        super().__init__(master)
        # Setting up variables
        self.radio_variable = radio_variable
        self.x_array=x_array
        self.y_array=y_array
        self.plasmon_array=plasmon_array


        # Setting up frame for rendering spectrogram
        self.figure = Figure(figsize=(8, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master)
        self.axis = self.figure.add_subplot()
        self.axis.set_axis_off()
        spectrogram_widget = self.canvas.get_tk_widget()
        # Adding spectrogram to frame
        spectrogram_widget.pack()

    def open_image(self):
        # Potentially add ability to filter by file types
        file_path = tk.filedialog.askopenfilename()
        if(len(file_path) != 0):
            # Rendering spectrogram
            # If error loading file, error message is displayed
            try:
                self.spectrogram_data = load_spectrogram(file_path)
            except (OSError, pickle.UnpicklingError):
                tk.messagebox.showerror(
                    title="Error",
                    message=(
                        "Something went wrong loading the spectrogram." +
                        "\n Please try again!"
                    )
                )
                return

            # Processing spectrogram data
            self.spectrogram_processed = process_spectrogram(
                self.spectrogram_data
            )

            # Drawing spectrogram
            self.axis.clear()
            self.axis.imshow(self.spectrogram_processed)
            self.axis.set_xlabel("ev")
            self.axis.set_ylabel("micro rad")
            self.axis.set_axis_on()
            self.canvas.draw()

            # Binding to click to canvas(setup bind when image opened)
            # self.bind('<ButtonPress>', self.on_click)
            self.canvas.mpl_connect('button_press_event',self.on_click)

            # Storing min/max values for later on
            self.y_max, self.y_min = self.axis.get_ylim()
            self.x_min, self.x_max = self.axis.get_xlim()

    def on_click(self, event):
        y = event.y
        x = event.x

        # Transforms location from screen coordinates to data coordinaes
        x, y = self.axis.transData.inverted().transform((x, y))

        # If location falls in bounds plot it
        if (x > self.x_min and y > self.y_min and
                x < self.x_max and y < self.y_max):
            self.add_feature(x, y)
    
    def add_feature(self, x, y):
        self.x_array[self.radio_variable.get()] = x
        self.y_array[self.radio_variable.get()] = y

        # redraw canvas
        self.redraw_points()

        # Convert to int for display
        x = int(x)
        y = int(y)

        print(self.plasmon_array)
    
        for plasmons in range(self.plasmon_array.size):
            print(plasmons)
            print(self.plasmon_array[plasmons])
            self.plasmon_array[plasmons].x.set(self.x_array[plasmons])
            self.plasmon_array[plasmons].y.set(self.y_array[plasmons])


    
    def redraw_points(self):
        # Erase previouse plot (change if possible)
        self.axis.clear()
        self.axis.imshow(self.spectrogram_processed)

        # re-draws the locations
        for i in range(6):
            if(self.x_array[i] != 0 and self.y_array[i] != 0):
                self.axis.plot(
                    [self.x_array[i]], [self.y_array[i]],
                    marker="o", color="red"
                )
                self.axis.annotate(
                    int(i/2) + 1, (self.x_array[i]-10, self.y_array[i]-15),
                    color="black"
                )
        self.canvas.draw()

    def reset(self):
        if self.spectrogram_processed is not None:
            self.x_array = np.array([0, 0, 0, 0, 0, 0])
            self.y_array = np.array([0, 0, 0, 0, 0, 0])
            self.redraw_points()