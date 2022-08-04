import tkinter as tk
from tkinter import ttk
from nrcemt.qeels.engine.peak_detection import peak_detection
from nrcemt.qeels.gui.frame_canvas import CanvasFrame
from .plasmon_section import PlasmonSelect, ResultBoxes, WidthComponent
from nrcemt.qeels.engine.results import save_results
from nrcemt.qeels.engine.spectrogram import (
    load_spectrogram,
    process_spectrogram,
)

EV_VALS = (15, 15.8, 16.7, 24.8, 25, 33)
MATERIAL_OPTIONS = (
    "Aluminium (15.0 ev)", "Germanium (15.8 ev)",
    "Silicone (16.7 ev)", "Gold (24.8 ev)", "Silver (25.0 ev)",
    "Diamond (33 ev)"
)


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

        results = ttk.Frame(settings_frame)

        list_frame = ttk.Frame(results)
        ttk.Label(
            list_frame,
            text="Select a material: "
        ).pack()

        dropdown_var = tk.StringVar(value=MATERIAL_OPTIONS)

        self.material_list = tk.Listbox(
            list_frame,
            listvariable=dropdown_var,
            height=6
        )
        self.material_list.select_set(0)
        self.material_list.pack(padx=20)

        list_frame.pack(side="right")

        ttk.Label(
            results,
            text=""
        ).pack()

        # Average Pixel
        average_pixel = ResultBoxes(results, "Average Pixel")
        average_pixel.result_var.set(10)
        average_pixel.pack()

        # Micro rad/pixel upper
        rad_upper = ResultBoxes(results, "Micro rad/Pixel Upper")
        rad_upper.result_var.set(0.0380)
        rad_upper.pack()

        # Micro rad/pixel lower
        rad_lower = ResultBoxes(results, "Micro rad/Pixel Lower")
        rad_lower.result_var.set(0.0380)
        rad_lower.pack()

        # Ev/Pixel
        ev = ResultBoxes(results, "EV/Pixel")
        ev.result_var.set(0.0569)
        ev.pack()

        results.pack(anchor="nw", pady=10, padx=10)

        self.results_array.append(ev)
        self.results_array.append(rad_upper)
        self.results_array.append(rad_lower)
        self.results_array.append(average_pixel)

        # adding buttons
        button_frame = ttk.Frame(settings_frame)
        self.open_button = ttk.Button(
            button_frame, text="Open Image",
            command=self.open_image
        )
        self.detect_button = ttk.Button(
            button_frame,
            text="Detect",
            command=self.detect
        )
        self.save_button = ttk.Button(
            button_frame, text="Save Data",
            command=self.save_results
        )
        self.reset_button = ttk.Button(
            button_frame, text="Reset"
        )
        self.open_button.pack(side="left", padx=10, pady=10)
        self.detect_button.pack(side="left", padx=10, pady=10)
        self.save_button.pack(side="left", padx=10, pady=10)
        self.reset_button.pack(side="left", padx=10, pady=10)
        button_frame.pack(anchor="nw")
        settings_frame.pack(anchor='n', side="left")

        self.save_button['state'] = "disabled"
        self.detect_button['state'] = "disabled"
        self.reset_button['state'] = "disabled"

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
        file_path = tk.filedialog.askopenfilename()
        if len(file_path) != 0:
            # Rendering spectrogram
            # If error loading file, error message is displayed
            try:
                self.spectrogram_data = load_spectrogram(file_path)
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
            self.save_button['state'] = "normal"
            self.detect_button['state'] = "normal"
            self.reset_button['state'] = "normal"

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
        save_path = None

        # If image has been loaded
        save_path = tk.filedialog.asksaveasfile(
            mode='w',
            defaultextension=".csv",
            filetypes=[("CSV File", "*.csv")]
        )
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

        headers = [
            " ",
            "X1", "Y1",
            "X2", "Y2",
            "Width",
            "Results"
        ]

        data = []
        # if their is a path to save file
        if save_path is not None:
            save_path = save_path.name
            for i in range(0, 6, 2):
                row = []
                row.append(names[int(i/2)])
                row.append(self.plasmon_array[i].x_var.get())
                row.append(self.plasmon_array[i].y_var.get())
                row.append(self.plasmon_array[i+1].x_var.get())
                row.append(self.plasmon_array[i+1].y_var.get())
                row.append(self.width_array[int(i/2)].width_var.get())
                row.append(self.results_array[int(i/2)].result_var.get())
                row.append(result_names[int(i/2)])
                data.append(row)
            data.append((
                "Average Pixel",
                self.results_array[3].result_var.get()
            ))
            save_results(save_path, headers, data)

    def detect(self):
        results = []
        for items in self.results_array:
            results.append(items.result_var.get())

        plasmons = []
        for plasmon in self.plasmon_array:
            plasmons.append((plasmon.x_var.get(), plasmon.y_var.get()))

        width = []
        checkbox = []
        for item in self.width_array:
            width.append(item.width_var.get())
            checkbox.append(item.detect_var.get())

        ev = EV_VALS[self.material_list.curselection()[0]]

        result, result_image = peak_detection(
            plasmons, width,
            results, checkbox,
            self.spectrogram_data,
            ev
        )

        # setting results
        for i in range(len(result)):
            self.results_array[i].result_var.set(results[i])
        self.spectrogram_processed = process_spectrogram(result_image)
        self.canvas.render_spectrogram(self.spectrogram_processed)
