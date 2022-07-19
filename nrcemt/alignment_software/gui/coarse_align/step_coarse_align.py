import os
from tkinter.messagebox import showerror, showinfo
from nrcemt.alignment_software.engine.img_io import (
    load_float_tiff,
    save_float_tiff
)
from nrcemt.alignment_software.engine.img_processing import (
    combine_tranforms,
    compute_img_shift,
    transform_img,
    translate_transform
)


class CoarseAlignStep:

    def __init__(self, main_window, loading_step, transform_step):
        self.main_window = main_window
        self.transform_step = transform_step
        self.loading_step = loading_step
        self.aligned_count = 0

    def open(self, close_callback):
        self.aligned_count = 0
        self.perform_alignment(close_callback)

    def perform_alignment(self, close_callback):
        try:
            previous_image = None
            total_x_shift = 0
            total_y_shift = 0
            for i in range(self.image_count()):
                image = self.transform_step.load_image(i)
                if previous_image is not None:
                    x_shift, y_shift = compute_img_shift(previous_image, image)
                    total_x_shift += x_shift
                    total_y_shift += y_shift
                shift = translate_transform(total_x_shift, total_y_shift)
                transform = self.transform_step.get_transform(i)
                # transform from the previous step and the shift are combined
                # and applied in one go to avoid accidentally clipping the
                # edges of the images.
                combined_tranformed = combine_tranforms(shift, transform)
                image_transformed = transform_img(image, combined_tranformed)
                self.save_image(image_transformed, i)
                self.aligned_count = i + 1
                self.main_window.image_select.set(i+1)
                self.main_window.update()
                previous_image = image
            showinfo("Coarse Alignment", "Coarse Alignment Completed!")
            self.main_window.image_select.set(1)
        except Exception as e:
            showerror("Coarse Alignment Error", str(e))
        finally:
            close_callback(reset=True)

    def save_image(self, image, i):
        # files are asved to disk here to because computing the image shift is
        # and expensive operation. Don't want to do it continuously.
        output_path = self.loading_step.get_output_path()
        filename = f"coarse_{i+1:03d}.tiff"
        filepath = os.path.join(output_path, filename)
        save_float_tiff(filepath, image)

    def image_count(self):
        return self.transform_step.image_count()

    def load_image(self, i):
        # load from the files saved by save_image
        output_path = self.loading_step.get_output_path()
        filename = f"coarse_{i+1:03d}.tiff"
        filepath = os.path.join(output_path, filename)
        return load_float_tiff(filepath)

    def select_image(self, i):
        if i < self.aligned_count:
            image = self.load_image(i)
            self.main_window.image_frame.render_image(image)
            self.main_window.image_frame.update()

    def is_ready(self):
        image_count = self.image_count()
        return self.aligned_count == image_count and image_count > 0
