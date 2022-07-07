import numpy as np
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
<<<<<<< HEAD
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
=======
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
import numpy as np
from nrcemt.nanomi_optics.engine.lense import Lense
>>>>>>> 9f0860a (Output between two lenses)


LENS_BORE = 25.4*0.1/2

# diameter of condensor aperature
CA_DIAMETER = 0.02

# stores info for the condensor aperature
CONDENSOR_APERATURE = [192.4, 1.5, 1, [0, 0, 0], 'Cond. Apert']

# add color of each ray in same order as rays
# red, blue, green, gold
RAY_COLORS = [[0.9, 0, 0], [0.0, 0.7, 0], [0.0, 0, 0.8], [0.7, 0.4, 0]]

# pin condenser aperture angle limited as per location and diameter
RAYS = [
    np.array(
        [[1.5e-2], [(CA_DIAMETER/2 - 1.5e-2) / CONDENSOR_APERATURE[0]]]
    ),
    # 2nd ray, at r = 0, angle limited by CA
    np.array(
        [[0], [(CA_DIAMETER/2) / CONDENSOR_APERATURE[0]]]
    ),
    # 3rd ray, at r = tip edge, parallel to opt. axis
    np.array(
        [[1.5e-2], [0]]
    ),
    # 4th ray, at -rG, angle up to +CA edge CRAZY BEAM
    np.array(
        [[-1*1.5e-2], [(CA_DIAMETER/2 + 1.5e-2) / CONDENSOR_APERATURE[0]]]
    )
]


# frame that holds the diagram (current values are placeholders)
class DiagramFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, borderwidth=5)

        # create figure
        self.figure = Figure(figsize=(8, 8), dpi=100)
        self.axis = self.figure.add_subplot()

        self.axis.axis([0, 1000, -1.8, 1.8])
        self.axis.text(
            275, -2.1, 'Z [mm]', color=[0, 0, 0], fontsize=6
        )
        self.axis.set_ylabel(
            'X [mm]', color=[0, 0, 0], fontsize=6
        )

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
        # Initial focal distance of the lenses in [mm]
        self.cf = [13, 35, 10.68545]

        self.c1 = Lense(
            self.upper_lenses[0][0],
            self.cf[0],
            0,
            self.upper_lenses[0][0]
        )
        self.c2 = Lense(
            self.upper_lenses[1][0],
            self.cf[1],
            self.c1.source_distance,
            self.upper_lenses[1][0] - self.upper_lenses[0][0]
        )
        self.c3 = Lense(
            self.upper_lenses[2][0],
            self.cf[2],
            self.c2.source_distance,
            self.upper_lenses[2][0] - self.upper_lenses[1][0]
        )
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
        self.symmetrical_box(
            self.anode[0], self.anode[1], self.anode[2],
            self.anode[3], self.anode[4]
        )

        # draws sample
        self.sample_aperature_box(
            self.sample[0], self.sample[1], self.sample[2],
            self.sample[3], self.sample[4]
        )

        # draws condensor aperature
        self.sample_aperature_box(
            CONDENSOR_APERATURE[0], CONDENSOR_APERATURE[1],
            CONDENSOR_APERATURE[2], CONDENSOR_APERATURE[3],
            CONDENSOR_APERATURE[4]
        )

        # draws scintillator
        self.asymmetrical_box(
            self.scintillator[0], self.scintillator[1],
            self.scintillator[2], self.scintillator[3],
            self.scintillator[4]
        )

        # ------- Setup the Rays ---------
        # draw red dashed line on x-axis
        self.axis.axhline(0, 0, 1, color='red', linestyle='--')

        # variables that will later be updated
        self.drawn_rays, self.c_mag, self.crossover_points = [], [], []

<<<<<<< HEAD
        # Initial focal distance of the lenses in [mm]
        self.cf = [13, 35, 10.68545]
=======
>>>>>>> 9f0860a (Output between two lenses)

        # Calculate UR from Cf
        # Ur = make call to engine for calculation

<<<<<<< HEAD
        for i in range(len(self.cf)):
=======
        for i in range(len(self.upper_lenses)):
>>>>>>> 9f0860a (Output between two lenses)
            # text to display magnification factor of each lens
            self.c_mag.append(
                self.axis.text(
                    self.upper_lenses[i][0] + 5,
                    -1, '', color='k', fontsize=8,
                    rotation='vertical',
                    backgroundcolor=[245/255, 245/255, 245/255]
                )
            )
            # green circle to mark the crossover point of each lens
            self.crossover_points.append(self.axis.plot([], 'go')[0])

<<<<<<< HEAD
=======
        # for i in range(self.upper_lenses):

