import tkinter as tk
from tkinter import ttk
from .widget_config import UpperWidgets, LowerWidgets, DisplaySettings

class MainWindow(ttk.Frame):
    
    def __init__(self, master):
        super().__init__(master)
        inputs = ttk.Frame(master)
        
        # Upper Settings
        options_menu = UpperWidgets(inputs)
        options_menu.grid(row=0, column=0, padx=2, pady=2)
        
        # Lower Settings
        
        # Display Results
        