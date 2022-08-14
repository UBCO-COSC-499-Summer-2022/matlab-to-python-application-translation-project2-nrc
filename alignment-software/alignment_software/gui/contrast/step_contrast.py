import os
from tkinter.messagebox import showerror
from ..common import AsyncHandler

import numpy as np
from alignment_software.engine.csv_io import (
    read_columns_csv, write_columns_csv
)
from alignment_software.engine.img_processing import (
    adjust_img_range,
    convert_img_float64,
    reject_outliers_percentile
)
from .window_contrast import ContrastWindow


class ContrastStep:
    """Step that applies contrast adjustments."""

    def __init__(self, main_window, loading_step):
        """
        Create contrast step.
        Depends on loading step to get raw images.
        """
        self.main_window = main_window
        self.loading_step = loading_step
        self.contrast_window = None
        self.contrast_ranges = None
        self.reset()

    def open(self, close_callback):
        """Opens the step and calls close_callback when done."""
        self.contrast_window = ContrastWindow(self.main_window)

        def close():
            self.save()
            self.contrast_window.destroy()
            self.contrast_window = None
            close_callback(reset=True)

        self.contrast_window.protocol("WM_DELETE_WINDOW", close)

        self.contrast_window.tools.apply.config(
            command=self.apply_outlier_rejection
        )
        slider_handler = AsyncHandler(self.handle_sliders)
        self.contrast_window.tools.slider_min.config(
            command=slider_handler
        )
        self.contrast_window.tools.slider_max.config(
            command=slider_handler
        )

    def save(self):
        """Saves contrast ranges to transform csv."""
        transform_csv = os.path.join(
            self.loading_step.get_output_path(),
            "transform.csv"
        )
        if self.contrast_ranges is None:
            write_columns_csv(transform_csv, {
                "contrast_min": [], "contrast_max": []
            })
        else:
            write_columns_csv(transform_csv, {
                "contrast_min": self.contrast_ranges[:, 0],
                "contrast_max": self.contrast_ranges[:, 1]
            })

    def restore(self):
        """Restore from transform csv."""
        transform_csv = os.path.join(
            self.loading_step.get_output_path(),
            "transform.csv"
        )
        try:
            restored_contrast = read_columns_csv(
                transform_csv, ["contrast_min", "contrast_max"]
            )
            if len(restored_contrast["contrast_min"]) != self.image_count():
                return False
            if len(restored_contrast["contrast_min"]) != self.image_count():
                return False
            self.contrast_ranges = np.empty((self.image_count(), 2))
            self.contrast_ranges[:, 0] = restored_contrast["contrast_min"]
            self.contrast_ranges[:, 1] = restored_contrast["contrast_max"]
            return True
        except FileNotFoundError:
            return False
        except KeyError:
            return False

    def load_image(self, i):
        """Load image, either raw or contrast adjusted."""
        image = self.loading_step.load_image(i)
        image = convert_img_float64(image)
        if self.contrast_ranges is not None:
            vmin, vmax = self.contrast_ranges[i]
            image = adjust_img_range(image, vmin, vmax, 0.0, 1.0)
        return image

    def get_contrast_range(self, i):
        """Get contrast range as a tuple."""
        if self.contrast_ranges is None:
            return None, None
        else:
            return self.contrast_ranges[i]

    def image_count(self):
        """Returns the number of frames in the sequence."""
        return self.loading_step.image_count()

    def select_image(self, i):
        """Render image and update histogram."""
        raw_image = self.loading_step.load_image(i)
        float_image = convert_img_float64(raw_image)
        if self.contrast_ranges is None:
            vmin, vmax = 0.0, 1.0
        else:
            vmin, vmax = self.contrast_ranges[i]
        if self.contrast_window is not None:
            self.contrast_window.histogram.render_histogram(float_image)
            self.contrast_window.histogram.render_range(vmin, vmax)
        self.main_window.image_frame.render_image(float_image, vmin, vmax)
        self.main_window.image_frame.update()

    def reset(self):
        """Erase the contrast ranges."""
        self.contrast_ranges = None

    def is_ready(self):
        """Contrast step is ready if loading step is ready, regardless."""
        return self.loading_step.is_ready()

    def apply_outlier_rejection(self):
        """Apply percentile outlier rejection."""
        try:
            percentile = self.contrast_window.tools.percentile_var.get()
        except Exception as e:
            showerror("Contrast Error", str(e))
            return
        self.contrast_window.progress_var.set(0)
        self.contrast_window.update_idletasks()
        apply_per_image = self.contrast_window.tools.discrete_var.get()
        image_count = self.image_count()
        selected_image = self.main_window.selected_image()
        if apply_per_image:
            self.contrast_ranges = np.empty((image_count, 2))
            for i in range(image_count):
                image = self.loading_step.load_image(i)
                image = convert_img_float64(image)
                self.contrast_ranges[i] = (
                    reject_outliers_percentile(image, percentile)
                )
                self.contrast_window.progress_var.set(i / (image_count-1))
                self.contrast_window.update_idletasks()
        else:
            image = self.loading_step.load_image(selected_image)
            image = convert_img_float64(image)
            contrast_range = reject_outliers_percentile(image, percentile)
            self.contrast_ranges = np.array(image_count * [contrast_range])
        self.contrast_window.progress_var.set(1)
        self.select_image(selected_image)

    def handle_sliders(self, value):
        """Handle contrast sliders updating."""
        vmin = self.contrast_window.tools.slider_min.get()
        vmax = self.contrast_window.tools.slider_max.get()
        self.contrast_ranges = np.array(self.image_count() * [[vmin, vmax]])
        self.select_image(self.main_window.selected_image())

    def focus(self):
        """Brings the contrast window to the top."""
        self.contrast_window.lift()
