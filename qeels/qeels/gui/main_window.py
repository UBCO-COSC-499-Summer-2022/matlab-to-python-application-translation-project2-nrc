import tkinter as tk
from tkinter import ttk
from nrcemt.common.gui.async_handler import AsyncHandler
from nrcemt.qeels.engine.peak_detection import peak_detection
from nrcemt.qeels.gui.frame_canvas import CanvasFrame
from .plasmon_section import PlasmonSelect, ResultBox, WidthComponent
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
        self.title("qEEls peak detection")
        self.geometry("1200x700")

        self.disable_redraw = False
        self.radio_variable = tk.IntVar()
        self.plasmon_array = []
        self.width_array = []
        self.results_array = []
        self.spectrogram_data = None
        self.spectrogram_processed = None

        settings_frame = ttk.Frame(self)
        settings_frame.pack(anchor='n', side="left")
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

        middle_frame = ttk.Frame(settings_frame)
        results = ttk.Frame(middle_frame)

        ttk.Label(
            results,
            text=""
        ).pack()

        # Average Pixel
        average_pixel = ResultBox(results, "Average Pixel", 10)
        average_pixel.pack()

        # Micro rad/pixel upper
        rad_upper = ResultBox(results, "Micro rad/Pixel Upper", 0.0380)
        rad_upper.pack()

        # Micro rad/pixel lower
        rad_lower = ResultBox(results, "Micro rad/Pixel Lower", 0.0380)
        rad_lower.pack()

        # Ev/Pixel
        ev = ResultBox(results, "EV/Pixel", 0.0569)
        ev.pack()

        results.pack(side="left", padx=10, pady=1)

        list_frame = ttk.Frame(middle_frame)

        ttk.Label(
            list_frame,
            text="Select a material: "
        ).pack()

        self.material_list = ttk.Combobox(
            list_frame,
            values=MATERIAL_OPTIONS,
            height=6,
            state="readonly"
        )
        self.material_list.current(0)
        self.material_list.pack(padx=20)

        list_frame.pack()

        self.results_array.append(ev)
        self.results_array.append(rad_upper)
        self.results_array.append(rad_lower)
        self.results_array.append(average_pixel)

        middle_frame.pack(anchor="nw")

        # adding buttons
        button_frame = ttk.Frame(settings_frame)
        button_frame.pack(anchor="nw")
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
            button_frame, text="Reset",
            command=self.reset
        )
        self.open_button.pack(side="left", padx=10, pady=10)
        self.detect_button.pack(side="left", padx=10, pady=10)
        self.save_button.pack(side="left", padx=10, pady=10)
        self.reset_button.pack(side="left", padx=10, pady=10)
        self.save_button['state'] = "disabled"
        self.detect_button['state'] = "disabled"
        self.reset_button['state'] = "disabled"

        contrast_frame = tk.Frame(settings_frame)
        contrast_frame.pack(anchor="nw")
        contrast_min_label = ttk.Label(contrast_frame, text="Constrast Min: ")
        contrast_min_label.grid(row=0, column=0)
        contrast_max_label = ttk.Label(contrast_frame, text="Constrast Max: ")
        contrast_max_label.grid(row=1, column=0)
        self.contrast_min_scale = ttk.Scale(
            contrast_frame, length=300, value=0,
            command=AsyncHandler(lambda x: self.redraw_canvas())
        )
        self.contrast_min_scale.grid(row=0, column=1)
        self.contrast_max_scale = ttk.Scale(
            contrast_frame, length=300, value=1,
            command=AsyncHandler(lambda x: self.redraw_canvas())
        )
        self.contrast_max_scale.grid(row=1, column=1)

        # Adding frame to window
        self.spectrogram_frame.pack(side="left", anchor='n')

        for plasmon in self.plasmon_array:
            plasmon.x.set_command(self.redraw_canvas)
            plasmon.y.set_command(self.redraw_canvas)

        for width in self.width_array:
            width.width.set_command(self.redraw_canvas)

    def canvas_click(self, x, y):
        x = int(x)
        y = int(y)
        selected_plasmon = self.plasmon_array[self.radio_variable.get()]
        selected_plasmon.x.set(x)
        selected_plasmon.y.set(y)
        row = int(self.radio_variable.get()/2)

        x1 = self.plasmon_array[row*2].x.get()
        y1 = self.plasmon_array[row*2].y.get()
        x2 = self.plasmon_array[row*2+1].x.get()
        y2 = self.plasmon_array[row*2+1].y.get()

        if all([x1, y1, x2, y2]):
            self.width_array[row].detect.set(True)

        self.redraw_canvas()

    def redraw_canvas(self):
        if self.spectrogram_processed is None:
            return

        if self.disable_redraw:
            return

        self.canvas.render_spectrogram(
            self.spectrogram_processed,
            self.contrast_min_scale.get(),
            self.contrast_max_scale.get()
        )
        for plasmon in self.plasmon_array:
            x = plasmon.x.get()
            y = plasmon.y.get()
            if x != 0 or y != 0:
                self.canvas.render_point(x, y, int(plasmon.radio_value/2)+1)
        self.draw_rect()
        self.canvas.update()

    def open_image(self):
        # Potentially add ability to filter by file types
        file_path = tk.filedialog.askopenfilename(
            filetypes=[("Prz File", "*.prz")]
        )
        if len(file_path) != 0:
            # Rendering spectrogram
            # If error loading file, error message is displayed
            try:
                self.spectrogram_data = load_spectrogram(file_path)
            except Exception as e:
                tk.messagebox.showerror(
                    title="Error",
                    message=(
                        "Something went wrong loading the spectrogram."
                        + "\n Please try again!"
                    ),
                )
                print(str(e))
                return

            # Processing spectrogram data
            self.spectrogram_processed = process_spectrogram(
                self.spectrogram_data
            )
            height, width = self.spectrogram_processed.shape
            for plasmon in self.plasmon_array:
                plasmon.set_image_size(width, height)
            self.reset()
            self.save_button['state'] = "normal"
            self.detect_button['state'] = "normal"
            self.reset_button['state'] = "normal"

    def draw_rect(self):
        for i in range(0, 6, 2):
            plasmon_1 = None
            plasmon_2 = None
            completed_1 = (
                self.plasmon_array[i].x.get() != 0 or
                self.plasmon_array[i].y.get() != 0
            )
            completed_2 = (
                self.plasmon_array[i+1].x.get() != 0 or
                self.plasmon_array[i+1].y.get() != 0
            )
            if completed_1 and completed_2:
                plasmon_1 = (
                    self.plasmon_array[i].x.get(),
                    self.plasmon_array[i].y.get()
                )
                plasmon_2 = (
                    self.plasmon_array[i+1].x.get(),
                    self.plasmon_array[i+1].y.get()
                )
            box_width = self.width_array[int(i/2)].width.get()
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
                row.append(self.plasmon_array[i].x.get())
                row.append(self.plasmon_array[i].y.get())
                row.append(self.plasmon_array[i+1].x.get())
                row.append(self.plasmon_array[i+1].y.get())
                row.append(self.width_array[int(i/2)].width.get())
                row.append(self.results_array[int(i/2)].result.get())
                row.append(result_names[int(i/2)])
                data.append(row)
            data.append((
                "Average Pixel",
                self.results_array[3].result.get()
            ))
            save_results(save_path, headers, data)

    def detect(self):
        results = []
        for items in self.results_array:
            results.append(items.result.get())

        plasmons = []
        for plasmon in self.plasmon_array:
            plasmons.append((plasmon.x.get(), plasmon.y.get()))

        width = []
        checkbox = []
        for item in self.width_array:
            width.append(item.width.get())
            checkbox.append(item.detect.get())

        ev = EV_VALS[self.material_list.current()]

        result, result_image = peak_detection(
            plasmons, width,
            results, checkbox,
            self.spectrogram_data,
            ev
        )

        # setting results
        for i in range(len(result)):
            self.results_array[i].result.set(results[i])
        self.spectrogram_processed = process_spectrogram(result_image)
        self.canvas.render_spectrogram(
            self.spectrogram_processed,
            self.contrast_min_scale.get(),
            self.contrast_max_scale.get()
        )

    def reset(self):
        self.disable_redraw = True
        # Reset entry boxes
        for entry in self.plasmon_array:
            entry.x.set(0)
            entry.y.set(0)

        # reset widths
        for width in self.width_array:
            width.width.set(60)
            width.detect.set(False)

        # Reset result boxes
        self.results_array[0].result.set(0.0569)
        self.results_array[1].result.set(0.038)
        self.results_array[2].result.set(0.038)
        self.results_array[3].result.set(10)

        # radio button
        self.radio_variable.set(0)

        # listbox
        self.material_list.current(0)

        # re-do spectrogram
        self.spectrogram_processed = process_spectrogram(self.spectrogram_data)

        # Reset contrast adjustment
        self.contrast_min_scale.set(0)
        self.contrast_max_scale.set(1)
        self.disable_redraw = False

        self.redraw_canvas()
