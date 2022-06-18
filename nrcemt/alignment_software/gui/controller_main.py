from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from nrcemt.alignment_software.engine.file_discovery import list_file_sequence


class MainController:

    def __init__(self, main_window):

        file_discovery = main_window.steps.file_discovery
        file_discovery.config(command=self.select_first_image)

        self.image_select = main_window.image_select

        self.dm3_sequence = None

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
                self.image_select.set(1)
                self.image_select.set_length(len(file_sequence))
            except Exception as e:
                showerror("DM3 Load Error", str(e))
