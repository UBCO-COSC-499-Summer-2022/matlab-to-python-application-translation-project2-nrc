import tkinter as tk
from tkinter.messagebox import showwarning
from nrcemt.alignment_software.gui.auto_track.step_auto_track import AutoTrackStep

from nrcemt.common.gui.async_handler import AsyncHandler
from .contrast.step_contrast import ContrastStep
from .loading.step_loading import LoadingStep
from .transform.step_transform import TransformStep
from .coarse_align.step_coarse_align import CoarseAlignStep
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

        self.image_select.set_command(AsyncHandler(
            lambda n: self.select_image(n-1)
        ))

        self.image_frame.set_click_command(self.canvas_click)

        self.loading_step = LoadingStep(self)
        self.contrast_step = ContrastStep(self, self.loading_step)
        self.transform_step = TransformStep(self, self.contrast_step)
        self.coarse_align_step = CoarseAlignStep(
            self, self.transform_step, self.loading_step
        )
        self.auto_track_step = AutoTrackStep(self, self.coarse_align_step)
        self.current_step = None
        self.current_step_open = False

        self.steps.load_button.config(
            command=lambda: self.open_step(self.loading_step)
        )
        self.steps.contrast_button.config(
            command=lambda: self.open_step(self.contrast_step)
        )
        self.steps.transform_button.config(
            command=lambda: self.open_step(self.transform_step)
        )
        self.steps.coarse_align_button.config(
            command=lambda: self.open_step(self.coarse_align_step)
        )
        self.steps.auto_track_button.config(
            command=lambda: self.open_step(self.auto_track_step)
        )

        self.update_step_button_states()

    def open_step(self, step):
        # check if a nother step is currently open
        if self.current_step_open:
            return showwarning(
                "Error launching step",
                "Finish the current step before opening another!"
            )
        # launch the step and set callback for when it closes
        self.current_step = step
        self.current_step_open = True
        self.current_step.open(lambda reset: self.close_step(step, reset))
        self.select_image(self.selected_image())

    def close_step(self, step, reset):
        self.current_step_open = False
        if reset and step == self.loading_step:
            self.contrast_step.reset()
            self.transform_step.reset()
        self.update_step_button_states()

    def update_step_button_states(self):
        self.steps.contrast_button.config(
            state="normal" if self.loading_step.is_ready() else "disabled"
        )
        self.steps.transform_button.config(
            state="normal" if self.loading_step.is_ready() else "disabled"
        )
        self.steps.coarse_align_button.config(
            state="normal" if self.loading_step.is_ready() else "disabled"
        )
        self.steps.auto_track_button.config(
            state="normal" if self.coarse_align_step.is_ready() else "disabled"
        )

    def canvas_click(self, x, y):
        if self.current_step is not None:
            if hasattr(self.current_step, 'canvas_click'):
                self.current_step.canvas_click(x, y)

    def select_image(self, index):
        self.current_step.select_image(index)

    def selected_image(self):
        return self.image_select.get()-1
