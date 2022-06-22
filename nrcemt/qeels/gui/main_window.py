import tkinter as tk
from tkinter import ttk
from nrcemt.qeels.gui.frame_canvas import frame_canvas
from .plasmon_section import PlasmonSelect, ResultBoxes, WidthComponent
import matplotlib
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



matplotlib.use('TkAgg')

# TODO:
# directly editing text boxes needs to update location on spectrogram

class MainWindow(tk.Tk):


    def __init__(self):
        super().__init__()
        settings_frame = ttk.Frame()
        self.spectrogram_frame = ttk.Frame()
        self.canvas_frame = frame_canvas(self.spectrogram_frame)

        self.spectrogram_data = None
        self.spectrogram_processed = None

        # Creating variables for the ui
        self.radio_variable = tk.IntVar()
        self.x_array = np.array([0, 0, 0, 0, 0, 0])
        self.y_array = np.array([0, 0, 0, 0, 0, 0])

        inputs = ttk.Frame(settings_frame)
        # Bulk Plasmons
        self.bulk_plasmon1 = PlasmonSelect(
            inputs, "Bulk Plasmon 1",
            self.radio_variable, 0
        )

        self.bulk_plasmon2 = PlasmonSelect(
            inputs, "Bulk Plasmon 2",
            self.radio_variable, 1
        )

        self.bulk_width = WidthComponent(inputs)
        self.bulk_plasmon1.grid(row=0, column=0, padx=2, pady=2)
        self.bulk_plasmon2.grid(row=0, column=1, padx=2, pady=2)
        self.bulk_width.grid(row=0, column=2, padx=2, pady=2, sticky="s")

        # Surface Plasmon Upper
        self.upper_plasmon1 = PlasmonSelect(
            inputs, "Surface Plasmon Upper 1",
            self.radio_variable, 2
        )
        self.upper_plasmon2 = PlasmonSelect(
            inputs, "Surface Plasmon Upper 2",
            self.radio_variable, 3
        )
        self.upper_width = WidthComponent(inputs)
        self.upper_plasmon1.grid(row=1, column=0, padx=2, pady=2)
        self.upper_plasmon2.grid(row=1, column=1, padx=2, pady=2)
        self.upper_width.grid(row=1, column=2, padx=2, pady=2, sticky="s")

        # Surface Plasmon Lower
        self.lower_plasmon1 = PlasmonSelect(
            inputs, "Surface Plasmon Lower 1",
            self.radio_variable, 4
        )
        self.lower_plasmon2 = PlasmonSelect(
            inputs, "Surface Plasmon Lower 2",
            self.radio_variable, 5
        )
        self.lower_width = WidthComponent(inputs)
        self.lower_plasmon1.grid(row=2, column=0, padx=2, pady=2)
        self.lower_plasmon2.grid(row=2, column=1, padx=2, pady=2)
        self.lower_width.grid(row=2, column=2, padx=2, pady=2, sticky="s")

        inputs.pack(anchor="w")

        # Average Pixel
        results = ttk.Frame(settings_frame)
        average_pixel = ResultBoxes(results, "Average Pixel")
        average_pixel.pack()

        # Micro rad/pixel upper
        rad_upper = ResultBoxes(results, "Micro rad/Pixel Upper")
        rad_upper.pack()

        # Micro rad/pixel lower
        rad_lower = ResultBoxes(results, "Micro rad/Pixel Lower")
        rad_lower.pack()

        # Ev/Pixel
        ev = ResultBoxes(results, "EV/Pixel")
        ev.pack()
        results.pack(anchor="nw", pady=20, padx=10)

        # adding buttons
        button_frame = ttk.Frame(settings_frame)
        open_button = ttk.Button(
            button_frame, text="Open Image",
            command=self.canvas_frame.open_image
        )
        detect_button = ttk.Button(button_frame, text="Detect")
        save_button = ttk.Button(button_frame, text="Save Data")
        reset_button = ttk.Button(button_frame, text="Reset",command=self.canvas_frame.reset)
        open_button.pack(side="left", padx=10, pady=10)
        detect_button.pack(side="left", padx=10, pady=10)
        save_button.pack(side="left", padx=10, pady=10)
        reset_button.pack(side="left", padx=10, pady=10)
        button_frame.pack(anchor="nw")

        settings_frame.pack(anchor='n', side="left")

        self.canvas_frame.pack()
        # Adding frame to window
        self.spectrogram_frame.pack(side="left", anchor='n')
