from tkinter.messagebox import showerror
import numpy as np
from nrcemt.alignment_software.engine.img_processing import combine_tranforms, rotate_transform, scale_transform, transform_img, translate_transform

from nrcemt.alignment_software.engine.optimization import (
    compute_marker_shifts,
    compute_transformed_shift,
    normalize_marker_data,
    optimize_magnification_and_rotation,
    optimize_particle_model,
    optimize_tilt_angles,
    optimize_x_shift
)
from .window_optimization import OptimizationWindow


class OptimizationStep:

    def __init__(
        self, main_window, loading_step, transform_step,
        coarse_align_step, auto_track_step
    ):
        self.main_window = main_window
        self.loading_step = loading_step
        self.transform_step = transform_step
        self.coarse_align_step = coarse_align_step
        self.auto_track_step = auto_track_step

    def open(self, close_callback):
        self.optimization_window = OptimizationWindow(self.main_window)

        def close():
            self.optimization_window.destroy()
            self.optimization_window = None
            close_callback(reset=True)

        self.optimization_window.protocol("WM_DELETE_WINDOW", close)

        self.optimization_window.optimize_button.config(
            command=self.perform_optimization
        )

    def load_image(self, i):
        image = self.loading_step.load_image(i)
        return image

    def image_count(self):
        return self.loading_step.image_count()

    def select_image(self, i):
        image = self.loading_step.load_image(i)
        self.main_window.image_frame.render_image(image, None, None)
        self.main_window.image_frame.update()

    def perform_optimization(self):
        tilt_mode = self.optimization_window.settings.tilt_var.get()
        if tilt_mode == "csv":
            raise NotImplementedError()
        elif tilt_mode == "constant":
            step = self.optimization_window.settings.step_angle_input.get()
            tilt = np.arange(self.image_count()) * step
        if self.optimization_window.operations.azimuth_var.get():
            phai = None
            fixed_phai = False
        else:
            phai = 0
            fixed_phai = True
        opmode = self.optimization_window.operations.operation_var.get()
        if opmode == "fixrot-fixmag":
            alpha = self.optimization_window.operations.input_angle.get()
        else:
            alpha = None
        if opmode == "onerot-fixmag":
            group_rotation = False
            group_magnification = False
        if opmode == "onerot-groupmag":
            group_rotation = False
            group_magnification = True
        if opmode == "grouprot-groupmag":
            group_rotation = True
            group_magnification = True
        markers = self.auto_track_step.get_marker_data()
        normalized_markers = normalize_marker_data(markers)
        x, y, z, alpha, phai = optimize_particle_model(
            normalized_markers, tilt, phai, alpha
        )
        if opmode == "fixrot-fixmag":
            magnification = 1
        else:
            magnification, alpha, phai = optimize_magnification_and_rotation(
                normalized_markers, x, y, z, tilt, alpha, phai,
                fixed_phai, group_rotation, group_magnification
            )
        if self.optimization_window.operations.tilt_group_var.get():
            tilt = optimize_tilt_angles(
                normalized_markers,
                x, y, z, tilt, alpha, phai, magnification
            )
        image = self.loading_step.load_image(0)
        height, width = image.shape
        shifts = compute_marker_shifts(markers, (width, height))
        x_shift = shifts[:, 0]
        y_shift = shifts[:, 1]
        x_shift, y_shift = compute_transformed_shift(
            x_shift, y_shift, alpha, magnification
        )
        x_shift = optimize_x_shift(x_shift, tilt)
        magnification = np.ones(self.image_count()) * magnification
        alpha = np.ones(self.image_count()) * alpha
        try:
            self.optimization_window.withdraw()
            for i in range(self.image_count()):
                image = self.loading_step.load_image(i)
                transform_matrix = self.transform_step.get_transform(
                    i, (width, height)
                )
                coarse_matrix = self.coarse_align_step.get_transform(
                    i, self.transform_step.get_binning_factor()
                )
                optimization_transform = combine_tranforms(
                    scale_transform(magnification[i], width/2, height/2),
                    rotate_transform(-alpha[i], width/2, height/2),
                    translate_transform(x_shift[i],  y_shift[i])
                )
                m = combine_tranforms(transform_matrix, coarse_matrix, optimization_transform)
                image = transform_img(image, m, image.mean())
                self.main_window.image_frame.render_image(image, None, None)
                self.main_window.image_frame.update()
                self.main_window.update()
        except Exception as e:
            showerror("Optimized Alignment Error", str(e))
        finally:
            self.optimization_window.deiconify()
