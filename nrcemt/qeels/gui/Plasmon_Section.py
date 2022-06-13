import tkinter as tk
from tkinter import ttk

X_PADDING = 2
Y_PADDING = 2


class PlasmonSelect(ttk.Frame):

    def __init__(self, master, name):
        super().__init__(master)

        # new frame that contains labels and entry boxes
        self.entry_frame = ttk.Frame(self)

        # creates styling for radio buttons
        # creates the radio button
        self.radio_btn = ttk.Radiobutton(self, text=name, width=25)
        self.radio_btn.pack(anchor=tk.W)

        # creates label
        self.x_label = ttk.Label(self.entry_frame, text="X: ")
        self.x_label.pack(side="left", padx=X_PADDING, pady=Y_PADDING)

        # Creates entry box
        self.x_entry = ttk.Entry(self.entry_frame, width=7)
        self.x_entry.pack(side="left", padx=X_PADDING, pady=Y_PADDING)

        # creates label
        self.y_label = ttk.Label(self.entry_frame, text="Y: ")
        self.y_label.pack(side="left", padx=X_PADDING, pady=Y_PADDING)

        # Creates entry box
        self.y_entry = ttk.Entry(self.entry_frame, width=7)
        self.y_entry.pack(side="left", padx=X_PADDING, pady=Y_PADDING)
        self.entry_frame.pack()


class ResultBoxes(ttk.Frame):
    def __init__(self, master, name):
        super().__init__(master)
        ev_label = ttk.Label(self, text=name + ": ", width=20)
        ev_entry = ttk.Entry(self, width=7)
        ev_label.pack(side="left", pady=X_PADDING)
        ev_entry.pack(side="left", pady=Y_PADDING)

class WidthComponent(ttk.Frame):
    def __init__(self,master):
        super().__init__(master)
        #Creating width label and entry box
        width_label=ttk.Label(self,text="Width: ",)
        width_entry=ttk.Entry(self,width=7)
        
        #creating detect checkbox
        detect_checkbox=ttk.Checkbutton(self,text="Detect")
        
        #adding empty label so lines up with other components
        #ttk.Label(self).pack(side="top")
        #Placing above items
        width_label.pack(side="left",anchor=tk.NW,padx=X_PADDING,pady=Y_PADDING)
        width_entry.pack(side="left",pady=Y_PADDING,padx=X_PADDING)
        detect_checkbox.pack(side="left",padx=X_PADDING,pady=Y_PADDING)