from tkinter import ttk
from nrcemt.alignment_software.gui.frames.file_discovery_frame import FileDiscoveryFrame
from nrcemt.alignment_software.gui.frames.contrast_adjustment_frame import ContrastAdjustmentFrame
from nrcemt.alignment_software.gui.frames.image_adjustment_frame import ImageAdjustmentFrame
from nrcemt.alignment_software.gui.frames.coarse_alignment_frame import CoarseAlignmentFrame
from nrcemt.alignment_software.gui.frames.auto_detection_frame import AutoDetectionFrame
from nrcemt.alignment_software.gui.frames.manual_detection_frame import ManualDetectionFrame
from nrcemt.alignment_software.gui.frames.optimization_frame import OptimizationFrame
from nrcemt.alignment_software.gui.frames.image_slider_frame import ImageSliderFrame


class ToolFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.__create_widgets()

    def __create_widgets(self):
        self.file_discovery = FileDiscoveryFrame(self)
        self.file_discovery.grid(column=0, row=0)
        self.contrast_adjustment = ContrastAdjustmentFrame(self)
        self.contrast_adjustment.grid(column=0, row=1)
        self.image_properties = ImageAdjustmentFrame(self)
        self.image_properties.grid(column=0, row=2)
        self.contrast_adjustment = CoarseAlignmentFrame(self)
        self.contrast_adjustment.grid(column=0, row=3)
        self.contrast_adjustment = AutoDetectionFrame(self)
        self.contrast_adjustment.grid(column=0, row=4)
        self.contrast_adjustment = ManualDetectionFrame(self)
        self.contrast_adjustment.grid(column=0, row=5)
        self.contrast_adjustment = OptimizationFrame(self)
        self.contrast_adjustment.grid(column=0, row=6)
        self.contrast_adjustment = ImageSliderFrame(self)
        self.contrast_adjustment.grid(column=0, row=7)
        
