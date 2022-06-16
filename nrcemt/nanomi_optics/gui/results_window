from tkinter import ttk
from .widget_templates import LabelLayout


# widgets configuration for the results
class ResultsConfiguration(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, borderwidth=5)

        # lens Ur stuff
        lens_ur = LabelLayout(self, "Lens Ur: ")
        lens_ur.pack(side="top", anchor="nw")

        # lens focal length
        lens_focal = LabelLayout(self, "Lens Focal Length: ")
        lens_focal.pack(side="top", anchor="nw")

        # lens magnification

        # condensor aperature
        condensor = ttk.Label(self, text="Condensor Aperature = 10", width=10)
        condensor.pack(side="top")

        # magnification
        magnification = ttk.Label(self, text="Magnification = 10", width=10)
        magnification.pack(side="top")
