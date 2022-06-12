import tkinter as tk
from tkinter import Checkbutton, Entry, Label, Variable, ttk
from nrcemt.qeels.engine import qeels_engine_greeting

class plasmonSelect(ttk.Frame):
    # initializing
    def __init__(self,master,name,radio_var,x_var,y_var):
        super().__init__(master)
        self.name=name
        # creates the radio button
        self.radio_btn = ttk.Radiobutton(self,text=name,value=name,variable=radio_var,width=30)
        self.radio_btn.pack()
        
        #new frame
        frm=ttk.Frame(self)
        #creates label
        self.lbl = ttk.Label(frm,text="X: ")
        self.lbl.pack(side="left")
        
        #Creates entry box
        self.x_entry=ttk.Entry(frm,textvariable=x_var, width=7)
        self.x_entry.pack(side="left")
        
        #creates label
        self.lbl = ttk.Label(frm,text="Y: ")
        self.lbl.pack(side="left")
        
        #Creates entry box
        self.x_entry=ttk.Entry(frm,textvariable=y_var, width=7)
        self.x_entry.pack(side="left")
        
        
        frm.pack()
        
class rows(ttk.Frame):
    def __init__(self,master,name1,name2,radio_var,x1_var,y1_var,x2_var,y2_var,width,detect):
        super().__init__(master)
        #creates all asociated buttons/entrys for 1st plasmon locations
        plasmon_1=plasmonSelect(self,name1,radio_var,x1_var,y1_var)
        plasmon_1.pack(side="left",anchor=tk.NW)
        #creates all asociated buttons/entrys for 2nd plasmon locations
        plasmon_2=plasmonSelect(self,name2,radio_var,x2_var,y2_var)
        plasmon_2.pack(side="left",anchor=tk.NW)
        
        #Width
        ttk.Label(self,text="Width: ").pack(side="left",anchor=tk.W)  
        
        width_entry=ttk.Entry(self,textvariable=width,width=7)
        width_entry.pack(side="left")      
        
        detect_box=ttk.Checkbutton(self,variable=detect,text="Detect")
        detect_box.pack(side="left")