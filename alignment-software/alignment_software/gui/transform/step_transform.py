import os
from alignment_software.engine.csv_io import (
    read_columns_csv, write_columns_csv
)
from alignment_software.engine.img_processing import (
    no_transform,
    resize_img,
    combine_tranforms,
    rotate_transform,
    scale_transform,
    transform_img,
    translate_transform
)
from ..common import AsyncHandler
from .window_transform import TransformWindow


class TransformStep:
    """Step that handles handles bulk transforms to the image sequence."""

    def __init__(self, main_window, loading_step, contrast_step):
        """
        Create the transform step.
        Depends on loading step to get the output path.
        Depends on contrast step to get contrast adjusted images.
        """
        self.main_window = main_window
        self.loading_step = loading_step
        self.contrast_step = contrast_step
        self.transform_window = None
        self.transform = {
            "offset_x": 0,
            "offset_y": 0,
            "angle": 0,
            "scale": 1,
            "binning": 1,
            "sobel": False
        }

    def open(self, close_callback):
        """Opens the step and calls close_callback when done."""

        # Create transform window and register handlers
        self.transform_window = TransformWindow(self.main_window)
        self.transform_window.set_command(AsyncHandler(self.update_transform))
        self.transform_window.set_transform(self.transform)

        def close():
            self.save()
            self.transform_window.destroy()
            self.transform_window = None
            close_callback(reset=True)

        self.transform_window.protocol("WM_DELETE_WINDOW", close)

    def save(self):
        """Save the transformation configuration to csv."""
        transform_csv = os.path.join(
            self.loading_step.get_output_path(),
            "transform.csv"
        )
        image_count = self.image_count()

        write_columns_csv(transform_csv, {
            "transform_x": [self.transform["offset_x"]] * image_count,
            "transform_y": [self.transform["offset_y"]] * image_count,
            "transform_angle": [self.transform["angle"]] * image_count,
            "transform_scale": [self.transform["scale"]] * image_count,
            "transform_binning": [self.transform["binning"]] * image_count
        })

    def restore(self):
        """Restore the transformation from csv."""
        transform_csv = os.path.join(
            self.loading_step.get_output_path(),
            "transform.csv"
        )
        try:
            restored_transform = read_columns_csv(
                transform_csv,
                [
                    "transform_x", "transform_y", "transform_angle",
                    "transform_scale", "transform_binning"
                ]
            )
            self.transform = {
                "offset_x": restored_transform["transform_x"][0],
                "offset_y": restored_transform["transform_y"][0],
                "angle": restored_transform["transform_angle"][0],
                "scale": restored_transform["transform_scale"][0],
                "binning": restored_transform["transform_binning"][0],
                "sobel": False
            }
            return True
        except FileNotFoundError:
            return False
        except KeyError:
            return False

    def load_image(self, i):
        """Gets the resized image with a given index."""
        image = self.contrast_step.load_image(i)
        image = resize_img(image, 1 / self.transform['binning'])
        return image

    def image_count(self):
        """Returns the number of frames in the sequence."""
        return self.contrast_step.image_count()

    def select_image(self, i):
        """Displays the transformed preview of with a given index."""
        image = self.load_image(i)
        transform = self.get_transform(i)
        image = transform_img(image, transform)
        self.main_window.image_frame.render_image(image)
        self.main_window.image_frame.update()

    def update_transform(self):
        """Handle transform update."""
        self.transform = self.transform_window.get_tranform()
        self.select_image(self.main_window.selected_image())

    def get_transform(self, i, image_size=None):
        """Return the combined affine transform."""
        if self.transform is None:
            return no_transform()
        if image_size is None:
            height, width = self.load_image(i).shape
        else:
            width, height = image_size
        center_x = width / 2
        center_y = height / 2
        offset_x = self.transform['offset_x'] * width
        offset_y = self.transform['offset_y'] * height
        translation = translate_transform(offset_x, offset_y)
        scale = scale_transform(self.transform['scale'], center_x, center_y)
        rotate = rotate_transform(self.transform['angle'], center_x, center_y)
        return combine_tranforms(scale, rotate, translation)

    def get_binning_factor(self):
        """Returns the binning factor, for other steps."""
        return self.transform["binning"]

    def is_ready(self):
        """Returns the binning factor, for other steps."""
        return self.contrast_step.is_ready()

    def focus(self):
        """Brings the transform window to the top."""
        self.transform_window.lift()