>>>>>>> 9f0860a (Output between two lenses)
        # drawn lines representing the path of the rays
        for i in range(len(RAYS)):
            self.drawn_rays.append(
                self.axis.plot(
                    [], lw=1, color=RAY_COLORS[i]
                )[0]
            )
<<<<<<< HEAD
            # set the initial path for the rays
            # self.drawn_rays[i].set_data(draw_ray(UR, Cf, RAYS[i],
            # self.fig, self.crossover_points, self.c_mag_1))
        self.drawn_rays[0].set_data(
            [
                0, 257.03, 257.03, 270.72253780272916,
                257.03, 349.0, 349, 387.9012738853503,
                349, 517, 517, 527.910959698867,
                517, 528.9
            ],
            [
                0.015, 0.008320426195426197,
                0.008320426195426197, -0.0007990820800721221,
                0.008320426195426197, -0.05293346173836562,
                -0.05293346173836562, -0.020008811875395355,
                -0.05293346173836562, 0.08925574248360797,
                0.08925574248360797, 0.007350960601603784,
                0.08925574248360797, -7.342115513725433e-05
            ]
        )
        self.drawn_rays[1].set_data(
            [
                0, 257.03, 257.03, 270.72253780272916,
                257.03, 349.0, 349, 387.9012738853503,
                349, 517, 517, 527.910959698867,
                517, 528.9
            ],
            [
                0.0, 0.013359147609147609,
                0.013359147609147609, 0.0,
                0.013359147609147609, -0.07637153806173042,
                -0.07637153806173042, -0.029441342442251932,
                -0.07637153806173042, 0.12630236118663052,
                0.12630236118663052, 0.010497365439609885,
                0.12630236118663052, 4.796915628602072e-08
            ]
        )
        self.drawn_rays[2].set_data(
            [
                0, 257.03, 257.03, 270.72253780272916,
                257.03, 349.0, 349, 387.9012738853503,
                349, 517, 517, 527.910959698867,
                517, 528.9
            ],
            [
                0.015, 0.015,
                0.015, -0.0007990820800721221,
                0.015, -0.09111923076923081,
                -0.09111923076923081, -0.03472948309652131,
                -0.09111923076923081, 0.15240692307692322,
                0.15240692307692322, 0.012599643321408727,
                0.15240692307692322, -7.339717055909745e-05
            ]
        )

        self.drawn_rays[3].set_data(
            [
                0, 257.03, 257.03, 270.72253780272916,
                257.03, 349.0, 349, 387.9012738853503,
                349, 517, 517, 527.910959698867,
                517, 528.9
            ],
            [
                -0.015, 0.018397869022869023,
                0.018397869022869023, 0.0007990820800721256,
                0.018397869022869023, -0.0998096143850952,
                -0.0998096143850952, -0.03887387300910849,
                -0.0998096143850952, 0.1633489798896531,
                0.1633489798896531, 0.013643770277615985,
                0.1633489798896531, 7.351709344982638e-05
            ]
        )
=======

        self.crossover_points[0].set_data(self.c1.crossover_point_location())
        self.crossover_points[1].set_data(self.c2.crossover_point_location())
        for i in range(len(RAYS)):
            points = self.c1.ray_path(RAYS[i], self.c_mag)
            points.extend(
                self.c2.ray_path(self.c1.out_beam_lense_vect, self.c_mag)
            )
<<<<<<< HEAD
>>>>>>> 9f0860a (Output between two lenses)
=======
            points.extend(
                self.c3.ray_path(self.c2.out_beam_lense_vect, self.c_mag)
            )
            points = ([x for x, y in points], [y for x, y in points])
            self.drawn_rays[i].set_data(points)
>>>>>>> 8de51b7 (Create lense instance to test)

        # text to display extreme info
        self.extreme_info = self.axis.text(
            300, 1.64, '', color=[0, 0, 0],
            fontsize='large', ha='center'
        )

        # set the initial extreme information
        # self.extreme_info.set_text('EXTREME beam DIAMETER @ sample
        # = {:.2f}'.format(routMax[0][0]*1e6*2)
        # + ' nm  & convergence SEMI angle = {:.2f}'.format(routMax[1][0]*1e3)
        # + ' mrad')

    # draws symmetrical box
    def symmetrical_box(self, x, w, h, colour, name):
        # x = location of centre point of box along x-axis
        # w = width, h = height, colour = color

        # rectangle box
        self.axis.add_patch(
            Rectangle(
                (x-w/2, -h), w, h*2, edgecolor=colour,
                facecolor='none', lw=1
            )
        )
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