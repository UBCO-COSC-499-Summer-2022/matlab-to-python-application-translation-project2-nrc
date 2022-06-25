import tkinter as tk


class ScaleSpinboxLink:

    def __init__(self, scale, spinbox, value, value_range, value_type=float):
        self.command = None
        self.value_type = value_type
        self.scale = scale
        self.spinbox = spinbox
        scale.set(value)
        self.spinbox_var = tk.StringVar()
        self.spinbox_var.trace('w', lambda a, b, c: self.handle_spinbox())
        scale.configure(
            from_=value_range[0],
            to=value_range[1],
            command=self.handle_scale
        )
        spinbox.configure(
            from_=value_range[0],
            to=value_range[1],
            textvariable=self.spinbox_var
        )
        spinbox.set(value)

    def set_command(self, command):
        self.command = command

    def get(self):
        return self.scale.get()

    def set(self, value):
        self.scale.set(value)

    def handle_scale(self, value):
        rounded_value = round(self.value_type(float(value)), 2)
        self.spinbox.set(rounded_value)
        if self.command is not None:
            self.command(rounded_value)

    def handle_spinbox(self):
        try:
            self.scale.set(self.spinbox_var.get())
        except:
            pass
