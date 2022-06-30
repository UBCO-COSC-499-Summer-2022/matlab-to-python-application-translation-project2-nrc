import os
from tkinter.messagebox import showerror, showinfo
from nrcemt.alignment_software.engine.img_io import load_float_tiff, save_float_tiff
from nrcemt.alignment_software.engine.img_processing import combine_tranforms, compute_img_shift, transform_img, translate_transform


class CoarseAlignStep:

    def __init__(self, main_window, transform_step, loading_step):
        self.main_window = main_window
        self.transform_step = transform_step
        self.loading_step = loading_step

    def open(self, close_callback):
        try:
            self.perform_alignment()
            showinfo("Coarse Alignment", "Coarse alignment completed!")
        except Exception:
            showerror("Coarse Alignment Error")
        finally:
            close_callback(reset=True)

    def perform_alignment(self):
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
            combined_tranformed = combine_tranforms(shift, transform)
            image_transformed = transform_img(image, combined_tranformed)
            self.save_image(image_transformed, i)
            self.main_window.image_select.set(i+1)
            self.main_window.update_idletasks()
            previous_image = image

    def save_image(self, image, i):
        output_path = self.loading_step.get_output_path()
        filename = f"coarse_{i+1:03d}.tiff"
        filepath = os.path.join(output_path, filename)
        save_float_tiff(filepath, image)

    def image_count(self):
        return self.transform_step.image_count()

    def select_image(self, i):
        output_path = self.loading_step.get_output_path()
        filename = f"coarse_{i+1:03d}.tiff"
        filepath = os.path.join(output_path, filename)
        image = load_float_tiff(filepath)
        self.main_window.image_frame.render_image(image, 0.0, 1.0)
