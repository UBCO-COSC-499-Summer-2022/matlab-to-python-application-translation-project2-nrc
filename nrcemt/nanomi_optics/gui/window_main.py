import tkinter as tk
from .frame_above_sample import AboveSampleFrame
from .frame_below_sample import BelowSampleFrame
from .frame_results import ResultsFrame
from .frame_diagram import DiagramFrame
from nrcemt.common.gui.async_handler import AsyncHandler

PAD_X = 20
PAD_Y = 20


class MainWindow(tk.Tk):

    def __init__(self):
        super().__init__()
        # set title of window
        self.title('Nanomi Optics')

        # set window size
        self.geometry('1200x600')
        self.minsize(1200, 600)
        self.columnconfigure(0, weight=1)

        # Results Window
        numerical_results = ResultsFrame(self)
        numerical_results.grid(row=0, column=0, sticky="we")

        # Diagram
        self.diagram = DiagramFrame(self)
        self.diagram.grid(row=1, column=0, sticky="nwse")
        self.rowconfigure(1, weight=4)

        settings_frame = tk.Frame(self)
        settings_frame.grid(row=2, column=0, sticky="nwse")
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)

        # Upper Settings
        async_hand_c = AsyncHandler(self.update_cf_u)
        self.upper_menu = AboveSampleFrame(settings_frame)
        self.upper_menu.grid(row=0, column=0, sticky="nwse")
        self.upper_menu.c1_link.set_command(async_hand_c)
        self.upper_menu.c1_toggle.set_command(self.slider_status_u)
        self.upper_menu.c2_link.set_command(async_hand_c)
        self.upper_menu.c2_toggle.set_command(self.slider_status_u)
        self.upper_menu.c3_link.set_command(async_hand_c)
        self.upper_menu.c3_toggle.set_command(self.slider_status_u)

        # Lower Settings
        async_hand_l = AsyncHandler(self.update_cf_l)
        self.lower_menu = BelowSampleFrame(settings_frame)
        self.lower_menu.grid(row=0, column=1, sticky="nwse")
        self.lower_menu.distance_link.set_command(async_hand_l)
        for i in range(len(self.lower_menu.sliders)):
            self.lower_menu.links[i].set_command(async_hand_l)
            self.lower_menu.buttons[i].set_command(self.slider_status_l)
        self.lower_menu.opt_sel.trace(
            "w", lambda a, b, c: self.optimization_mode()
        )
        self.lower_menu.lens_sel.trace(
            "w", lambda a, b, c: self.optimization_mode()
        )
        self.current_opt = "Image"
        self.current_lens = -1
        self.last_lens = -1

    # gets the values from all the slides and update lists
    def update_cf_u(self, value):
        self.diagram.cf_u = [
            float(self.upper_menu.c1_link.get()),
            float(self.upper_menu.c2_link.get()),
            float(self.upper_menu.c3_link.get())
        ]
        self.diagram.update_u_lenses()

    # turns slider on and off based on toggle status + name
    def slider_status_u(self, value):
        self.diagram.active_lc = [
            self.upper_menu.c1_toggle.get_status(),
            self.upper_menu.c2_toggle.get_status(),
            self.upper_menu.c3_toggle.get_status()
        ]
        self.diagram.update_u_lenses()

    def update_cf_l(self, value):
        self.diagram.distance_from_optical = \
            float(self.lower_menu.distance_link.get()) * (10**-6)
        self.diagram.cf_l = [
            float(i.get()) for i in self.lower_menu.links
        ]

        self.diagram.update_l_lenses(
            self.current_lens != -1, self.current_opt, self.current_lens
        )
        self.set_slider_opt()

    def slider_status_l(self, value):
        self.diagram.active_lb = [
            b.get_status() for b in self.lower_menu.buttons
        ]
        self.diagram.update_l_lenses(
            self.current_lens != -1, self.current_opt, self.current_lens
        )
        self.set_slider_opt()

    def optimization_mode(self):
        self.enable_lens_widgets(self.current_lens)
        self.diagram.active_lb[self.current_lens] = True
        self.current_lens = self.lower_menu.lens_sel.get()
        self.current_opt = self.lower_menu.opt_sel.get()

        if self.current_lens != -1:
            self.disable_lens_widgets(self.current_lens, True)
            self.diagram.update_l_lenses(
                True, self.current_opt, self.current_lens
            )
            self.set_slider_opt()

    def set_slider_opt(self):
        index = self.current_lens
        if index != -1:
            self.lower_menu.links[index].set(self.diagram.cf_l[index])

    def disable_lens_widgets(self, index, opt):
        if index != -1:
            if opt:
                self.lower_menu.buttons[index].config(
                    text="ON", state="disabled", relief=tk.SUNKEN
                )
            self.lower_menu.links[index].set_disabled(True)

    def enable_lens_widgets(self, index):
        if index != -1:
            self.lower_menu.buttons[index].config(
                text="ON", state="active", relief=tk.RAISED
            )
            self.lower_menu.links[index].set_disabled(False)
