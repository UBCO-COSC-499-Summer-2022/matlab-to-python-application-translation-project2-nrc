from tkinter import ttk
from .widget_templates import TableLayout


# widgets configuration for the results
class ResultsConfiguration(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, borderwidth=5)

        # upper lens results
        lst = [("", "C1", "C2", "C3"),
               ("Lens Ur: ", 123, 123, 123),
               ("Lens Focal length:", 123, 123, 123),
               ("Lens Magification:", 123, 123, 123)]
        upper_results = TableLayout(self, lst)
        upper_results.pack(side="top", anchor="nw", pady=5)

        # lower lens results

        # condensor aperature label
        condensor = ttk.Label(self, text="Condensor Aperature = 10")
        condensor.pack(side="top", anchor="nw", pady=5)

        # magnification label
        magnification = ttk.Label(self, text="Magnification = 10")
        magnification.pack(side="top", anchor="nw", pady=5)
