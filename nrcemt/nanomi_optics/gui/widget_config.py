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

        #labelframe for drop down box
        self.mode_label = ttk.LabelFrame(text="Mode: ")
        self.mode_label.pack(padx=X_PADDING, pady=Y_PADDING)
        
        # create drop down box
        self.modes = ('nm', 'Cf', 'Ur')
        self.option_var = tk.StringVar(self)
        self.option_var.set(self.modes[0])
        option_menu = ttk.OptionMenu(self.mode_label, self.option_var, *self.modes)
        option_menu.pack(side = 'left', padx=X_PADDING, pady=Y_PADDING)
        
        # label for sliders
        self.sliders_label = ttk.Label(text="Lens settings (nm):")
        self.sliders_label.pack(padx=X_PADDING, pady=Y_PADDING)
        
        #call 3 slider layouts and label their names 
        self.c1_slider = SliderLayout("C1: ")
        self.c1_slider.slider_frame.pack(padx=X_PADDING, pady=Y_PADDING)
        
        self.c2_slider = SliderLayout("C2: ")
        self.c2_slider.slider_frame.pack(padx=X_PADDING, pady=Y_PADDING)
        
        self.c3_slider = SliderLayout("C3: ")
        self.c3_slider.slider_frame.pack(padx=X_PADDING, pady=Y_PADDING)

# make class that makes a standard slider layout with: label, slider, box, and toggle
class SliderLayout(ttk.Frame):
    
    def __init__(self, name):
        
        # new frame that contains widgets
        self.slider_frame = ttk.Frame()
        
        # creates label
        self.x_label = ttk.Label(text=name)
        self.x_label.pack(side="left", padx=X_PADDING)
        
        # creates slider
        self.val = tk.DoubleVar()
        self.slider = ttk.Scale(variable = self.val, from_=0, to = 100, orient='horizontal',)
        self.slider.pack(side ='left', padx=X_PADDING)
        
        # creates entry box
        self.entry = ttk.Entry(width=7)
        self.entry.pack(side="left", padx=X_PADDING)

        # creates on/off toggle button
        self.toggle = ttk.Button(text="OFF", width=3)
        self.toggle.pack(side="left", padx=X_PADDING)

# widgets for lower settings adjustment
class LowerWidgets(ttk.Frame):
    
    def __init__(self, container, *args):
        super().__init__(container)
            
        # new frame that contains widgets for adjusting lower settings
        self.lower_frame = ttk.Frame(self)
        
        #label for radio box
        self.imagemode_frame= ttk.LabelFrame(text="Image Mode: ")
        self.imagemode_frame.pack(padx=X_PADDING, pady=Y_PADDING)
        
        #diffraction radio button
        diffraction_radio = ttk.Radiobutton(self.imagemode_frame, text="Diffraction", width=10)
        diffraction_radio.pack(side="left",)
        
        #image radio button
        image_radio = ttk.Radiobutton(self.imagemode_frame, text="Image", width=7)
        image_radio.pack(side="left",)
        
        # label for auto mode radio box
        self.automode_frame= ttk.LabelFrame(text="Auto Mode: ")
        self.automode_frame.pack(padx=X_PADDING, pady=Y_PADDING)
        
        # objective radio button
        objective_radio = ttk.Radiobutton(self.automode_frame, text="Objective", width=10)
        objective_radio.pack(side="left",)
        
        # Intermediate radio button
        intermediate_radio = ttk.Radiobutton(self.automode_frame, text="Intermediate", width=7)
        intermediate_radio.pack(side="left",)
        
        # Projective radio button
        projective_radio = ttk.Radiobutton(self.automode_frame, text="Projective", width=7)
        projective_radio.pack(side="left",)
        
        # None radio button
        none_radio = ttk.Radiobutton(self.automode_frame, text="None", width=7)
        none_radio.pack(side="left",)
        
        # label for sliders
        self.sliders_label = ttk.Label(text="Lens settings (nm):")
        self.sliders_label.pack(padx=X_PADDING, pady=Y_PADDING)
        
        # call 4 slider layouts and label their names 
        self.distance_slider = SliderLayout("Distance: ")
        self.distance_slider.slider_frame.pack(padx=X_PADDING, pady=Y_PADDING)
        
        self.objective_slider = SliderLayout("Objective: ")
        self.objective_slider.slider_frame.pack(padx=X_PADDING, pady=Y_PADDING)
        
        self.intermediate_slider = SliderLayout("Intermediate: ")
        self.intermediate_slider.slider_frame.pack(padx=X_PADDING, pady=Y_PADDING)
        
        self.projective_slider = SliderLayout("Projective: ")
        self.projective_slider.slider_frame.pack(padx=X_PADDING, pady=Y_PADDING)
            
# displaying current settings / results
class DisplaySettings(ttk.Frame):
    
    def __init__(self, container, *args):
        super().__init__(container)
        
        # new frame that contains the display of settings and results to the user
        self.display_frame = ttk.Frame(self) 