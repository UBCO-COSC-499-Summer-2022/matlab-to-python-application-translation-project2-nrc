import tkinter as tk
from tkinter import ttk
from .widget_templates import DropDownWidget, SliderLayout, ToggleButton
from nrcemt.common.gui import ScaleSpinboxLink
from nrcemt.nanomi_optics.engine.lens_excitation import (
    ur_symmetric, ur_asymmetric, cf_symmetric, cf_asymmetric
)
PAD_Y = 5


# widgets configuration for the settings above the sample
class AboveSampleFrame(tk.LabelFrame):

    def __init__(self, master):
        super().__init__(master, text="Settings above sample")
        self.columnconfigure(1, weight=1)

        self.mode_widget = DropDownWidget(self)
        self.mode_widget.grid(row=0, column=0, sticky="we")

        # label for sliders
        sliders_label = ttk.Label(self, text="Lens settings (mm):")
        sliders_label.grid(row=1, column=0, sticky="we")

        # stores the values of the lenses
        self.focal_values = [67.29, 22.94, 39.88]

        # stores the status of the lenses on/off
        self.lens_status = [True, True, True]

        self.c1_slider = SliderLayout(self, "Lens C1: ")
        self.c1_link = ScaleSpinboxLink(
            self.c1_slider.slider,
            self.c1_slider.entry,
            self.focal_values[0], (6, 300)
        )
        self.c1_slider.grid(row=2, column=0, columnspan=2, sticky="nwse")

        self.c1_toggle = ToggleButton(self)
        self.c1_toggle.grid(row=2, column=2)

        c2_slider = SliderLayout(self, "Lens C2: ")
        self.c2_link = ScaleSpinboxLink(
            c2_slider.slider,
            c2_slider.entry,
            self.focal_values[1], (6, 300)
        )
        c2_slider.grid(row=3, column=0, columnspan=2, sticky="nwse")

        self.c2_toggle = ToggleButton(self)
        self.c2_toggle.grid(row=3, column=2)

        c3_slider = SliderLayout(self, "Lens C3: ")
        self.c3_link = ScaleSpinboxLink(
            c3_slider.slider,
            c3_slider.entry,
            self.focal_values[2], (6, 300)
        )
        c3_slider.grid(row=4, column=0, columnspan=2, sticky="nwse")
        self.c3_toggle = ToggleButton(self)
        self.c3_toggle.grid(row=4, column=2)

    # def set_mode(self, mode):
    #     links = [self.c1_link, self.c2_link, self.c3_link]
    #     lens_type = [True, False, False]
    #     if mode:
    #         for link in links:
    #             link.spinbox_var.trace_vdelete("w", link.trace_id)
    #             link.trace_id = link.spinbox_var.trace(
    #                 'w', lambda a, b, c: link.handle_spinbox()
    #             )
    #             link.scale.configure(command=link.handle_scale)
    #             link.handle_scale(link.scale.get())
    #     else:
    #         for i, link in enumerate(links):
    #             if lens_type[i]:
    #                 link.spinbox_var.trace_vdelete("w", link.trace_id)
    #                 link.trace_id = link.spinbox_var.trace(
    #                     'w', lambda a, b, c: self.handle_spinbox_uf_sym(link)
    #                 )
    #                 link.scale.configure(
    #                     command=lambda a: self.handle_scale_uf_sym(a, link)
    #                 )
    #                 self.handle_scale_uf_sym(link.scale.get(), link)
    #             else:
    #                 link.spinbox_var.trace_vdelete("w", link.trace_id)
    #                 link.trace_id = link.spinbox_var.trace(
    #                     'w', lambda a, b, c: self.handle_spinbox_uf_asym(link)
    #                 )
    #                 link.scale.configure(
    #                        command=lambda a: self.handle_scale_uf_asym(a, link)
    #                 )
    #                 self.handle_scale_uf_asym(link.scale.get(), link)

    # def handle_spinbox_uf_sym(self, link):
    #     try:
    #         link.scale.set(cf_symmetric(float(link.spinbox_var.get())))
    #     except Exception:
    #         pass

    # def handle_spinbox_uf_asym(self, link):
    #     try:
    #         link.scale.set(cf_asymmetric(float(link.spinbox_var.get())))
    #     except Exception:
    #         pass

    # def handle_scale_uf_sym(self, value, link):
    #     rounded_value = ur_symmetric(round(link.value_type(float(value)), 2))
    #     link.spinbox.set(rounded_value)
    #     if link.command is not None:
    #         link.command(rounded_value)

    # def handle_scale_uf_asym(self, value, link):
    #     rounded_value = ur_asymmetric(round(link.value_type(float(value)), 2))
    #     link.spinbox.set(rounded_value)
    #     if link.command is not None:
    #         link.command(rounded_value)
