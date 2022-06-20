import pickle
import tkinter as tk
from tkinter import ttk
from .plasmon_section import PlasmonSelect, ResultBoxes, WidthComponent
import matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from nrcemt.qeels.engine.spectrogram import (
    load_spectrogram,
    process_spectrogram
)


matplotlib.use('TkAgg')


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        settings_frame = ttk.Frame()
        self.spectrogram_frame = ttk.Frame(width=500, height=500)
        self.spectrogram_data = None

        inputs = ttk.Frame(settings_frame)
        # Bulk Plasmons
        bulk_plasmon1 = PlasmonSelect(inputs, "Bulk Plasmon 1")
        bulk_plasmon2 = PlasmonSelect(inputs, "Bulk Plasmon 2")
        bulk_width = WidthComponent(inputs)
        bulk_plasmon1.grid(row=0, column=0, padx=2, pady=2)
        bulk_plasmon2.grid(row=0, column=1, padx=2, pady=2)
        bulk_width.grid(row=0, column=2, padx=2, pady=2, sticky="s")

        # Surface Plasmon Upper
        upper_plasmon1 = PlasmonSelect(inputs, "Surface Plasmon Upper 1")
        upper_plasmon2 = PlasmonSelect(inputs, "Surface Plasmon Upper 2")
        upper_width = WidthComponent(inputs)
        upper_plasmon1.grid(row=1, column=0, padx=2, pady=2)
        upper_plasmon2.grid(row=1, column=1, padx=2, pady=2)
        upper_width.grid(row=1, column=2, padx=2, pady=2, sticky="s")

        # Surface Plasmon Lower
        lower_plasmon1 = PlasmonSelect(inputs, "Surface Plasmon Lower 1")
        lower_plasmon2 = PlasmonSelect(inputs, "Surface Plasmon Lower 2")
        lower_width = WidthComponent(inputs)
        lower_plasmon1.grid(row=2, column=0, padx=2, pady=2)
        lower_plasmon2.grid(row=2, column=1, padx=2, pady=2)
        lower_width.grid(row=2, column=2, padx=2, pady=2, sticky="s")

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
            command=self.open_image
        )
        detect_button = ttk.Button(button_frame, text="Detect")
        save_button = ttk.Button(button_frame, text="Save Data")
        reset_button = ttk.Button(
            button_frame, text="Reset",
            command=self.reset
        )
        open_button.pack(side="left", padx=10, pady=10)
        detect_button.pack(side="left", padx=10, pady=10)
        save_button.pack(side="left", padx=10, pady=10)
        reset_button.pack(side="left", padx=10, pady=10)
        button_frame.pack(anchor="nw")

        settings_frame.pack(anchor='n', side="left")

        # Creating frame for spectrogram
        self.spectrogram_frame = ttk.Frame(width=500, height=500)

        # Setting up frame for rendering spectrogram
        self.figure = Figure(figsize=(8, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.spectrogram_frame)
        self.axis = self.figure.add_subplot()
        spectrogram_widget = self.canvas.get_tk_widget()

        # Adding spectrogram to frame
        spectrogram_widget.pack()

        # Adding frame to window
        self.spectrogram_frame.pack(side="left", anchor='n')

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
            spectrogram_processed = process_spectrogram(self.spectrogram_data)

            # Drawing spectrogram
            self.axis.clear()
            self.axis.imshow(spectrogram_processed)
            self.axis.set_xlabel("ev")
            self.axis.set_ylabel("micro rad")
            self.canvas.draw()

            # Binding to click to canvas(setup bind when image opened)
            self.bind('<ButtonPress>', self.add_feature)

            # Storing min/max values for later on
            self.y_max, self.y_min = self.axis.get_ylim()
            self.x_min, self.x_max = self.axis.get_xlim()

    def add_feature(self, event):
        # need to:
        # Update the entry spots

        # Changes location of "origin" to match matplotlib
        y_click = self.winfo_height()-event.y
        x_click = event.x

        # Transforms location from screen coordinates to data coordinaes
        x, y = self.axis.transData.inverted().transform((x_click, y_click))

        if (x > self.x_min and y > self.y_min and
                x < self.x_max and y < self.y_max):
            self.axis.plot([x], [y], marker="o", color="red")
            self.axis.annotate("TEMP_NAME", (x, y), color="red")
            self.canvas.draw()

    def reset(self):
        # removes spectrogram
        self.axis.clear()
        self.canvas.draw()
