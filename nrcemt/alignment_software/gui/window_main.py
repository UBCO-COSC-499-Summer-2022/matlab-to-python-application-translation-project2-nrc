import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from nrcemt.alignment_software.engine.file_discovery import list_file_sequence
from nrcemt.alignment_software.engine.img_loading import load_dm3
from nrcemt.alignment_software.engine.img_processing import convert_img_float64
from .frame_steps import StepsFrame
from .frame_image import ImageFrame
from .frame_sequence_selector import SequenceSelector
from .contrast.window_contrast import ContrastWindow


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("Alignment Main Window")
        self.minsize(600, 450)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        side_frame = tk.Frame()
        side_frame.grid(column=0, row=0, sticky="nswe")
        side_frame.rowconfigure(0, weight=1)
        self.steps = StepsFrame(side_frame)
        self.steps.grid(column=0, row=0, sticky="nwe")
        self.image_select = SequenceSelector(side_frame, "Image displayed")
        self.image_select.grid(column=0, row=1, sticky="swe")

        self.image_frame = ImageFrame(self)
        self.image_frame.grid(column=1, row=0)
        file_discovery = self.steps.file_discovery
        file_discovery.config(command=self.select_first_image)
        contrast_adjustment = self.steps.contrast_adjustment
        contrast_adjustment.config(state="disabled")
        contrast_adjustment.config(command=self.open_contrast_adjustment)

        self.contrast_window = None

        self.image_select.set_command(self.select_image)
        self.selected_image_index = 0
        self.selected_image = None
        self.dm3_sequence = None
        self.contrast_ranges = None

    def load_images(self):
        for filename in self.dm3_sequence:
            yield convert_img_float64(load_dm3(filename))

    def image_count(self):
        return len(self.dm3_sequence)

    def select_first_image(self):
        filename = askopenfilename(
            filetypes=[("DigitalMicrograph 3 file", ".dm3")]
        )
        if filename:
            try:
                file_sequence = list(list_file_sequence(filename))
                if len(file_sequence) < 2:
                    showerror(
                        "DM3 Load Error",
                        "there must be at least 2 images in the dm3 sequence"
                    )
                self.dm3_sequence = file_sequence
                self.image_select.set_length(len(file_sequence))
                self.image_select.set(1)
                self.select_image(1)
                self.steps.contrast_adjustment.config(state="normal")
            except Exception as e:
                showerror("DM3 Load Error", str(e))

    def select_image(self, n):
        self.selected_image_index = n - 1
        self.selected_image = convert_img_float64(
            load_dm3(self.dm3_sequence[self.selected_image_index])
        )
        self.render_image()
        if self.contrast_window is not None:
            self.contrast_window.update_image(n-1, self.selected_image)

    def update_contrast_ranges(self, contrast_ranges):
        self.contrast_ranges = contrast_ranges
        self.render_image()

    def render_image(self):
        if self.contrast_ranges is not None:
            if self.selected_image_index < len(self.contrast_ranges):
                vmin, vmax = self.contrast_ranges[self.selected_image_index]
            else:
                vmin, vmax = self.contrast_ranges[0]
        else:
            vmin, vmax = (None, None)
        self.image_frame.render_image(self.selected_image, vmin, vmax)

    def open_contrast_adjustment(self):
        if self.contrast_window is None:
            self.contrast_window = ContrastWindow(
                self, self.load_images, self.image_count
            )
            self.contrast_window.protocol(
                "WM_DELETE_WINDOW", self.close_contrast_adjustment
            )
            self.contrast_window.set_command(self.update_contrast_ranges)
            self.contrast_window.update_image(
                self.selected_image_index, self.selected_image
            )
        else:
            self.contrast_window.lift()

    def close_contrast_adjustment(self):
        self.contrast_window.destroy()
        self.contrast_window = None
