from tkinter import ttk


class ContrastAdjustmentFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=4)
        self.__create_widgets()

    def __create_widgets(self):
        self.label = ttk.Label(self, text="(2)")
        self.label.grid(column=0, row=0)
        self.button = ttk.Button(
            self,
            text="Contrast Adjustment",
            command=self.open_window
        )
        self.button.grid(column=1, row=0)
        self.path_window = ttk.Frame(self)
        self.path_window.grid(column=1, row=1)

    def open_window(self):
        contrast_root = tk.Tk()
        contrast_root.geometry("400x600")
        histogram_window = ContrastAdjustmentFrame(root)
        histogram_window.grid(column=0, row=0)
        contrast_root.mainloop()
