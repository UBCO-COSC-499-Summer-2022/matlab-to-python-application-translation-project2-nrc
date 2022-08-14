import tkinter as tk
from .frame_above_sample import AboveSampleFrame
from .frame_below_sample import BelowSampleFrame
from .frame_results import ResultsFrame
from .frame_diagram import DiagramFrame, CA_DIAMETER
from .common import AsyncHandler

PAD_X = 20
PAD_Y = 20


class MainWindow(tk.Tk):
    """main window for nanomi optics"""
    def __init__(self):
        """initialize window and setup widgets"""
        super().__init__()
        # set title of window
        self.title('Nanomi Optics')

        # set window size
        self.geometry('1400x800')
        self.minsize(1200, 700)
        self.columnconfigure(0, weight=1)

        # Diagram
        self.diagram = DiagramFrame(self)
        self.diagram.grid(row=1, column=0, sticky="nwse")
        self.rowconfigure(1, weight=4)

        # Results Window
        self.numerical_results = ResultsFrame(
            self, self.diagram.cf_u, self.diagram.cf_l,
            self.diagram.mag_upper, self.diagram.mag_lower,
            CA_DIAMETER, self.diagram.last_mag
        )
        self.numerical_results.grid(row=0, column=0, sticky="we")

        # Settings frame
        settings_frame = tk.Frame(self)
        settings_frame.grid(row=2, column=0, sticky="nwse")
        settings_frame.columnconfigure(0, weight=1)
        settings_frame.columnconfigure(1, weight=1)

        # Upper Settings
        async_hand_c = AsyncHandler(self.update_cf_u)
        self.upper_menu = AboveSampleFrame(settings_frame)
        self.upper_menu.grid(row=0, column=0, sticky="nwse")
        for i in range(len(self.upper_menu.links)):
            self.upper_menu.links[i].set_command(async_hand_c)
            self.upper_menu.toggles[i].set_command(self.slider_status_u)
        self.upper_menu.mode_widget.option_var.trace(
            "w", lambda a, b, c: self.u_lens_mode()
        )
        self.mode = True

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

    def update_cf_u(self, value):
        """gets the values from all the sliders and update lists"""
        self.diagram.cf_u = [
            float(i.get()) for i in self.upper_menu.links
        ]
        self.diagram.update_u_lenses()
        self.update_results()

    def slider_status_u(self, value):
        """turns slider on and off based on toggle status + name"""
        self.diagram.active_lc = [
            i.get_status() for i in self.upper_menu.toggles
        ]
        self.diagram.update_u_lenses()
        self.update_results()

    def update_cf_l(self, value):
        """update lower focal lenses"""
        self.diagram.distance_from_optical = \
            float(self.lower_menu.distance_link.get()) * (10**-6)
        self.diagram.cf_l = [
            float(i.get()) for i in self.lower_menu.links
        ]

        self.diagram.update_l_lenses(
            self.current_lens != -1, self.current_opt, self.current_lens
        )
        self.set_slider_opt()
        self.update_results()

    def slider_status_l(self, value):
        """get status for on/off lower lenses"""
        self.diagram.active_lb = [
            b.get_status() for b in self.lower_menu.buttons
        ]
        self.diagram.update_l_lenses(
            self.current_lens != -1, self.current_opt, self.current_lens
        )
        self.set_slider_opt()
        self.update_results()

    def optimization_mode(self):
        """set up optimization mode and lens index"""
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
            self.update_results()

    def set_slider_opt(self):
        """enable/disable sliders for optimization"""
        index = self.current_lens
        if index != -1:
            self.lower_menu.links[index].set(self.diagram.cf_l[index])

    def disable_lens_widgets(self, index, opt):
        """disable lens settings widgets

        Args:
            index (int): lens index to disable
            opt (bool): is it for optimization
        """
        if index != -1:
            if opt:
                self.lower_menu.buttons[index].config(
                    text="ON", state="disabled", relief=tk.SUNKEN
                )
            self.lower_menu.links[index].set_disabled(True)

    def enable_lens_widgets(self, index):
        """enable lens settings widgets

        Args:
            index (int): lens index to enable
        """
        if index != -1:
            self.lower_menu.buttons[index].config(
                text="ON", state="active", relief=tk.RAISED
            )
            self.lower_menu.links[index].set_disabled(False)

    def update_results(self):
        """update result tables"""
        self.numerical_results.update_results(
            self.diagram.cf_u, self.diagram.cf_l,
            self.diagram.mag_upper, self.diagram.mag_lower,
            CA_DIAMETER, self.diagram.last_mag
        )

    def u_lens_mode(self):
        """set upper lens mode"""
        md = self.upper_menu.mode_widget.option_var.get()
        if md == "Ur":
            self.mode = False
        elif md == "Cf":
            self.mode = True
        self.upper_menu.set_mode(self.mode)