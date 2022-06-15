from tkinter import ttk


class ImageAdjustmentFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)

        # Create input widgets
        input_labels = [
            "Offset X (pixel)",
            "Offset Y (pixel)",
            "Angle (degree)"
        ]
        for i, label in enumerate(input_labels):
            label = ttk.Label(self, text=label)
            label.grid(column=0, row=i)
            input = ttk.Entry(self, width=10)
            input.grid(column=1, row=i)

        # Create slider widget
        self.__create_radio("Binning", 3)

        # Create checkbox widget
        sobel = ttk.Checkbutton(self, text="Use Sobel")
        sobel.grid(column=0, row=4)

        self.grid(column=0, row=0)

    def __create_radio(self, text, i):
        label = ttk.Label(self, text=text)
        label.grid(column=0, row=i)

        # Create frame to contain radio buttons
        radio_frame = ttk.Frame(self)
        radio_frame.grid(column=1, row=i)
        for i in range(4):
            radio = ttk.Radiobutton(
                radio_frame,
                text=f"{2**(i+1)}"
            )
            radio.grid(column=i, row=0)
