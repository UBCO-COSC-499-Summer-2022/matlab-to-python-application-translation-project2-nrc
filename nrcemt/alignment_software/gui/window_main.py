import tkinter as tk
from nrcemt.alignment_software.gui.loading.step_loading import LoadingStep
from .frame_steps import StepsFrame
from .frame_image import ImageFrame
from .frame_sequence_selector import SequenceSelector


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

        self.image_select.set_command(lambda n: self.select_image(n-1))

        self.loading_step = LoadingStep(self)
        self.current_step = None
        self.current_step_open = False

        self.steps.file_discovery.config(
            command=lambda: self.open_step(self.loading_step)
        )

    def open_step(self, step):
        # check if a nother step is currently open
        if self.current_step_open:
            return showwarning(
                "Error launching step",
                "Close the current step before opening another!"
            )
        # launch the step and set callback for when it closes
        self.current_step = step
        self.current_step_open = True
        self.current_step.open(lambda reset: self.close_step(step, reset))

    def close_step(self, step, reset):
        self.current_step_open = False

    def select_image(self, index):
        self.current_step.select_image(index)
