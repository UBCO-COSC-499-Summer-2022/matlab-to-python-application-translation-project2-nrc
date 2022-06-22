import tkinter as tk

BUTTON_WIDTH = 20


class ImageSetFrame(tk.LabelFrame):

    def __init__(self, master, text):
        super().__init__(master, text=text, bd=1)
        self.columnconfigure(0, weight=1)
        self.image_set_path = tk.Label(
            self, text="Path", bd=1, relief="solid", bg="white", fg="black"
        )
        self.image_set_path.grid(row=0, column=0, sticky="nwse")

        change_image_set = tk.Button(
            self,
            text="Change Image Set"
        )
        change_image_set.grid(row=1, column=0)
