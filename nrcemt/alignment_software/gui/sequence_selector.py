import tkinter as tk


class SequenceSelector(tk.Frame):

    def __init__(self, master, title, command=None):
        tk.Frame.__init__(self, master)
        self.length = 0
        self.command = command
        self.top_frame = tk.Frame(self)
        self.bottom_frame = tk.Frame(self)
        self.title = tk.Label(self.top_frame, text=title)
        self.entry_var = tk.StringVar()
        self.entry_var.set("0")
        self.entry_var.trace("w", self.handle_entry)
        self.entry = tk.Entry(
            self.top_frame,
            textvariable=self.entry_var,
            state=tk.DISABLED,
            validate="focusout",
            validatecommand=self.validate_entry,
            width=3
        )
        self.length_label = tk.Label(self.top_frame, text=" / 0")
        self.scale = tk.Scale(
            self.bottom_frame,
            from_=1,
            state=tk.DISABLED,
            orient=tk.HORIZONTAL,
            command=self.handle_scale
        )
        self.left_button = tk.Button(
            self.bottom_frame, text="<", command=self.handle_left_button)
        self.right_button = tk.Button(
            self.bottom_frame, text=">", command=self.handle_right_button)
        self.title.pack(side=tk.LEFT)
        self.length_label.pack(side=tk.RIGHT)
        self.entry.pack(side=tk.RIGHT)
        self.left_button.pack(side=tk.LEFT)
        self.right_button.pack(side=tk.RIGHT)
        self.scale.pack(fill="x", expand=True)
        self.top_frame.pack(fill="x", expand=True)
        self.bottom_frame.pack(fill="x", expand=True)

    def set_length(self, length):
        self.length = length
        self.length_label.config(text=" / " + str(length))
        if length > 0:
            self.scale.config(state=tk.NORMAL)
            self.entry.config(state=tk.NORMAL)
            old_scale = self.scale.get()
            self.scale.config(to=length)
            new_scale = self.scale.get()
            if old_scale != new_scale:
                self.handle_scale(new_scale)
        else:
            self.entry_var.set("0")
            self.scale.config(state=tk.DISABLED)
            self.entry.config(state=tk.DISABLED)

    def handle_scale(self, scale):
        self.entry_var.set(str(scale))
        self.command(scale)

    def handle_entry(self, *_):
        if self.validate_entry():
            scale = int(self.entry_var.get())
            self.scale.set(scale)

    def handle_left_button(self):
        scale = self.scale.get()
        scale -= 1
        if scale >= 1:
            self.scale.set(scale)
            self.handle_scale(scale)

    def handle_right_button(self):
        scale = self.scale.get()
        scale += 1
        if scale <= self.length:
            self.scale.set(scale)
            self.handle_scale(scale)

    def validate_entry(self):
        try:
            scale = int(self.entry_var.get())
            return scale > 0 and scale <= self.length
        except ValueError:
            return False
