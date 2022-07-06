import tkinter as tk
from tkinter import ttk
from nrcemt.qeels.gui.frame_canvas import CanvasFrame
from .plasmon_section import PlasmonSelect, ResultBoxes, WidthComponent
from nrcemt.qeels.engine.spectrogram import (
    load_spectrogram,
    process_spectrogram,
)
from nrcemt.qeels.engine.results import save_results


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        # Creating variables for the ui
        self.radio_variable = tk.IntVar()
        self.plasmon_array = []
        self.width_array = []
        self.results_array = []
        settings_frame = ttk.Frame()
        self.spectrogram_data = None
        self.spectrogram_processed = None
        inputs = ttk.Frame(settings_frame)
        self.file_path = None
    
        # Bulk Plasmons
        self.bulk_plasmon1 = PlasmonSelect(
            inputs, "Bulk Plasmon 1",
            self.radio_variable, 0
        )
        self.plasmon_array.append(self.bulk_plasmon1)
        self.bulk_plasmon2 = PlasmonSelect(
            inputs, "Bulk Plasmon 2",
            self.radio_variable, 1
        )
        self.plasmon_array.append(self.bulk_plasmon2)

        self.bulk_width = WidthComponent(inputs)
        self.bulk_plasmon1.grid(row=0, column=0, padx=2, pady=2)
        self.bulk_plasmon2.grid(row=0, column=1, padx=2, pady=2)
        self.bulk_width.grid(row=0, column=2, padx=2, pady=2, sticky="s")
        self.width_array.append(self.bulk_width)

        # Surface Plasmon Upper
        self.upper_plasmon1 = PlasmonSelect(
            inputs, "Surface Plasmon Upper 1",
            self.radio_variable, 2
        )

        self.plasmon_array.append(self.upper_plasmon1)

        self.upper_plasmon2 = PlasmonSelect(
            inputs, "Surface Plasmon Upper 2",
            self.radio_variable, 3
        )
        self.plasmon_array.append(self.upper_plasmon2)

        self.upper_width = WidthComponent(inputs)
        self.upper_plasmon1.grid(row=1, column=0, padx=2, pady=2)
        self.upper_plasmon2.grid(row=1, column=1, padx=2, pady=2)
        self.upper_width.grid(row=1, column=2, padx=2, pady=2, sticky="s")
        self.width_array.append(self.upper_width)

        # Surface Plasmon Lower
        self.lower_plasmon1 = PlasmonSelect(
            inputs, "Surface Plasmon Lower 1",
            self.radio_variable, 4
        )
        self.plasmon_array.append(self.lower_plasmon1)

        self.lower_plasmon2 = PlasmonSelect(
            inputs, "Surface Plasmon Lower 2",
            self.radio_variable, 5
        )
        self.plasmon_array.append(self.lower_plasmon2)

        self.lower_width = WidthComponent(inputs)
        self.lower_plasmon1.grid(row=2, column=0, padx=2, pady=2)
        self.lower_plasmon2.grid(row=2, column=1, padx=2, pady=2)
        self.lower_width.grid(row=2, column=2, padx=2, pady=2, sticky="s")
        self.width_array.append(self.lower_width)

        inputs.pack(anchor="w")

        self.spectrogram_frame = ttk.Frame()

        # Create the canvas
        self.canvas = CanvasFrame(
            self.spectrogram_frame,
            self.canvas_click
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

        self.results_array.append(ev)
        self.results_array.append(rad_upper)
        self.results_array.append(rad_lower)
        self.results_array.append(average_pixel)

        # adding buttons
        button_frame = ttk.Frame(settings_frame)
        open_button = ttk.Button(
            button_frame, text="Open Image",
            command=self.open_image
        )
        detect_button = ttk.Button(button_frame, text="Detect")
        save_button = ttk.Button(
            button_frame, text="Save Data",
            command=self.save_results
        )
        reset_button = ttk.Button(
            button_frame, text="Reset"
        )
        open_button.pack(side="left", padx=10, pady=10)
        detect_button.pack(side="left", padx=10, pady=10)
        save_button.pack(side="left", padx=10, pady=10)
        reset_button.pack(side="left", padx=10, pady=10)
        button_frame.pack(anchor="nw")
        settings_frame.pack(anchor='n', side="left")

        # Adding frame to window
        self.spectrogram_frame.pack(side="left", anchor='n')

        for plasmon in self.plasmon_array:
            plasmon.x_var.trace('w', lambda a, b, c: self.redraw_canvas())
            plasmon.y_var.trace('w', lambda a, b, c: self.redraw_canvas())

        for width in self.width_array:
            width.width_var.trace('w', lambda a, b, c: self.redraw_canvas())

    def canvas_click(self, x, y):
        x = int(x)
        y = int(y)
        selected_plasmon = self.plasmon_array[self.radio_variable.get()]
        selected_plasmon.x_var.set(x)
        selected_plasmon.y_var.set(y)

    def redraw_canvas(self):
        if self.spectrogram_processed is None:
            return
        self.canvas.render_spectrogram(self.spectrogram_processed)
        for plasmon in self.plasmon_array:
            try:
                x = plasmon.x_var.get()
                y = plasmon.y_var.get()
            except Exception:
                continue
            if x != 0 or y != 0:
                self.canvas.render_point(x, y, int(plasmon.radio_value/2)+1)
        self.draw_rect()
        self.canvas.update()

    def open_image(self):
        # Potentially add ability to filter by file types
        self.file_path = tk.filedialog.askopenfilename()
        if len(self.file_path) != 0:
            # Rendering spectrogram
            # If error loading file, error message is displayed
            try:
                self.spectrogram_data = load_spectrogram(self.file_path)
            except Exception:
                tk.messagebox.showerror(
                    title="Error",
                    message=(
                        "Something went wrong loading the spectrogram."
                        + "\n Please try again!"
                    ),
                )
                return

            # Processing spectrogram data
            self.spectrogram_processed = process_spectrogram(
                self.spectrogram_data
            )
            self.canvas.render_spectrogram(self.spectrogram_processed)

    def draw_rect(self):
        for i in range(0, 6, 2):
            plasmon_1 = None
            plasmon_2 = None
            try:
                completed_1 = (
                    self.plasmon_array[i].x_var.get() != 0 or
                    self.plasmon_array[i].y_var.get() != 0
                )
                completed_2 = (
                    self.plasmon_array[i+1].x_var.get() != 0 or
                    self.plasmon_array[i+1].y_var.get() != 0
                )
                if completed_1 and completed_2:
                    plasmon_1 = (
                        self.plasmon_array[i].x_var.get(),
                        self.plasmon_array[i].y_var.get()
                    )
                    plasmon_2 = (
                        self.plasmon_array[i+1].x_var.get(),
                        self.plasmon_array[i+1].y_var.get()
                    )
                box_width = self.width_array[int(i/2)].width_var.get()

            except Exception:
                continue
            if plasmon_1 is not None and plasmon_2 is not None:
                self.canvas.render_rect(
                    plasmon_1, plasmon_2,
                    box_width
                )

    def save_results(self):
        data = []
        # ANY REASONN TO CUSTOMIZE SAVE LOCATION????
        names = [
            "Bulk Plasmon",
            "Surface Plasmon Upper",
            "Surface Plasmon Lower"
        ]
        result_names = [
            "ev/Pixel",
            "micro rad/Pixel Upper",
            "micro rad/Pixel Lower"
        ]
        if self.file_path is not None:
            for i in range(0, 6, 2):
                row = []
                row.append(names[int(i/2)])
                row.append(self.plasmon_array[i].x_var.get())
                row.append(self.plasmon_array[i].y_var.get())
                row.append(self.plasmon_array[i+1].x_var.get())
                row.append(self.plasmon_array[i+1].y_var.get())
                row.append(self.width_array[int(i/2)].width_var.get())
                row.append(self.results_array[int(i/2)].result_var.get())
                data.append(row)

            save_results(self.file_path, data)
