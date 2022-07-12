import numpy as np
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from nrcemt.nanomi_optics.engine.lens import Lens


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
            [257.03, 63.5, 1.5, [0.3, 0.9, 0.65], 'C1'],
            [349, 1.5, 1, [0.3, 0.75, 0.75], 'C2'],
            [517, 1.5, 1, [0.3, 0.75, 0.75], 'C3']
        ]
        # Initial focal distance of the lenses in [mm]
        self.cf = [13, 35, 10.68545]
        self.active_lenses = [True, True, True]

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

        # Calculate UR from Cf
        # Ur = make call to engine for calculation

        for i in range(len(self.upper_lenses)):
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

        # drawn lines representing the path of the rays
        for i in range(len(RAYS)):
            self.drawn_rays.append(
                self.axis.plot(
                    [], lw=1, color=RAY_COLORS[i]
                )[0]
            )

        # text to display extreme info
        self.extreme_info = self.axis.text(
            300, 1.64, '', color=[0, 0, 0],
            fontsize='large', ha='center'
        )

        self.display_rays()
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

    def display_rays(self):
        upper_lenses_obj = []
        for i in range(len(self.upper_lenses)):
            j = 0
            if self.active_lenses[i]:
                upper_lenses_obj.append(
                    Lens(
                        self.upper_lenses[j][0],
                        self.cf[j],
                        upper_lenses_obj[j - 1].source_distance
                        if j > 0 else 0,
                        self.upper_lenses[j][0] - self.upper_lenses[j - 1][0]
                        if j > 0 else self.upper_lenses[0][0]
                    )
                )
                j += 1
        for i, lense in enumerate(upper_lenses_obj):
            self.crossover_points[i].set_data(lense.crossover_point_location())

        for i in range(len(RAYS)):
            points = []
            for j, lens in enumerate(upper_lenses_obj):
                points.extend(
                    lens.ray_path(
                        upper_lenses_obj[j - 1].out_beam_lense_vect
                        if j > 0 else RAYS[i],
                        self.c_mag
                    )
                )
            points = ([x for x, y in points], [y for x, y in points])
            self.drawn_rays[i].set_data(points)

    def update_focal_length(self, focal_values, active_lenses):
        self.cf = focal_values
        self.active_lenses = active_lenses
        self.display_rays()
        self.canvas.draw()
        self.canvas.flush_events()
