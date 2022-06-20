from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)


# frame that holds the diagram (current values are placeholders)
class DiagramLayout(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, borderwidth=5)

        # draws symmetrical box, C1 lens
        def C1Lens(x, w, h, col, text, ax):
            # x = location of centre point of box along x-axis
            # w = width, h = height, col = color

            # smaller diameter lens bore (ground outer electrodes)
            lens_bore = 25.4*0.1/2

            # rectangle box
            ax.add_patch(Rectangle(
                (x-w/2, -h), w, h*2, edgecolor=col,
                facecolor='none', lw=1))
            # top lens bore (horizontal line)
            ax.hlines(lens_bore, x-w/2, x+w/2, colors=col)
            # bottom lens bore (horizontal line)
            ax.hlines(-lens_bore, x-w/2, x+w/2, colors=col)
            # electrode location in lens
            ax.vlines(x, -h, h, colors=col, linestyles='--')

            ax.text(x, -h-0.2, text, fontsize=8,
                    rotation='horizontal', ha='center')
            return

        # Simply draws an asymetric box for the lenses C2, C3
        def LBoxA(x, h, col, text, ax):
            # x = location of center point along (true) x-axis
            # h = height, col = color
            # Shrt, Lng distance from mid electrode to face of lens in [mm]
            Lng = 52.2   # mm
            Shrt = 11.6  # mm

            # smaller diameter lens bore (ground outer electrodes)
            Lbore = 25.4*0.1/2

            ax.add_patch(Rectangle((x+Shrt, -h), -Lng-Shrt,
                                   2*h, edgecolor=col, facecolor='none', lw=1))
            # Electrode Location in lens
            ax.vlines(x, -h, h, colors=col, linestyles='--')
            # bottom lens bore
            ax.hlines(-Lbore, x-Lng, x+Shrt, colors=col)
            # top lens bore
            ax.hlines(Lbore, x-Lng, x+Shrt, colors=col)
 
            ax.text(x, -h-0.2, text, fontsize=8,
                    rotation='horizontal', ha='center')
            return

        # create figure
        fig = plt.figure()
        ax = fig.add_subplot()

        # x and y axis
        ax.axis([0, 600, -1.8, 1.8])
        ax.text(275, -2.1, 'Z [mm]', color=[0, 0, 0],
                fontsize=6)
        ax.set_ylabel('X [mm]', color=[0, 0, 0],
                      fontsize=6)

        # draw upper lenses
        # draw C1 Lens
        C1Lens(257, 63, 1.5, [0.3, 0.9, 0.65], 'C1', ax)

        # put the figure in a widget on the tk window
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # put the navigation toolbar in a widget on the tk window
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()

        canvas.get_tk_widget().pack()
        # plt.show()
