from tkinter import ttk
from .widget_templates import LabelLayout, FramedLabelLayout


# widgets configuration for the results
class ResultsConfiguration(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, borderwidth=5)

        # lens Ur stuff labels
        lens_ur = LabelLayout(self, "Lens Ur: ")
        lens_ur.pack(side="top", anchor="nw")

        # lens focal length labels
        lens_focal = LabelLayout(self, "Lens Focal Length: ")
        lens_focal.pack(side="top", anchor="nw")

        # lens magnification Label Frame
        lens_mag = FramedLabelLayout(self, "Lens Magnification: ")
        lens_mag.pack(side="top", anchor="nw")

        # condensor aperature label
        condensor = ttk.Label(self, text="Condensor Aperature = 10")
        condensor.pack(side="top", anchor="nw")

        # magnification label
        magnification = ttk.Label(self, text="Magnification = 10")
        magnification.pack(side="top", anchor="nw")
