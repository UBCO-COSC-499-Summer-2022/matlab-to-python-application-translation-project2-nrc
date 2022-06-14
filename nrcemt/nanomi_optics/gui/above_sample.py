import tkinter as tk
from tkinter import ttk


# widgets configuration for the settings above the sample
class AboveSampleConfiguration(ttk.LabelFrame):

    def __init__(self, master):
        super().__init__(master, text="Settings above sample", borderwidth=10)

        mode_widget = ModeWidget(self)
        mode_widget.pack(side="top", anchor="nw")

        # label for sliders
        sliders_label = ttk.Label(self, text="Lens settings (nm):")
        sliders_label.pack(side="top", pady=5)

        # #call 3 slider layouts and label their names
        c1_slider = SliderLayout(self, "C1: ")
        c1_slider.pack(side="top", anchor="nw", pady=5)

        c2_slider = SliderLayout(self, "C2: ")
        c2_slider.pack(side="top", anchor="nw", pady=5)

        c3_slider = SliderLayout(self, "C3: ")
        c3_slider.pack(side="top", anchor="nw", pady=5)


class ModeWidget(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        label = ttk.Label(self, text="Mode: ")
        label.pack(side='left')

        modes = ('nm', 'Cf', 'Ur')
        option_var = tk.StringVar(self)
        option_menu = ttk.OptionMenu(self, option_var, *modes)
        option_menu.pack(side='left')


# make class that makes a standard slider layout with: label, slider,
# box, and toggle
class SliderLayout(ttk.Frame):

    def __init__(self, master, name):
        super().__init__(master)
        # creates label
        sx_label = ttk.Label(self, text=name)
        sx_label.pack(side="left", padx=5)

        # creates slider
        slider = ttk.Scale(self, length=220, orient='horizontal',)
        slider.pack(side='left', padx=5)

        # creates entry box
        entry = ttk.Entry(self, width=6)
        entry.pack(side="left", padx=5)

        # creates on/off toggle button
        toggle = ttk.Button(self, text="OFF", width=3)
        toggle.pack(side="left", padx=5)
