import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror 
from .frame_contrast_tool import ContrastToolFrame
from .frame_histogram import HistogramFrame
from nrcemt.alignment_software.engine.img_processing import (
    reject_outliers_percentile
)


class ContrastWindow(tk.Toplevel):

    def __init__(self, master, request_images, request_image_count):
        super().__init__(master)
        self.command = None
        self.contrast_ranges = None
        self.selected_image = None
        self.selected_image_index = 0
        self.request_images = request_images
        self.request_image_count = request_image_count
        self.geometry("700x360")
        self.title("Contrast Adjustment Window")
        self.minsize(700, 360)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.tools = ContrastToolFrame(self)
        self.tools.grid(row=0, column=0, sticky="w")
        self.tools.apply.config(command=self.apply_outlier_rejection)
        self.histogram = HistogramFrame(self)
        self.histogram.grid(row=1, column=0, sticky="nswe")
        self.progress_var = tk.DoubleVar(value=0.0)
        progress = ttk.Progressbar(
            self, orient="horizontal", variable=self.progress_var, max=1.0
        )
        progress.grid(row=2, column=0, sticky="we")

    def set_command(self, command):
        self.command = command

    def update_image(self, index, img):
        self.selected_image_index = index
        self.selected_image = img
        self.histogram.render_histogram(img)
        self.update_range()

    def update_range(self):
        if self.contrast_ranges is None:
            return
        elif self.selected_image_index < len(self.contrast_ranges):
            vmin, vmax = self.contrast_ranges[self.selected_image_index]
        else:
            vmin, vmax = self.contrast_ranges[0]
        self.histogram.render_range(vmin, vmax)

    def apply_outlier_rejection(self):
        self.contrast_ranges = []
        try:
            percentile = self.tools.percentile_var.get()
        except Exception as e:
            showerror("Contrast Error", str(e))
            return
        self.progress_var.set(0)
        self.update_idletasks()
        if self.tools.discrete_var.get():
            image_count = self.request_image_count()
            for i, img in enumerate(self.request_images()):
                self.contrast_ranges.append(
                    reject_outliers_percentile(img, percentile)
                )
                self.progress_var.set(i / (image_count-1))
                self.update_idletasks()
        else:
            self.contrast_ranges.append(
                reject_outliers_percentile(self.selected_image, percentile)
            )
        self.progress_var.set(1)
        self.update_range()
        if self.command is not None:
            self.command(self.contrast_ranges)
