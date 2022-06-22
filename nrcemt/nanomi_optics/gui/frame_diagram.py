from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
# 2D array that holds info for the upper lenses
UPPER_LENSES = ([[257.03, 63, 1.5, [0.3, 0.9, 0.65], 'C1'],
                 [349, 1.5, [0.3, 0.75, 0.75], 'C2'],
                 [517, 1.5, [0.3, 0.75, 0.75], 'C3']])


# frame that holds the diagram (current values are placeholders)
class DiagramFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, borderwidth=5)

        # create figure
        fig = plt.figure(figsize=(8, 8), dpi=50)
        ax = fig.add_subplot()

        # x and y axis
        ax.axis([0, 600, -1.8, 1.8])
        ax.text(275, -2.1, 'Z [mm]', color=[0, 0, 0],
                fontsize=6)
        ax.set_ylabel('X [mm]', color=[0, 0, 0],
                      fontsize=6)

        # draw upper lenses
        # draw C1 Lens
        # 2D array that hold values for each lens
        # self.symmetrical_box(257.03, 63, 1.5, [0.3, 0.9, 0.65], 'C1', ax)
        # self.asymmetrical_box(349, 1.5, [0.3, 0.75, 0.75], 'C2', ax)

        # takes in list of lense info and makes lenses
        for i, row in enumerate(UPPER_LENSES):
            if i == 0:
                self.symmetrical_box(row[0], row[1], row[2], row[3], row[4], ax)
            else:
                self.asymmetrical_box(row[0], row[1], row[2], row[3], ax)

        # put the figure in a widget on the tk window
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # put the navigation toolbar in a widget on the tk window
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()

        canvas.get_tk_widget().pack()
        # plt.show()

    # draws symmetrical box
    def symmetrical_box(self, x, w, h, colour, name, ax):
        # x = location of centre point of box along x-axis
        # w = width, h = height, colour = color

        # smaller diameter lens bore (ground outer electrodes)
        lens_bore = 25.4*0.1/2

        # rectangle box
        ax.add_patch(Rectangle(
            (x-w/2, -h), w, h*2, edgecolor=colour,
            facecolor='none', lw=1))
        # top lens bore (horizontal line)
        ax.hlines(lens_bore, x-w/2, x+w/2, colors=colour)
        # bottom lens bore (horizontal line)
        ax.hlines(-lens_bore, x-w/2, x+w/2, colors=colour)
        # electrode location in lens
        ax.vlines(x, -h, h, colors=colour, linestyles='--')

        ax.text(x, -h-0.2, name, fontsize=8,
                rotation='horizontal', ha='center')
        return

    # draws an asymmetrical box
    def asymmetrical_box(self, x, h, colour, name, ax):
        # x = location of center point along (true) x-axis
        # h = height, colour = color
        # Short, Long distance from mid electrode to face of lens in [mm]
        long = 52.2   # mm
        short = 11.6  # mm

        # smaller diameter lens bore (ground outer electrodes)
        lens_bore = 25.4*0.1/2

        ax.add_patch(Rectangle((x+short, -h), -long-short,
                               2*h, edgecolor=colour, facecolor='none', lw=1))
        # Electrode Location in lens
        ax.vlines(x, -h, h, colors=colour, linestyles='--')
        # bottom lens bore
        ax.hlines(-lens_bore, x-long, x+short, colors=colour)
        # top lens bore
        ax.hlines(lens_bore, x-long, x+short, colors=colour)

        ax.text(x, -h-0.2, name, fontsize=8,
                rotation='horizontal', ha='center')
        return

    # draws box for sample and condensor aperature
    def sample_aperature_box(self, x, h, position, colour, name, ax):
        # x = location of center point along (true) x-axis
        # h = height
        # colour = colour expressed as [r,g,b], where r,g,b are b/w 0 to 1
        # set position = 1 for nose (dashed line) on right
        # set position = -1 for nose on left

        # Short, Long distance from mid holder to sample [mm]
        long = 25  # mm
        short = 3  # mm

        ax.add_patch(Rectangle((x+position*short, -h),
                               -position*long-position*short,
                               2*h, edgecolor=colour, facecolor='none', lw=1))
        # electrode location in lens
        ax.vlines(x, h, -h, colors=colour, linestyle='--')
        ax.text(x-position*10, -h-0.2, name, color=colour, fontsize=8,
                ha='center', rotation='horizontal')
        return
