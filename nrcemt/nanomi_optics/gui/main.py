# Nanomi Optics GUI
import tkinter as tk
from tkinter import ttk
from nrcemt.nanomi_optics.engine import nanomi_engine_greeting
from .main_window import MainWindow


def main():
    # application 
    # window creation
    root = MainWindow()
    # set title of window
    root.title('Nanomi Optics')
    # set window size 
    root.geometry(f'1200x800')

    # keep the window open
    root.mainloop()

if __name__ == "__main__":
    main()
