from tkinter import ttk
from .widget_templates import TableLayout
from nrcemt.nanomi_optics.engine.lens_excitation import (
    ur_asymetric, ur_symmetric
)


PAD_Y = 5


# widget layout for the results
class ResultsFrame(ttk.LabelFrame):

    def __init__(
        self, master, f_upper, f_lower, mag_upper, mag_lower, aper, mag
    ):
        super().__init__(master, text="Results", borderwidth=5)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        # upper lens results
        self.ur = [
            ur_symmetric(f_upper[0]),
            ur_asymetric(f_upper[1]),
            ur_asymetric(f_upper[2])
        ]
        self.upper_units = ["", "mm", "x"]
        upper_data = [
            ("", "C1", "C2", "C3"),
            ("Lens Ur: ", *self.ur),
            ("Lens Focal length:", *f_upper),
            ("Lens Magification:", *mag_upper)
        ]
        self.upper_results = TableLayout(self, upper_data, self.upper_units)
        self.upper_results.grid(row=0, column=0, sticky="e")

        self.lower_units = ["mm", "x"]
        # lower lens results
        lower_data = [
            ("", "Objective", "Intermediate", "Projective"),
            ("Lens Focal Length: ", *f_lower),
            ("Lens Magnification:", *mag_lower)
        ]
        self.lower_results = TableLayout(self, lower_data, self.lower_units)
        self.lower_results.grid(row=0, column=2, sticky="w")

        # condensor aperature label
        aperature = aper * 1e3
        self.condensor = ttk.Label(
            self, text=f"Condensor Aperature = {aperature:.2f} nm"
        )
        self.condensor.grid(row=1, column=0, sticky="e", padx=40)

        # magnification label
        self.magnification = ttk.Label(
            self, text=f"Magnification = {mag:.2f} x"
        )
        self.magnification.grid(row=1, column=2, sticky="w", padx=40)

    def update_results(
        self, f_upper, f_lower, mag_upper, mag_lower, aper, mag
    ):
        self.ur = [
            ur_symmetric(f_upper[0]),
            ur_asymetric(f_upper[1]),
            ur_asymetric(f_upper[2])
        ]
        self.upper_results.update_table(
            self.upper_units, self.ur, f_upper, mag_upper
        )

        self.lower_results.update_table(
            self.lower_units, f_lower, mag_lower
        )
        aperature = aper * 1e3
        self.condensor["text"] = f"Condensor Aperature = {aperature:.2f} nm"

        self.magnification["text"] = f"Magnification = {mag:.2f} x"
