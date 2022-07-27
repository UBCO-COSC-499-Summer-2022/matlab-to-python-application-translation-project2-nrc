from tkinter import ttk


class NumericSpinbox(ttk.Spinbox):

    def __init__(
        self, master, value_default=0, value_range=[0, 100], value_type=int,
        command=None, **kwargs
    ):
        super().__init__(
            master, from_=value_range[0], to=value_range[1], **kwargs
        )
        self.value_type = value_type
        self.value_range = value_range
        self.value_default = value_default
        self.value_cached = None
        self.command = command
        validate_command = (master.register(self.validate), '%P')
        invalid_command = (master.register(self.on_invalid),)
        self.config(validate="focusout", validatecommand=validate_command)
        self.config(invalidcommand=invalid_command)
        self.set(value_default)

    def get(self):
        return self.value_type(super().get())

    def set(self, value):
        self.value_cached = value
        super().set(value)

    def set_command(self, command):
        self.command = command

    def validate(self, value):
        try:
            value = self.value_type(value)
            if self.value_range is not None:
                if value < self.value_range[0]:
                    valid = False
                if value > self.value_range[1]:
                    valid = False
            valid = True
        except Exception:
            valid = False
        if valid:
            self.value_cached = value
            if self.command is not None:
                self.command()
        return valid

    def on_invalid(self):
        if self.value_cached is not None:
            self.set(self.value_cached)
        else:
            self.set(self.value_default)
