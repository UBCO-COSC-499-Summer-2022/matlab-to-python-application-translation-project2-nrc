import tkinter as tk

class Buttons(tk.Tk):
    def __init__(self, master, custom_arg):
        tk.Tk.__init__(self, master)
        container = tk.Frame(self)
        
        