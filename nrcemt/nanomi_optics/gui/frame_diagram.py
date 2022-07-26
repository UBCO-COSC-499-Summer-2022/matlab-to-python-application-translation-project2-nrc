import numpy as np
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
from nrcemt.nanomi_optics.engine.lens import Lens
from nrcemt.nanomi_optics.engine.optimization import optimize_focal_length

LAMBDA_ELECTRON = 0.0112e-6

LENS_BORE = 25.4*0.1/2

# diameter of condensor aperature
CA_DIAMETER = 0.01

# stores info for the anode
ANODE = [39.1, 30, 1.5, [0.5, 0, 0.3], 'Anode']

# stores info for the sample
SAMPLE = [528.9, 1.5, -1, [1, 0.7, 0], 'Sample']

# stores info for the scintillator
SCINTILLATOR = [972.7, 1.5, 1, [0.3, 0.75, 0.75], 'Scintillator']

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


# stores info for the lower lenses
LOWER_LENSES = [
    [551.6, 1.5, -1, [0.3, 0.75, 0.75], 'Objective'],
    [706.4, 1.5, 1, [0.3, 0.75, 0.75], 'Intermediate'],
    [826.9, 1.5, 1, [0.3, 0.75, 0.75], 'Projective']
]

# stores info for the upper lenses
UPPER_LENSES = [
    [257.03, 63.5, 1.5, [0.3, 0.9, 0.65], 'C1'],
    [349, 1.5, 1, [0.3, 0.75, 0.75], 'C2'],
    [517, 1.5, 1, [0.3, 0.75, 0.75], 'C3']
]


