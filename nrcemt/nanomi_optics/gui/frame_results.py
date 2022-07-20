from tkinter import ttk
from .widget_templates import TableLayout

PAD_Y = 5


# widget layout for the results
class ResultsFrame(ttk.LabelFrame):

    def __init__(self, master):
        super().__init__(master, text="Results", borderwidth=5)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        # upper lens results
        upper_data = [("", "C1", "C2", "C3"),
                      ("Lens Ur: ", 123.123, 123.123, 123.123),
                      ("Lens Focal length:", 123.123, 123.123, 123.123),
                      ("Lens Magification:", 123.123, 123.123, 123.123)]
        upper_results = TableLayout(self, upper_data)
        upper_results.grid(row=0, column=0, sticky="e")

        # lower lens results
        lower_data = [("", "Objective", "Intermediate", "Projective"),
                      ("Lens Focal Length: ", 123.123, 123.123, 123.123),
                      ("Lens Magnification:", 123.123, 123.123, 123.123)]
        lower_results = TableLayout(self, lower_data)
        lower_results.grid(row=0, column=2, sticky="w")

        # condensor aperature label
        condensor = ttk.Label(self, text="Condensor Aperature = 10")
        condensor.grid(row=1, column=0, sticky="e", padx=40)

        # magnification label
        magnification = ttk.Label(self, text="Magnification = 10")
        magnification.grid(row=1, column=2, sticky="w", padx=40)
