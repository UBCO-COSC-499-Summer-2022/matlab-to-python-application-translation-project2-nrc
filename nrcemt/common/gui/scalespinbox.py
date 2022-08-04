import tkinter as tk
from nrcemt.nanomi_optics.engine.lens_excitation import (
    ur_symmetric, ur_asymmetric, cf_symmetric, cf_asymmetric
)


class ScaleSpinboxLink:

    def __init__(self, scale, spinbox, value, value_range):
        self.command = None
        self.scale = scale
        self.spinbox = spinbox
        scale.set(value)
        self.to_spinbox = lambda x: x
        self.from_spinbox = lambda x: x
        self.spinbox_var = tk.StringVar()
        self.trace_id = self.spinbox_var.trace(
            'w', lambda a, b, c: self.handle_spinbox()
        )
        self.scale.configure(
            from_=value_range[0],
            to=value_range[1],
            command=self.handle_scale
        )
        self.spinbox.configure(
            from_=value_range[0],
            to=value_range[1],
            textvariable=self.spinbox_var
        )
        self.spinbox.set(value)

    def set_command(self, command):
        self.command = command

    def set_disabled(self, is_disabled):
        if is_disabled:
            self.scale.config(state="disabled")
            self.spinbox.config(state="disabled")
        else:
            self.scale.config(state="normal")
            self.spinbox.config(state="normal")

    def get(self):
        return self.scale.get()

    def set(self, value):
        value = float(value)
        self.scale.set(value)
        self.update_spinbox(value)

    def update_spinbox(self, value):
        if self.to_spinbox is not None:
            value = self.to_spinbox(value)
        rounded_value = round(value, 2)
        self.spinbox.set(rounded_value)

    def handle_scale(self, value):
        value = float(value)
        self.update_spinbox(value)
        if self.command is not None:
            self.command(value)

    def handle_scale_uf_sym(self, value):
        rounded_value = ur_symmetric(round(self.value_type(float(value)), 2))
        self.spinbox.set(rounded_value)
        if self.command is not None:
            self.command(rounded_value)

    def handle_scale_uf_asym(self, value):
        rounded_value = ur_asymmetric(round(self.value_type(float(value)), 2))
        self.spinbox.set(rounded_value)
        if self.command is not None:
            self.command(rounded_value)

    def handle_spinbox(self):
        try:
            spinbox_value = self.from_spinbox(float(self.spinbox_var.get()))
            self.scale.set(spinbox_value)
        except Exception:
            pass

    def set_spinbox_mapping(self, to_spinbox, from_spinbox, spinbox_range):
        self.to_spinbox = to_spinbox
        self.from_spinbox = from_spinbox
        self.update_spinbox(self.scale.get())
        self.spinbox.configure(
            from_=spinbox_range[0],
            to=spinbox_range[1]
        )
