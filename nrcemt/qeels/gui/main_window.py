import tkinter as tk
from tkinter import ttk
from .plasmon_section import PlasmonSelect, ResultBoxes, WidthComponent
import matplotlib
from matplotlib import pyplot
from matplotlib.figure import Figure
from tkinter import filedialog
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from nrcemt.qeels.engine.prz import load_prz,render_prz


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        inputs = ttk.Frame(self)
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

        inputs.pack(anchor="nw")

        # Average Pixel
        results = ttk.Frame(self)
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
        button_frame = ttk.Frame(self)
        open_button = ttk.Button(button_frame, text="Open Image",command=lambda: open_image())
        detect_button = ttk.Button(button_frame, text="Detect")
        save_button = ttk.Button(button_frame, text="Save Data")
        reset_button = ttk.Button(button_frame, text="Reset")
        open_button.pack(side="left", padx=10, pady=10)
        detect_button.pack(side="left", padx=10, pady=10)
        save_button.pack(side="left", padx=10, pady=10)
        reset_button.pack(side="left", padx=10, pady=10)
        button_frame.pack(anchor="nw")        
        
        
        def open_image():
            #Potentially add ability to filter by file types
            file_path = filedialog.askopenfilename()
            
            # Rendering spectrogram
            spectrogram_data = load_prz(file_path)
            spectrogram_processed=render_prz(spectrogram_data)
            figurez = Figure(figsize=(6, 4), dpi=100)
            canvas=FigureCanvasTkAgg(figurez, self)
            axis=figurez.add_subplot()
            axis.imshow(spectrogram_processed)
            axis.set_axis_off()
            canvas.draw()
            canvas.get_tk_widget().pack(side="top",anchor=tk.N)