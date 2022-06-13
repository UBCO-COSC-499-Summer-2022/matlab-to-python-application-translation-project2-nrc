import tkinter as tk
from tkinter import ttk

X_PADDING = 2
Y_PADDING = 2
        
# widget for upper settings
class UpperWidgets(ttk.Frame):
    
    def __init__(self, container, *args):
        super().__init__(container)
        
        # new frame that contains widgets for adjusting upper settings
        self.upper_frame = ttk.Frame(self)
        
        # create drop down box
        self.modes = ('nm', 'Cf', 'Ur')
        self.option_var = tk.StringVar(self)
        self.create_widget
        
    def create_widget(self):
        #label for drop down box
        mode_label = ttk.Label(self.upper_frame, text="Mode: ")
        #option menu
        option_menu = ttk.OptionMenu(
            self,
            self.option_var,
            self.modes[0],
            *self.modes
        )
        option_menu.pack(side="left", padx=X_PADDING, pady=Y_PADDING)


# make class that makes a standard slider

# widgets for lower settings adjustment
class LowerWidgets(ttk.Frame):
    
    def __init__(self, container, *args):
        super().__init__(container)
            
        # new frame that contains widgets for adjusting lower settings
        self.lower_frame = ttk.Frame(self)
            
# displaying current settings / results
class DisplaySettings(ttk.Frame):
    
    def __init__(self, container, *args):
        super().__init__(container)
        
        # new frame that contains the display of settings and results to the user
        self.display_frame = ttk.Frame(self) 

# make class that makes a standard radio button


