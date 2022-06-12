import tkinter as tk
from tkinter import Entry, Label, ttk
from typing import Text
from nrcemt.qeels.engine import qeels_engine_greeting
from plasmonSection import *



def main():
    size=25
    root = tk.Tk()
    # set title
    root.title("qEEls peak detection")
    
    # setting size of window(will change later)
    root.geometry("1500x700+10+0")   

    #THESE MIGHT NEED TO BE PUT IN A GRID
    inputs=ttk.Frame(root)
    #Bulk Plasmons  
    bulk_plasmon1=plasmonSelect(inputs,"Bulk Plasmon 1",size)
    bulk_plasmon2=plasmonSelect(inputs,"Bulk Plasmon 2",size)
    bulk_plasmon1.grid(row=0,column=0,padx=10,pady=10)
    bulk_plasmon2.grid(row=0,column=1,padx=10,pady=10)
    
    #Surface Plasmon Upper
    upper_plasmon1=plasmonSelect(inputs,"Surface Plasmon Upper 1",size)
    upper_plasmon2=plasmonSelect(inputs,"Surface Plasmon Upper 2",size)
    upper_plasmon1.grid(row=1,column=0,padx=10,pady=10)
    upper_plasmon2.grid(row=1,column=1,padx=10,pady=10)

    #Surface Plasmon Lower
    lower_plasmon1=plasmonSelect(inputs,"Surface Plasmon Lower 1",size)
    lower_plasmon2=plasmonSelect(inputs,"Surface Plasmon Lower 2",size)
    lower_plasmon1.grid(row=2,column=0,padx=10,pady=10)
    lower_plasmon2.grid(row=2,column=1,padx=10,pady=10)
    inputs.pack(anchor=tk.NW)
    
    #Average Pixel
    average_pixel=result_boxes(root,"Average Pixel",size)
    average_pixel.pack()
    #Micro rad/pixel upper
    rad_upper=result_boxes(root,"Micro rad/Pixel Upper",size)
    rad_upper.pack()
    #Micro rad/pixel lower
    rad_lower=result_boxes(root,"Micro rad/Pixel Lower",size)
    rad_lower.pack()
    #Ev/Pixel
    ev=result_boxes(root,"EV/Pixel",size)
    ev.pack()

    
    
    
    #adding buttons
    button_frame=ttk.Frame(root)
    ttk.Style(button_frame).configure("TButton",font=size)

    open_button=ttk.Button(button_frame,text="Open Image")
    detect_button=ttk.Button(button_frame,text="Detect")
    save_button=ttk.Button(button_frame,text="Save Data")
    reset_button=ttk.Button(button_frame,text="Reset")
    
    open_button.pack(side="left",padx=10,pady=10)
    detect_button.pack(side="left",padx=10,pady=10)
    save_button.pack(side="left",padx=10,pady=10)
    reset_button.pack(side="left",padx=10,pady=10)
    
    button_frame.pack(side="left",anchor=tk.W)
    root.mainloop()
 
if __name__ == "__main__":
    main()
