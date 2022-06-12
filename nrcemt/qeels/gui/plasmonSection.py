import tkinter as tk
from tkinter import ttk
from nrcemt.qeels.engine import qeels_engine_greeting

class plasmonSelect(ttk.Frame):
    # initializing
    def __init__(self,master,name,fsize):
        #font size
        self.fsize=fsize
        
        #padding
        self.xpad=5
        self.ypad=5
        super().__init__(master)
        self.name=name
        #new frame
        frm=ttk.Frame(self)
        
        #creates styling for radio buttons
        ttk.Style(self).configure("TRadiobutton",font=self.fsize)
        # creates the radio button
        self.radio_btn = ttk.Radiobutton(self,text=name,width=25)
        self.radio_btn.pack(anchor=tk.W)

        #creates label
        self.lbl = ttk.Label(frm,text="X: ",font=self.fsize)
        self.lbl.pack(side="left",padx=self.xpad,pady=self.ypad)
        
        #Creates entry box
        self.x_entry=ttk.Entry(frm, width=7)
        self.x_entry.pack(side="left",padx=self.xpad,pady=self.ypad)
        
        #creates label
        self.lbl = ttk.Label(frm,text="Y: ",font=self.fsize)
        self.lbl.pack(side="left",padx=self.xpad,pady=self.ypad)
        
        #Creates entry box
        self.x_entry=ttk.Entry(frm, width=7)
        self.x_entry.pack(side="left",padx=self.xpad,pady=self.ypad)
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

class result_boxes(ttk.Frame):
    def __init__(self,master,name,fsize):
        super().__init__(master)
        ev_label=ttk.Label(self,text=name + ": ",font=fsize,width=20)
        ev_entry=ttk.Entry(self,width=7)
        ev_label.pack(side="left")
        ev_entry.pack(side="left")