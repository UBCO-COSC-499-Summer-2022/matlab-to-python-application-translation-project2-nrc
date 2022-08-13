import pathlib
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from alignment_software.engine.file_discovery import (
    get_file_sequence_base,
    list_file_sequence
)
from alignment_software.engine.img_io import load_dm3


class LoadingStep:
    """Step that loads a dm3 iamge sequence."""

    def __init__(self, main_window):
        self.main_window = main_window
        self.dm3_sequence = []

    def open(self, close_callback):
        """Opens a file dialog prompt to select the first image."""

        filename = askopenfilename(
            filetypes=[("DigitalMicrograph 3 file", ".dm3")]
        )
        if not filename:
            close_callback(reset=False)
        else:
            try:
                file_sequence = list(list_file_sequence(filename))
            except Exception as e:
                showerror("DM3 Load Error", str(e))
                return close_callback(reset=False)
            if len(file_sequence) < 2:
                showerror(
                    "DM3 Load Error",
                    "there must be at least 2 images in the dm3 sequence"
                )
            self.dm3_sequence = file_sequence
            self.main_window.image_select.set_length(len(file_sequence))
            self.main_window.image_select.set(1)
            close_callback(reset=True)

    def image_count(self):
        """Returns the number of frames in the sequence."""
        return len(self.dm3_sequence)

    def load_image(self, i):
        """Loads the image from the dm3 file."""
        return load_dm3(self.dm3_sequence[i])

    def get_path(self, i):
        """Gets the path of the dm3 file with specified index."""
        return self.dm3_sequence[i]

    def select_image(self, i):
        """Displays the image if loaded."""
        if self.is_ready():
            image = self.load_image(i)
            self.main_window.image_frame.render_image(image, None, None)
            self.main_window.image_frame.update()

    def is_ready(self):
        """Returns whether dm3 sequence has been loaded."""
        return len(self.dm3_sequence) != 0

    def get_output_path(self):
        """
        Returns the location that subsequent steps should save to.
        For example "dir/image_001.dm3" -> "dir/image_output"
        """
        base = get_file_sequence_base(self.dm3_sequence[0])
        path = pathlib.Path(self.dm3_sequence[0])
        output_path = path.parent / (base + "output")
        output_path.mkdir(parents=True, exist_ok=True)
        return str(output_path)
