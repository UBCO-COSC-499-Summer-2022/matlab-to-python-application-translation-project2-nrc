from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

LENS_BORE = 25.4*0.1/2


# frame that holds the diagram (current values are placeholders)
class DiagramFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, borderwidth=5)

        # create figure
        self.figure = plt.figure(figsize=(8, 8), dpi=50)
        self.axis = self.figure.add_subplot()

        self.axis.axis([0, 1000, -1.8, 1.8])
        self.axis.text(275, -2.1, 'Z [mm]', color=[0, 0, 0],
                       fontsize=6)
        self.axis.set_ylabel('X [mm]', color=[0, 0, 0],
                             fontsize=6)

        # put the figure in a widget on the tk window
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.draw()

        # put the navigation toolbar in a widget on the tk window
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()

        self.canvas.get_tk_widget().pack()

        # takes in list of lens info and draws upper lenses
        for i, row in enumerate(self.upper_lenses):
            # draw C1 lens
            if i == 0:
                self.symmetrical_box(row[0], row[1], row[2], row[3], row[4])
            # draw C2, C3 lens
            else:
                self.asymmetrical_box(row[0], row[1], row[2], row[3], row[4])

        # takes in list of lens info and draws lower lenses
        for i, row in enumerate(self.lower_lenses):
            self.asymmetrical_box(row[0], row[1], row[2], row[3], row[4])

        # draws anode
        self.symmetrical_box(self.anode[0], self.anode[1], self.anode[2],
                             self.anode[3], self.anode[4])

        # draws sample
        self.sample_aperature_box(self.sample[0], self.sample[1],
                                  self.sample[2], self.sample[3],
                                  self.sample[4])

        # draws condensor aperature
        self.sample_aperature_box(self.condensor_aperature[0],
                                  self.condensor_aperature[1],
                                  self.condensor_aperature[2],
                                  self.condensor_aperature[3],
                                  self.condensor_aperature[4])

        # draws scintillator
        self.asymmetrical_box(self.scintillator[0],
                              self.scintillator[1],
                              self.scintillator[2],
                              self.scintillator[3],
                              self.scintillator[4])

    # draws symmetrical box
    def symmetrical_box(self, x, w, h, colour, name):
        # x = location of centre point of box along x-axis
        # w = width, h = height, colour = color

        # rectangle box
        self.axis.add_patch(Rectangle(
            (x-w/2, -h), w, h*2, edgecolor=colour,
            facecolor='none', lw=1))
        # top lens bore (horizontal line)
        self.axis.hlines(LENS_BORE, x-w/2, x+w/2, colors=colour)
        # bottom lens bore (horizontal line)
        self.axis.hlines(-LENS_BORE, x-w/2, x+w/2, colors=colour)
        # electrode location in lens
        self.axis.vlines(x, -h, h, colors=colour, linestyles='--')

        self.axis.text(
            x, -h+0.05, name, fontsize=8,
            rotation='vertical', ha='center'
            )
        return

    # draws an asymmetrical box
    def asymmetrical_box(self, x, h, position, colour, name):
        # x = location of center point along (true) x-axis
        # h = height, colour = color
        # Short, Long distance from mid electrode to face of lens in [mm]
        # set position = 1 for nose (dashed line) on right
        # set position = -1 for nose (dashed line) on left

        # Short, Long distance from mid holder to sample [mm]
        long = 52.2   # mm
        short = 11.6  # mm

        self.axis.add_patch(
            Rectangle(
                (x+position*short, -h), -position*long-position*short,
                2*h, edgecolor=colour, facecolor='none', lw=1
            )
        )
        # electrode Location in lens
        self.axis.vlines(x, -h, h, colors=colour, linestyles='--')
        # bottom lens bore
        self.axis.hlines(-LENS_BORE, x-long, x+short, colors=colour)
        # top lens bore
        self.axis.hlines(LENS_BORE, x-long, x+short, colors=colour)

        self.axis.text(
            x-position*10, -h+0.05, name, fontsize=8,
            rotation='vertical', ha='center'
            )
        return

    # draws box for sample and condensor aperature
    def sample_aperature_box(self, x, h, position, colour, name):
        # x = location of center point along (true) x-axis
        # h = height
        # colour = colour expressed as [r,g,b], where r,g,b are b/w 0 to 1
        # set position = 1 for nose (dashed line) on right
        # set position = -1 for nose (dashed line) on left

        # Short, Long distance from mid holder to sample [mm]
        long = 25  # mm
        short = 3  # mm

        self.axis.add_patch(
            Rectangle(
                (x+position*short, -h), -position*long-position*short,
                2*h, edgecolor=colour, facecolor='none', lw=1
            )
        )
        # electrode location in lens
        self.axis.vlines(x, h, -h, colors=colour, linestyle='--')
        self.axis.text(
            x-position*10, -h+0.05, name,
            fontsize=8, ha='center', rotation='vertical'
        )
        return
