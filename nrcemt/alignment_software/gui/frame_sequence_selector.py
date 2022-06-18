import tkinter as tk
from tkinter import ttk


class SequenceSelector(ttk.Frame):

    def __init__(self, master, title, **kwargs):
        ttk.Frame.__init__(self, master, **kwargs)
        self.length = 0
        self.command = None
        top_frame = ttk.Frame(self)
        bottom_frame = ttk.Frame(self)
        title = ttk.Label(top_frame, text=title)
        self.entry_var = tk.StringVar()
        self.entry_var.set("0")
        self.entry_var.trace("w", self.handle_entry)
        self.entry = ttk.Entry(
            top_frame,
            textvariable=self.entry_var,
            state="disabled",
            validate="focusout",
            validatecommand=self.validate_entry,
            width=3
        )
        self.length_label = ttk.Label(top_frame, text=" / 0")
        self.scale = tk.Scale(
            bottom_frame,
            from_=1,
            state="disabled",
            orient="horizontal",
            command=self.handle_scale
        )
        left_button = ttk.Button(
            bottom_frame, text="<", width=0.5,
            command=self.handle_left_button
        )
        right_button = ttk.Button(
            bottom_frame, text=">", width=0.5,
            command=self.handle_right_button
        )
        title.pack(side="left")
        self.length_label.pack(side="right")
        self.entry.pack(side="right")
        left_button.pack(side="left")
        right_button.pack(side="right")
        self.scale.pack(fill="x", expand=True)
        top_frame.pack(fill="x", expand=True)
        bottom_frame.pack(fill="x", expand=True)

    def set(self, scale):
        self.scale.set(scale)

    def set_length(self, length):
        self.length = length
        self.length_label.config(text=" / " + str(length))
        if length > 0:
            self.scale.config(state="normal")
            self.entry.config(state="normal")
            self.scale.config(to=length)
            new_scale = self.scale.get()
            self.handle_scale(new_scale)
        else:
            self.entry_var.set("0")
            self.scale.config(state="disabled")
            self.entry.config(state="disabled")

    def set_command(self, command):
        self.command = command

    def handle_scale(self, scale):
        self.entry_var.set(str(scale))
        if self.command is not None:
            self.command(int(scale))

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
