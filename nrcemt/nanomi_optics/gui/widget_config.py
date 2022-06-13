import tkinter as tk
from tkinter import ttk
        
#widgets for upper settings adjustment
class UpperWidgets(ttk.Frame):
    def __init__(self, container, *args):
        super().__init__(container)
        
        #new frame that contains widgets for adjusting upper settings
        self.upper_frame = ttk.Frame(self)

#widgets for lower settings adjustment
class LowerWidgets(ttk.Frame):
    def __init__(self, container, *args):
        super().__init__(container)
            
        #new frame that contains widgets for adjusting lower settings
        self.lower_frame = ttk.Frame(self)
            
#displaying current settings / results
class DisplaySettings(ttk.Frame):
    def __init__(self, container, *args):
        super().__init__(container)
        
        #new frame that contains the display of settings and results to the user
        self.display_frame = ttk.Frame(self)

#make class that makes a standard slider then call it inside UpperWidget + LowerWidget???
#make class that makes a standard radio button
# then call it inside UpperWidget + LowerWidget???


