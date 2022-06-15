import tkinter as tk


class ContrastAdjustmentWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        self.geometry("400x600")
        self.__create_widgets()
