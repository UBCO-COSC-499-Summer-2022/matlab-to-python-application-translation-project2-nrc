from tkinter import ttk


class ImageAdjustmentFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)

        # Create input widgets
        input_label = [
            "Offset X (pixel)",
            "Offset Y (pixel)",
            "Angle (degree)"
        ]
        for i in range(3):
            self.__create_subwidget_input(
                self,
                input_label[i],
                i
            )

        # Create slider widget
        self.__create_subwidget_radio_buttons(
            self,
            "Binning",
            3
        )

        # Create checkbox widget
        self.__create_subwidget_checkbox(
            self,
            "Use Sobel",
            4
        )

        self.grid(column=0, row=0)

    def __create_subwidget_input(self, master, text, i):
        label = ttk.Label(
            master, text=text)
        label.grid(column=0, row=i)
        input = ttk.Entry(master, width=10)
        input.grid(column=1, row=i)

    def __create_subwidget_radio_buttons(self, master, text, i):
        label = ttk.Label(master, text=text)
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

    def __create_subwidget_checkbox(self, master, text, i):
        cb = ttk.Checkbutton(master, text=text)
        cb.grid(column=0, row=i)
