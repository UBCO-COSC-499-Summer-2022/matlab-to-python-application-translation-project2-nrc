# contains templates for widgets that will be used in other classes
import tkinter as tk
from tkinter import ttk


# makes a standard drop down menu widget
# (upper sensors)
class DropDownWidget(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        label = ttk.Label(self, text="Mode: ")
        label.pack(side='left')

        modes = ('nm', 'Cf', 'Ur')
        option_var = tk.StringVar(self)
        option_menu = ttk.OptionMenu(self, option_var, *modes)
        option_menu.pack(side='left')


# makes a standard slider layout with: label, slider, box, and toggle
# (upper + lower sensors)
class SliderLayout(ttk.Frame):

    def __init__(self, master, name):
        super().__init__(master)

        self.columnconfigure(1, weight=1)

        # creates label
        sx_label = ttk.Label(self, text=name, width=10, anchor="e")
        sx_label.grid(column=0, row=0, sticky="e", padx=5)

        # creates slider
        slider = ttk.Scale(self, length=200, orient='horizontal')
        slider.grid(column=1, row=0, padx=5)

        # creates entry box
        entry = ttk.Entry(self, width=6)
        entry.grid(column=2, row=0, padx=5)

        # creates on/off toggle button
        toggle = ttk.Button(self, text="OFF", width=5)
        toggle.grid(column=3, row=0, padx=5)


# radio button widgets layout - located inside its own labelframe
# (lower sensors)
class RadioLayout(ttk.LabelFrame):

    def __init__(self, master, name, radio_names):
        super().__init__(master, text=name, borderwidth=5)
        # takes a list of names for radio widgets and puts them next
        # to each other inside of the label frame
        for item in radio_names:
            button = ttk.Radiobutton(self, text=item)
            button.pack(side="left", anchor="nw", padx=10)


# table layout created using Labels and Text
# (results)
class TableLayout(ttk.Frame):

    def __init__(self, master, data_list):
        super().__init__(master, borderwidth=5)

        # takes in list and makes table
        for i, row in enumerate(data_list):
            for j, value in enumerate(row):
                if i == 0 or j == 0:
                    table_data = ttk.Label(
                        self, text=value,
                        width=20, anchor="w"
                    )
                    table_data.grid(row=i, column=j)
                else:
                    table_data = tk.Text(self, width=20, height=1)
                    table_data.insert("insert", value)
                    table_data.config(state=tk.DISABLED)
                    table_data.grid(row=i, column=j, sticky="w")
