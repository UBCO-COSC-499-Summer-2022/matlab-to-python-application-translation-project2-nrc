import tkinter as tk
from tkinter import ttk

from pyparsing import col
from .plasmon_section import PlasmonSelect, ResultBoxes,WidthComponent


class MainWindow(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        inputs = ttk.Frame(master)
        # Bulk Plasmons
        bulk_plasmon1 = PlasmonSelect(inputs, "Bulk Plasmon 1")
        bulk_plasmon2 = PlasmonSelect(inputs, "Bulk Plasmon 2")
        bulk_width = WidthComponent(inputs)
        bulk_plasmon1.grid(row=0, column=0, padx=2, pady=2)
        bulk_plasmon2.grid(row=0, column=1, padx=2, pady=2)
        bulk_width.grid(row=0,column=2,padx=2,pady=2)
        

        # Surface Plasmon Upper
        upper_plasmon1 = PlasmonSelect(inputs, "Surface Plasmon Upper 1")
        upper_plasmon2 = PlasmonSelect(inputs, "Surface Plasmon Upper 2")
        upper_width = WidthComponent(inputs)
        upper_plasmon1.grid(row=1, column=0, padx=2, pady=2)
        upper_plasmon2.grid(row=1, column=1, padx=2, pady=2)
        upper_width.grid(row=1,column=2,padx=2,pady=2)

        # Surface Plasmon Lower
        lower_plasmon1 = PlasmonSelect(inputs, "Surface Plasmon Lower 1")
        lower_plasmon2 = PlasmonSelect(inputs, "Surface Plasmon Lower 2")
        lower_width = WidthComponent(inputs)
        lower_plasmon1.grid(row=2, column=0, padx=2, pady=2)
        lower_plasmon2.grid(row=2, column=1, padx=2, pady=2)
        lower_width.grid(row=2,column=2,padx=2,pady=2)

        inputs.pack(anchor=tk.SW)

        # Average Pixel
        results = ttk.Frame(master)
        average_pixel = ResultBoxes(results, "Average Pixel")
        average_pixel.pack()
        # Micro rad/pixel upper
        rad_upper = ResultBoxes(results, "Micro rad/Pixel Upper")
        rad_upper.pack()
        # Micro rad/pixel lower
        rad_lower = ResultBoxes(results, "Micro rad/Pixel Lower")
        rad_lower.pack()
        # Ev/Pixel
        ev = ResultBoxes(results, "EV/Pixel")
        ev.pack()
        results.pack(anchor=tk.W, pady=60, padx=10)

        # adding buttons
        button_frame = ttk.Frame(master)
        open_button = ttk.Button(button_frame, text="Open Image")
        detect_button = ttk.Button(button_frame, text="Detect")
        save_button = ttk.Button(button_frame, text="Save Data")
        reset_button = ttk.Button(button_frame, text="Reset")
        open_button.pack(side="left", padx=10, pady=10)
        detect_button.pack(side="left", padx=10, pady=10)
        save_button.pack(side="left", padx=10, pady=10)
        reset_button.pack(side="left", padx=10, pady=10)
        button_frame.pack(side="left", anchor=tk.W)

        # Dislpaying a temp image to help adjust UI
        s = ttk.Style()
        s.configure("block.TFrame", background="blue")
        block = ttk.Frame(master, style="block.TFrame", width=700, height=600)
        block.place(x=700, y=10)
