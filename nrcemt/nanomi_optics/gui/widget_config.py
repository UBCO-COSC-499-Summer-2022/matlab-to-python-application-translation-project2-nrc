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
        
        # label for sliders
        self.sliders_label = ttk.Label(self.upper_frame, text="Lens settings (nm):")
        self.sliders_label.pack(side="left", padx=X_PADDING, pady=Y_PADDING)
        
        #call 3 sliders with label names 
        SliderLayout.layout("C1: ")
        SliderLayout.layout("C2: ")
        SliderLayout.layout("C3: ")
        
        
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


# make class that makes a standard slider layout with: label, slider, box, and toggle
class SliderLayout(ttk.Frame):
    
    def layout(name):
        
        # new frame that contains widgets
        slider_frame = ttk.Frame()
        
        # creates label
        x_label = ttk.Label(slider_frame, text=name)
        x_label.pack(side="left", padx=X_PADDING, pady=Y_PADDING)
        
        # creates slider
        slider = ttk.Scale(slider_frame, from_=0, to = 100, orient='horizontal',)
        
        # creates entry box
        entry = ttk.Entry(slider_frame, width=9)
        entry.pack(side="left", padx=X_PADDING, pady=Y_PADDING)
        
        #make toggle
        #toggle function
        def Toggle():
            if toggle.config("text")[-1] == "ON":
                toggle.config(text="OFF")
            else:
                toggle.config(text="ON")
        # creates on/of toggle button
        toggle = ttk.Button(text="OFF", width=10, command=Toggle)
        toggle.pack(side="left", padx=X_PADDING, pady=Y_PADDING)
    
        

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

# class that makes a standard radio button layout