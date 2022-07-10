import pathlib
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from nrcemt.alignment_software.engine.file_discovery import (
    get_file_sequence_base,
    list_file_sequence
)
from nrcemt.alignment_software.engine.img_io import load_dm3


class LoadingStep:

    def __init__(self, main_window):
        self.main_window = main_window
        self.dm3_sequence = []

    def open(self, close_callback):
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
        return len(self.dm3_sequence)

    def load_image(self, i):
        return load_dm3(self.dm3_sequence[i])

    def select_image(self, i):
        if self.is_ready():
            image = self.load_image(i)
            self.main_window.image_frame.render_image(image, None, None)
            self.main_window.image_frame.update()

    def is_ready(self):
        return len(self.dm3_sequence) != 0

    def get_output_path(self):
        base = get_file_sequence_base(self.dm3_sequence[0])
        path = pathlib.Path(self.dm3_sequence[0])
        output_path = path.parent / (base + "output")
        output_path.mkdir(parents=True, exist_ok=True)
        return str(output_path)
