import tkinter as tk
from tkinter import ttk


# widget for upper settings
class UpperWidgets(ttk.LabelFrame):

    def __init__(self, master):
        super().__init__(master, text="Settings above sample")

        mode_widget = ModeWidget(self)
        mode_widget.pack(side="top", anchor="nw")

        # label for sliders
        sliders_label = ttk.Label(self, text="Lens settings (nm):")
        sliders_label.pack(side="top")

        # #call 3 slider layouts and label their names 
        c1_slider = SliderLayout(self, "C1: ")
        c1_slider.pack(side="top", anchor="nw")

        c2_slider = SliderLayout(self, "C2: ")
        c2_slider.pack(side="top", anchor="nw")

        c3_slider = SliderLayout(self, "C3: ")
        c3_slider.pack(side="top", anchor="nw")


class ModeWidget(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        label = ttk.Label(self, text="Mode: ")
        label.pack(side='left')

        modes = ('nm', 'Cf', 'Ur')
        option_var = tk.StringVar(self)
        option_menu = ttk.OptionMenu(self, option_var, *modes)
        option_menu.pack(side='left')


# make class that makes a standard slider layout with: label, slider, box, and toggle
class SliderLayout(ttk.Frame):

    def __init__(self, master, name):
        super().__init__(master)
        # creates label
        self.x_label = ttk.Label(self, text=name)
        self.x_label.pack(side="left")

        # creates slider
        self.slider = ttk.Scale(self, orient='horizontal',)
        self.slider.pack(side='left')

        # creates entry box
        self.entry = ttk.Entry(self, width=7)
        self.entry.pack(side="left")

        # creates on/off toggle button
        self.toggle = ttk.Button(self, text="OFF", width=3)
        self.toggle.pack(side="left")

# # widgets for lower settings adjustment
# class LowerWidgets(ttk.Frame):

#     def __init__(self, container, *args):
#         super().__init__(container)

#         # new frame that contains widgets for adjusting lower settings
#         self.lower_frame = ttk.Frame(self)

#         #label for radio box
#         self.imagemode_frame= ttk.LabelFrame(text="Image Mode: ")
#         self.imagemode_frame.pack(padx=X_PADDING, pady=Y_PADDING)

#         #diffraction radio button
#         diffraction_radio = ttk.Radiobutton(self.imagemode_frame, 
#         text="Diffraction", width=10)
#         diffraction_radio.pack(side="left",)

#         #image radio button
#         image_radio = ttk.Radiobutton(self.imagemode_frame, text="Image",
#         width=7)
#         image_radio.pack(side="left",)

#         # label for auto mode radio box
#         self.automode_frame= ttk.LabelFrame(text="Auto Mode: ")
#         self.automode_frame.pack(padx=X_PADDING, pady=Y_PADDING)

#         # objective radio button
#         objective_radio = ttk.Radiobutton(self, text="Objective", width=10)
#         objective_radio.pack(side="left",)

#         # Intermediate radio button
#         intermediate_radio = ttk.Radiobutton(self, text="Intermediate",
#         width=7)
#         intermediate_radio.pack(side="left",)

#         # Projective radio button
#         projective_radio = ttk.Radiobutton(self, text="Projective", width=7)
#         projective_radio.pack(side="left",)

#         # None radio button
#         none_radio = ttk.Radiobutton(self, text="None", width=7)
#         none_radio.pack(side="left",)

#         # label for sliders
#         self.sliders_label = ttk.Label(text="Lens settings (nm):")
#         self.sliders_label.pack(padx=X_PADDING, pady=Y_PADDING)

#         # call 4 slider layouts and label their names
#         self.distance_slider = SliderLayout("Distance: ")
#         self.distance_slider.slider_frame.pack()

#         self.objective_slider = SliderLayout("Objective: ")
#         self.objective_slider.slider_frame.pack()

#         self.intermediate_slider = SliderLayout("Intermediate: ")
#         self.intermediate_slider.slider_frame.pack()

#         self.projective_slider = SliderLayout("Projective: ")
#         self.projective_slider.slider_frame.pack()

# # displaying current settings / results
# class DisplaySettings(ttk.Frame):

#     def __init__(self, container, *args):
#         super().__init__(container)

#     # new frame that contains the display of settings and results to the user
#         self.display_frame = ttk.Frame(self)