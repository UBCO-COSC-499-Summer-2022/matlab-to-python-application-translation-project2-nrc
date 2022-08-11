import tkinter as tk


class ScaleSpinboxLink:
    """A link between a slider and a spinbox."""

    def __init__(self, scale, spinbox, value, value_range):
        """Creates a link between an existing slider and spinbox."""
        self.command = None
        self.decimals = 2
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
        """Sets the command to be called when updated."""
        self.command = command

    def set_disabled(self, is_disabled):
        """Enables or disables (greys out) the slider and spinbox."""
        if is_disabled:
            self.scale.config(state="disabled")
            self.spinbox.config(state="disabled")
        else:
            self.scale.config(state="normal")
            self.spinbox.config(state="normal")

    def get(self):
        """Returns value represeneted by the link."""
        return self.scale.get()

    def set(self, value):
        """Sets the value of the link."""
        value = float(value)
        self.scale.set(value)
        self.update_spinbox(value)

    def update_spinbox(self, value):
        """Updated the value of the spinbox independent from the slider."""
        if self.to_spinbox is not None:
            value = self.to_spinbox(value)
        rounded_value = round(value, self.decimals)
        self.spinbox.set(rounded_value)

    def handle_scale(self, value):
        """Called when the slider is moved."""
        value = float(value)
        self.update_spinbox(value)
        if self.command is not None:
            self.command(value)

    def handle_spinbox(self):
        """Called when the spinbox is updated."""
        try:
            spinbox_value = self.from_spinbox(float(self.spinbox_var.get()))
            self.scale.set(spinbox_value)
        except Exception:
            pass

    def set_spinbox_mapping(
        self, to_spinbox, from_spinbox, decimals, spinbox_range
    ):
        """
        Sets a custom mapping for the value in the spinbox, while keeping
        the underlying slider values the same.
        For example the underlying slider values may be (0, 1).
        But you might want map that onto the range (0, 100).
        Or you may want to use and even more complicated mapping function.
        """
        self.to_spinbox = to_spinbox
        self.from_spinbox = from_spinbox
        self.update_spinbox(self.scale.get())
        self.decimals = decimals
        self.spinbox.configure(
            from_=spinbox_range[0],
            to=spinbox_range[1]
        )
