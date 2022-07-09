from tkinter import ttk


class NumericSpinbox(ttk.Spinbox):

    def __init__(
        self, master, value_default=0, value_range=[0, 100], value_type=int,
        **kwargs
    ):
        super().__init__(
            master, from_=value_range[0], to=value_range[1], **kwargs
        )
        self.value_type = value_type
        self.value_range = value_range
        self.value_default = value_default
        self.value_cached = None
        validate_command = (master.register(self.validate), '%P')
        invalid_command = (master.register(self.on_invalid),)
        self.config(validate="all", validatecommand=validate_command)
        self.config(invalidcommand=invalid_command)
        self.set(value_default)

    def set(self, value):
        self.value_cached = value
        super().set(value)

    def validate(self, value):
        print(value)
        try:
            value = self.value_type(value)
        except Exception:
            return False
        if self.value_range is not None:
            if value < self.value_range[0]:
                return False
            if value > self.value_range[1]:
                return False
        return True

    def on_invalid(self):
        if self.value_cached is not None:
            self.set(self.value_cached)
        else:
            self.set(self.value_default)
