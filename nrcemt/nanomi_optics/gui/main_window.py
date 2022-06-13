import tkinter as tk
from tkinter import ttk
from .widget_config import UpperWidgets, LowerWidgets, DisplaySettings

class MainWindow(ttk.Frame):
    
    def __init__(self, master):
        super().__init__(master)
        inputs = ttk.Frame(master)
        
        # Upper Settings
        upper_menu = UpperWidgets(inputs)
        upper_menu.grid(row=0, column=0, padx=2, pady=2)
        
        # Lower Settings
        lower_menu = LowerWidgets(inputs)
        lower_menu.grid(row=1, column=0, padx=2, pady=2)
        
        # Display Results
        