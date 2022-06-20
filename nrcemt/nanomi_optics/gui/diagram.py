from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# frame that holds the diagram (current values are placeholders)
class ResultsLayout(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, borderwidth=5)

        # draws a box on x-axis
        def C1Box(x, w, h, col, text, ax):
            # x = location of centre point of box along x-axis
            # w = width, h = height, col = color

            # smaller diameter lens bore (ground outer electrodes)
            lens_bore = 25.4*0.1/2

            # rectangle box
            ax.add_patch(Rectangle(
                (x-w/2, -h), w, h*2, edgecolor=col,
                facecolor='none', lw=1))
            # top lens bore
            ax.hlines(lens_bore, x-w/2, x+w/2, colors=col)
            # bottom lens bore
            ax.hlines(-lens_bore, x-w/2, x+w/2, colors=col)
            # electrode location in lens
            ax.vlines(x, -h, h, colors=col, linestyles='--')

            ax.text(x, -h-0.2, text, fontsize=8,
                    rotation='horizontal', ha='center')
            return

        # plot
        def diagramming():

            fig = plt.figure()
            ax = fig.add_subplot()
            fig.subplots_adjust(top=0.88, bottom=0.18)

            # x and y axis
            ax.axis([0, 600, -1.8, 1.8])
            ax.text(275, -2.1, 'Z [mm]', color=[0, 0, 0],
                    fontsize=8*1.2)
            ax.set_ylabel('X [mm]', color=[0, 0, 0],
                          fontsize=8*1.2)

            # draw upper lenses
            # draw C1 Lens
            C1Box(257, 63, 1.5, [0.3, 0.9, 0.65], 'C1', ax)

            plt.show()