# frame that holds the diagram (current values are placeholders)
class DiagramFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master, borderwidth=5)

        # create figure
        self.figure = Figure(figsize=(10, 10))
        self.axis = self.figure.add_subplot()
        # self.axis.axis([0, 1000, -1.8, 1.8])

        self.axis.text(
            275, -2.1, 'X [mm]', color=[0, 0, 0], fontsize=6
        )
        self.axis.set_ylabel(
            'Z [mm]', color=[0, 0, 0], fontsize=6
        )
        # plt.savefig("image.png",bbox_inches='tight',dpi=100)

        # put the figure in a widget on the tk window
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.redraw()

        # put the navigation toolbar in a widget on the tk window
        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()

        self.x_min, self. x_max, self.y_min, self.y_max = 0, 0, 0, 0
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        # Initial focal distance of the lenses in [mm]
        self.cf_c = [67.29, 22.94, 39.88]
        self.cf_b = [19.67, 6.498, 6]
        self.active_lenses_c = [True, True, True]
        self.active_lenses_b = [True, True, True]

        # sample rays
        self.distance_from_optical = 0.00001
        self.scattering_angle = 0
        self.sample_rays = []
        self.update_b_rays()
        # takes in list of lens info and draws upper lenses
        for i, row in enumerate(UPPER_LENSES):
            # draw C1 lens
            if i == 0:
                self.symmetrical_box(*row)
            # draw C2, C3 lens
            else:
                self.asymmetrical_box(*row)

        # draws anode
        self.symmetrical_box(*ANODE)

        # draws sample
        self.sample_aperature_box(*SAMPLE)

        # draws condensor aperature
        self.sample_aperature_box(*CONDENSOR_APERATURE)

        # draws scintillator
        self.asymmetrical_box(*SCINTILLATOR)

        # ------- Setup the Rays ---------
        # draw red dashed line on x-axis
        self.axis.axhline(0, 0, 1, color='red', linestyle='--')

        # variables that will later be updated
        self.drawn_rays_c, self.drawn_rays_b, self.c_mag = [], [], []

        # crossover points arrays
        self.crossover_points_c, self.crossover_points_b = [], []

        # Calculate UR from Cf
        # Ur = make call to engine for calculation

        for i in range(len(UPPER_LENSES)):
            # text to display magnification factor of each lens
            self.c_mag.append(
                self.axis.text(
                    UPPER_LENSES[i][0] + 5,
                    -1, '', color='k', fontsize=8,
                    rotation='vertical',
                    backgroundcolor=[245/255, 245/255, 245/255]
                )
            )
            # green circle to mark the crossover point of each lens
            self.crossover_points_c.append(self.axis.plot([], 'go')[0])

        # takes in list of lens info and draws lower lenses
        for row in LOWER_LENSES:
            self.asymmetrical_box(*row)
            self.crossover_points_b.append(self.axis.plot([], 'go')[0])

        # drawn lines representing the path of the rays
        for i in range(len(RAYS)):
            for j in range(len(UPPER_LENSES)):
                self.drawn_rays_c.append(
                    self.axis.plot(
                        [], lw=1, color=RAY_COLORS[i]
                    )[0]
                )
                self.drawn_rays_c.append(
                    self.axis.plot(
                        [], lw=3, color=RAY_COLORS[i]
                    )[0]
                )
                self.drawn_rays_c.append(
                    self.axis.plot(
                        [], lw=1, color="r"
                    )[0]
                )
        for i in range(len(self.sample_rays)):
            for j in range(len(LOWER_LENSES)):
                self.drawn_rays_b.append(
                    self.axis.plot(
                        [], lw=1, color=RAY_COLORS[i]
                    )[0]
                )
                self.drawn_rays_b.append(
                    self.axis.plot(
                        [], lw=3, color=RAY_COLORS[i]
                    )[0]
                )
                self.drawn_rays_b.append(
                    self.axis.plot(
                        [], lw=1, color="r"
                    )[0]
                )

        # text to display extreme info
        self.extreme_info = self.axis.text(
            300, 1.64, '', color=[0, 0, 0],
            fontsize='large', ha='center'
        )

        self.lines_c = []
        self.lines_b = []
        self.optimization_flag = False
        self.display_c_rays()
        self.display_b_rays()

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

    def display_c_rays(self):
        upper_lenses_obj = []
        active_index = [x for x, act in enumerate(self.active_lenses_c) if act]
        last_itr = len(active_index) - 1
        for counter, index in enumerate(active_index):
            upper_lenses_obj.append(
                Lens(
                    UPPER_LENSES[index][0],
                    self.cf_c[index],
                    None if counter == 0 else
                    upper_lenses_obj[counter - 1],
                    3
                )
            )
            self.crossover_points_c[index].set_data(
                upper_lenses_obj[counter].crossover_point_location()
            )
            self.crossover_points_c[index].set_visible(True)
            # TODO: what happens if there no active lens
            if counter == last_itr:
                upper_lenses_obj.append(
                    Lens(
                        SAMPLE[0],
                        0,
                        upper_lenses_obj[counter],
                        1
                    )
                )

        inactive_index = [
            x for x, act in enumerate(self.active_lenses_c) if not act
        ]
        for index in inactive_index:
            self.crossover_points_c[index].set_visible(False)

        for i in range(len(RAYS)):
            for j, lens in enumerate(upper_lenses_obj):
                lens.update_output_plane_location()
                sl, el, li = lens.ray_path(
                    RAYS[i] if j == 0 else
                    upper_lenses_obj[j - 1].ray_out_lens,
                    self.c_mag
                )
                sl = ([x for x, y in sl], [y for x, y in sl])
                el = ([x for x, y in el], [y for x, y in el])
                li = ([x for x, y in li], [y for x, y in li])
                self.lines_c.append(
                    self.axis.plot(sl[0], sl[1],  lw=1, color=RAY_COLORS[i])
                )
                self.lines_c.append(
                    self.axis.plot(el[0], el[1],  lw=2, color=RAY_COLORS[i])
                )
                self.lines_c.append(
                    self.axis.plot(li[0], li[1],  lw=1, color="r")
                )

    def update_c_lenses(self):
        for line in self.lines_c:
            line.pop(0).remove()
        self.lines_c = []

        self.display_c_rays()
        self.redraw()
        self.canvas.flush_events()

    def update_b_rays(self):
        self.scattering_angle = LAMBDA_ELECTRON / self.distance_from_optical
        self.sample_rays = [
            np.array([[0], [self.scattering_angle]]),
            np.array([[self.distance_from_optical], [self.scattering_angle]]),
            # np.array([[self.distance_from_optical], [0]])
        ]

    def display_b_rays(self):
        lower_lenses_obj = []
        active_index = [x for x, act in enumerate(self.active_lenses_b) if act]
        last_itr = len(active_index) - 1
        sample = Lens(SAMPLE[0], None, None, None)
        for counter, index in enumerate(active_index):
            lower_lenses_obj.append(
                Lens(
                    LOWER_LENSES[index][0],
                    self.cf_b[index],
                    sample if counter == 0 else
                    lower_lenses_obj[counter - 1],
                    3 if index != 2 else 2
                )
            )
            self.crossover_points_b[index].set_data(
                lower_lenses_obj[counter].crossover_point_location()
            )
            self.crossover_points_b[index].set_visible(True)

            if counter == last_itr:
                lower_lenses_obj.append(
                    Lens(
                        SCINTILLATOR[0],
                        0,
                        lower_lenses_obj[counter],
                        1
                    )
                )

        inactive_index = [
            x for x, act in enumerate(self.active_lenses_b) if not act
        ]
        for index in inactive_index:
            self.crossover_points_b[index].set_visible(False)

        # print("DRAW")
        for i in range(len(self.sample_rays)):
            # print(self.sample_rays[i])
            for j, lens in enumerate(lower_lenses_obj):
                if j != 0:
                    lens.update_output_plane_location()

                sl, el, li = lens.ray_path(
                    self.sample_rays[i] if j == 0 else
                    lower_lenses_obj[j - 1].ray_out_lens,
                    self.c_mag
                )
                sl = ([x for x, y in sl], [y for x, y in sl])
                el = ([x for x, y in el], [y for x, y in el])
                li = ([x for x, y in li], [y for x, y in li])
                self.lines_b.append(
                    self.axis.plot(sl[0], sl[1],  lw=1, color=RAY_COLORS[i])
                )
                self.lines_b.append(
                    self.axis.plot(el[0], el[1],  lw=2, color=RAY_COLORS[i])
                )
                self.lines_b.append(
                    self.axis.plot(li[0], li[1],  lw=1, color="r")
                )

    def update_b_lenses(self):
        for line in self.lines_b:
            line.pop(0).remove()
        self.lines_b = []

        self.update_b_rays()
        self.display_b_rays()
        self.redraw()
        self.canvas.flush_events()

    def redraw(self):
        self.axis.relim()
        self.axis.autoscale_view()
        self.canvas.draw()

    def optimization(self, opt_sel, lens_sel):
        print(opt_sel, lens_sel)
        if opt_sel == "Image":
            self.cf_b[lens_sel] = optimize_focal_length(
                opt_sel, lens_sel, [cz[0] for cz in LOWER_LENSES],
                self.cf_b, self.sample_rays[0:2]
            )
            for line in self.lines_b:
                line.pop(0).remove()
            self.lines_b = []

            self.update_b_rays()
            self.display_b_rays()
            self.redraw()
            self.canvas.flush_events()
        elif opt_sel == "Diffraction":
            self.cf_b[lens_sel] = optimize_focal_length(
                opt_sel, lens_sel, [cz[0] for cz in LOWER_LENSES],
                self.cf_b, self.sample_rays[0:2]
            )
            for line in self.lines_b:
                line.pop(0).remove()
            self.lines_b = []

            self.update_b_rays()
            self.display_b_rays()
            self.redraw()
            self.canvas.flush_events()
