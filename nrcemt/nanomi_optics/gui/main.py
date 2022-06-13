#Nanomi Optics GUI
import tkinter as tk
from tkinter import ttk, Label
from nrcemt.nanomi_optics.engine import nanomi_engine_greeting
from .main_window import MainWindow


def main():
    #application window creation
    root = tk.Tk()
    #set title of window
    root.title('Nanomi Optics')
    #size of the window
    window_width = 1200
    window_height = 800
    #set the position of the window 
    root.geometry(f'{window_width}x{window_height}+50+50')
    
    #print engine message 
    message = Label(root, text=nanomi_engine_greeting())
    message.grid(column=0, row=0, padx=20, pady=20)
 
    #mainlabel frame for settings above sample
    #lf_above = ttk.LabelFrame(root, text='Settings above sample')
    #lf_above.grid(column=0, row=1, padx=20, pady=20)

    #placeholder label
    #label_settings = Label(lf_above, text = 'Lens Settings')
    #label_settings.pack(ipadx=10, ipady=10)

    #main label frame for settings below sample
    #lf_below = ttk.LabelFrame(root, text='Settings below sample')
    #lf_below.grid(column=0, row=2, padx=20, pady=20)

    #placeholder buttons
    #settingsb_var = tk.StringVar()
    #settingsb = ('Left', 'Center', 'Right')
    #grid_column = 0
    #for setting in settingsb:
        # create a radio button
        #radio = ttk.Radiobutton(lf_below, text=setting, value=setting, variable=settingsb_var)
        #radio.grid(column=grid_column, row=0, ipadx=10, ipady=10)
        # grid column
        #grid_column += 1

    #main label frame for results 

    #keep the window open
    root.mainloop()

if __name__ == "__main__":
    main()
