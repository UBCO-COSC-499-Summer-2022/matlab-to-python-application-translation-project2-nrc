# Nanomi Optics GUI
import tkinter as tk
from tkinter import ttk
from nrcemt.nanomi_optics.engine import nanomi_engine_greeting
from .main_window import MainWindow


def main():
    # application 
    # window creation
    root = tk.Tk()
    # set title of window
    root.title('Nanomi Optics')
    # set window size 
    root.geometry(f'1200x800')
    
    # create window with all widgets
    main_window = MainWindow(root)
    main_window.pack()

    # keep the window open
    root.mainloop()

if __name__ == "__main__":
    main()
