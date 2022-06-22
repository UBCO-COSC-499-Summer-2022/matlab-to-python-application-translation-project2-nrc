import tkinter as tk
from tkinter import ttk
from nrcemt.qeels.gui.frame_canvas import frame_canvas
from .plasmon_section import PlasmonSelect, ResultBoxes, WidthComponent
import matplotlib
import numpy as np

matplotlib.use('TkAgg')

# TODO:
# directly editing text boxes needs to update location on spectrogram


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()

        # Creating variables for the ui
        self.radio_variable = tk.IntVar()
        self.plasmon_array = np.array([])
        settings_frame = ttk.Frame()
        self.spectrogram_data = None
        self.spectrogram_processed = None
        inputs = ttk.Frame(settings_frame)

        # Bulk Plasmons
        self.bulk_plasmon1 = PlasmonSelect(
            inputs, "Bulk Plasmon 1",
            self.radio_variable, 0
        )
        self.plasmon_array = np.append(
            self.plasmon_array, [self.bulk_plasmon1]
        )
        self.bulk_plasmon2 = PlasmonSelect(
            inputs, "Bulk Plasmon 2",
            self.radio_variable, 1
        )
        self.plasmon_array = np.append(
            self.plasmon_array, [self.bulk_plasmon2]
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
        self.plasmon_array = np.append(
            self.plasmon_array, [self.upper_plasmon1]
        )

        self.upper_plasmon2 = PlasmonSelect(
            inputs, "Surface Plasmon Upper 2",
            self.radio_variable, 3
        )
        self.plasmon_array = np.append(
            self.plasmon_array, [self.upper_plasmon2]
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
        self.plasmon_array = np.append(
            self.plasmon_array, [self.lower_plasmon1]
        )

        self.lower_plasmon2 = PlasmonSelect(
            inputs, "Surface Plasmon Lower 2",
            self.radio_variable, 5
        )
        self.plasmon_array = np.append(
            self.plasmon_array, [self.lower_plasmon2]
        )

        self.lower_width = WidthComponent(inputs)
        self.lower_plasmon1.grid(row=2, column=0, padx=2, pady=2)
        self.lower_plasmon2.grid(row=2, column=1, padx=2, pady=2)
        self.lower_width.grid(row=2, column=2, padx=2, pady=2, sticky="s")

        inputs.pack(anchor="w")

        self.spectrogram_frame = ttk.Frame()
        # Create the canvas
        self.canvas = frame_canvas(
            self.spectrogram_frame,
            self.radio_variable,
            self.plasmon_array
        )

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
            command=self.canvas.open_image
        )
        detect_button = ttk.Button(button_frame, text="Detect")
        save_button = ttk.Button(button_frame, text="Save Data")
        reset_button = ttk.Button(
            button_frame, text="Reset",
            command=self.canvas.reset
        )
        open_button.pack(side="left", padx=10, pady=10)
        detect_button.pack(side="left", padx=10, pady=10)
        save_button.pack(side="left", padx=10, pady=10)
        reset_button.pack(side="left", padx=10, pady=10)
        button_frame.pack(anchor="nw")
        settings_frame.pack(anchor='n', side="left")

        # Adding frame to window
        self.spectrogram_frame.pack(side="left", anchor='n')
