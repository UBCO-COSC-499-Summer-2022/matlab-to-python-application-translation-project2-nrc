from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import numpy as np

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

        # stores info for the upper lenses
        self.upper_lenses = [
            [257.03, 63, 1.5, [0.3, 0.9, 0.65], 'C1'],
            [349, 1.5, 1, [0.3, 0.75, 0.75], 'C2'],
            [517, 1.5, 1, [0.3, 0.75, 0.75], 'C3']
        ]

        # stores info for the lower lenses
        self.lower_lenses = [
            [551.6, 1.5, -1, [0.3, 0.75, 0.75], 'OBJ'],
            [706.4, 1.5, 1, [0.3, 0.75, 0.75], 'Intermediate'],
            [826.9, 1.5, 1, [0.3, 0.75, 0.75], 'Projective']
        ]

        # stores info for the anode
        self.anode = [39.1, 30, 1.5, [0.5, 0, 0.3], 'Anode']

        # stores info for the sample
        self.sample = [528.9, 1.5, -1, [1, 0.7, 0], 'Sample']

        # stores info for the condensor aperature
        self.condensor_aperature = [192.4, 1.5, 1, [0, 0, 0], 'Cond. Apert']

        # stores info for the scintillator
        self.scintillator = [972.7, 1.5, 1, [0.3, 0.75, 0.75], 'Scintillator']

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

        # ------- Setup the Rays ---------
        # draw red dashed line on x-axis
        self.axis.axhline(0, 0, 1, color='red', linestyle='--')

        # diameter of condensor aperature
        ca_diameter = 0.02

        # 1st ray,
        # pin condenser aperture angle limited as per location and diameter
        rG = np.array([[1.5e-2],
                       [(ca_diameter/2 - 1.5e-2)/self.condensor_aperature[0]]])
        # 2nd ray, at r = 0, angle limited by CA
        rGr0 = np.array([[0], [(ca_diameter/2)/self.condensor_aperature[0]]])
        # 3rd ray, at r = tip edge, parallel to opt. axis
        rGq0 = np.array([[rG[0][0]], [0]])
        # 4th ray, at -rG, angle up to +CA edge CRAZY BEAM
        rGC = np.array([[-1*rG[0][0]],
                        [(ca_diameter/2 +
                          abs(rG[0][0]))/self.condensor_aperature[0]]])

        # add the rays into a list
        rays = [rG, rGr0, rGq0, rGC]

        # RGB color of the rays
        rG_color = [0.9, 0, 0]      # red
        rGr0_color = [0.0, 0.7, 0]  # blue
        rGq0_color = [0.0, 0, 0.8]  # green
        rGC_color = [0.7, 0.4, 0]   # gold

        # add color of each ray in same order as rays
        rayColors = [rG_color, rGr0_color, rGq0_color, rGC_color]

        # Initial focal distance of the lenses in [mm]
        Cf = [13, 35, 10.68545]

        # drawn lines representing the path of the rays
        drawnRays, Cmag, crossoverPoints = []
        for i in range(len(rays)):
            drawnRays.append(self.axis.plot([], lw=1, color=rayColors[i])[0])

        for i in range(len(Cf)):
            # text to display magnification factor of each lens
            Cmag.append(self.axis.text(Czz[i] + 5, -1, '', color='k', fontsize = FS, rotation = 'vertical', backgroundcolor = [245/255,245/255,245/255]))
            # green circle to mark the crossover point of each lens
            crossoverPoints.append(self.axis.plot([], 'go')[0])

        extremeInfo = ax.text(300,1.64,'', color = [0,0,0], fontsize = 'large', ha = 'center') #text to display extreme info
    
        # set the initial path for each of the rays
        # plotCL3 needs to be in the engine
        # calculation for UR and Cf come from engine
        # for i in range(len(rays)):
        #    drawnRays_1[i].set_data(PlotCL3(UR, Cf,
        # rays[i], fig_1, crossoverPoints_1, Cmag_1))

        # figure out this in a later pr
    """         for i in range(len(Cf)):
            # text to display magnification factor of each lens
            Cmag.append(self.axis.text(Czz[i] + 5, -1, '', color='k',
                                    fontsize=8, rotation='vertical',
                                backgroundcolor=[245/255, 245/255, 245/255]))
            # a green circle to mark the crossover point of each lens
            crossoverPoints.append(self.axis.plot([], 'go')[0])

        # text to display extreme info
        self.extremeInfo = self.axis.text(400, 2,
                                          'EXTREME beam DIAMETER @ sample:',
                                          color=[0, 0, 0], fontsize='large',
                                          ha='center'
                                          )
    """

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
