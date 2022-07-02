import numpy as np

# stores info for the upper lenses
upper_lenses = [
    [257.03, 63, 1.5, [0.3, 0.9, 0.65], 'C1'],
    [349, 1.5, 1, [0.3, 0.75, 0.75], 'C2'],
    [517, 1.5, 1, [0.3, 0.75, 0.75], 'C3']
]

# stores info for the lower lenses
lower_lenses = [
    [551.6, 1.5, -1, [0.3, 0.75, 0.75], 'OBJ'],
    [706.4, 1.5, 1, [0.3, 0.75, 0.75], 'Intermediate'],
    [826.9, 1.5, 1, [0.3, 0.75, 0.75], 'Projective']
]

# stores info for the anode
anode = [39.1, 30, 1.5, [0.5, 0, 0.3], 'Anode']

# stores info for the sample
sample = [528.9, 1.5, -1, [1, 0.7, 0], 'Sample']

# stores info for the condensor aperature
condensor_aperature = [192.4, 1.5, 1, [0, 0, 0], 'Cond. Apert']

# stores info for the scintillator
scintillator = [972.7, 1.5, 1, [0.3, 0.75, 0.75], 'Scintillator']


# transfer matrix for free space
def Mspc(d):
    return np.array([[1, d], [0, 1]], dtype=float)


# transfer matrix for thin lens
def Mtl(focal_length):
    return np.array([[1, 0], [-1/focal_length, 1]], dtype=float)


# determines path for a given ray based on the UR and Cf values of the lenses
def ray_path(UR, Cf, ray, fig, crossoverPoints, Cmag):

    # Array of coordinates of tbe path of the ray
    x, y = [], []  # x = horizontal plot axis, y = vertical plot axis

    # ------- Source to C1 to Image 1 -------
    z0 = 0
    # ray propagation from source to C1
    rout1, d1 = vacuum_matrix(0, upper_lenses[0][0], ray)
    x.append(z0)
    x.append(d1)
    y.append(ray[0][0])
    y.append(rout1[0][0])

    # effect of C1
    rout_C1, d_C1 = thin_lens_matrix(upper_lenses[0][0],
                                     Cf[0], rout1, 0, 'C1',
                                     crossoverPoints, Cmag)

    # ray propagation in vacuum from C1 to Image 1
    rout_Im1, d_Im1 = vacuum_matrix(upper_lenses[0][0], d_C1, rout_C1)
    x.append(upper_lenses[0][0])
    x.append(upper_lenses[0][0]+d_Im1)
    y.append(rout_C1[0][0])
    y.append(rout_Im1[0][0])

    # ------- Image 1 to C2 to Image 2 -------
    # ray propagation in vacuum from C1 to C2
    rout2, d2 = vacuum_matrix(upper_lenses[0][0],
                     upper_lenses[1][0]-upper_lenses[0][0], 
                     rout_C1)
    x.append(upper_lenses[0][0])
    x.append(upper_lenses[0][0]+d2)
    y.append(rout_C1[0][0])
    y.append(rout2[0][0])

    # effect of C2
    rout_C2, d_C2 = thin_lens_matrix(upper_lenses[1][0],
                                      Cf[1], rout2, 0, 'C2',
                                      crossoverPoints, Cmag)

    # ray propagation in vacuum from C2 to Image 2 
    rout_Im2, d_Im2 = vacuum_matrix(upper_lenses[1][0], d_C2,rout_C2)
    x.append(upper_lenses[1][0])
    x.append(upper_lenses[1][0]+d_Im2)
    y.append(rout_C2[0][0])
    y.append(rout_Im2[0][0])

    # ------- Image 2 to C3 to Image 3 -------
    # ray propagation in vacuum from C2 to C3
    rout3, d3 = vacuum_matrix(upper_lenses[1][0],
                    upper_lenses[2][0]-upper_lenses[1][0],
                    rout_C2)
    x.append(upper_lenses[1][0])
    x.append(upper_lenses[1][0]+d3)
    y.append(rout_C2[0][0])
    y.append(rout3[0][0])

    # effect of C3
    rout_C3, d_C3 = thin_lens_matrix(upper_lenses[2][0], Cf[2],
                                         rout3, 0, 'C3', crossoverPoints, Cmag)

    # ray propagation in vacuum from C3 to Image 3
    rout_Im3, d_Im3 = vacuum_matrix(upper_lenses[2][0], d_C3, rout_C3)
    x.append(upper_lenses[2][0])
    x.append(upper_lenses[2][0]+d_Im3)
    y.append(rout_C3[0][0])
    y.append(rout_Im3[0][0])

    # ------- C3 to sample plane ------
    # ray propagation in vacuum from C2 to C3
    rout_smpl, d_smpl = vacuum_matrix(upper_lenses[2][0],
                            sample[0]-upper_lenses[2][0],
                            rout_C3)
    x.append(upper_lenses[2][0])
    x.append(upper_lenses[2][0]+d_smpl)
    y.append(rout_C3[0][0])
    y.append(rout_smpl[0][0])

    # finding the beam farthest from the optics axis
    global routMax
    if abs(rout_smpl[0]) > abs(routMax[0]):
        routMax = rout_smpl
    return x, y


# transfer matrix for vacuum & plot of corresponding ray
def vacuum_matrix(z0, d, rin):
    """ inputs: z0   =object location [mm] from source
                d    =distance in space traveled [mm]
                rin  =height [mm] IN beam, angle of IN beam [rad]: column vector
    """
    # beam height X [mm], beam angle [rad] after propagation
    rout = np.matmul(Mspc(d), rin)

    """outputs: out =height X [mm] OUT-beam, angle of OUT beam [rad]: column vector
                d   =distance beam traveled along z [mm]
    """
    return rout, d


# transfer matrix for a thin lens & plot of corresponding ray from lens to image
def thin_lens_matrix(z0, focal_length, rin, zin, lens, crossoverPoints, Cmag):
    """ inputs:   z0     ... lens distance from source [mm]
                  f      ... focal length [mm]
                  rin    ... [height" of IN beam [mm]; angle of IN beam [rad]]; column vector
                  zin    ... location of object [mm] from source
                  lens   ... string name of the lens
        outputs:  rout   ... [height X [mm] OUT-beam-at-image, angle of OUT-beam [rad]]; column vector
                  zout   ... image location Z [mm] from source
                  d      ... lens centre-image distance along z [mm]
                  MagOut ... magnification image/object
    """

    # locate image z & crossover
    # temporary matrix calculating transfer vacuum to lens, and lens
    Mtmp = np.matmul(Mtl(focal_length), Mspc(z0-zin))
    # lens-to-image [mm] # for thin lens # AA = A(f,z0)
    d = -Mtmp[0, 1]/Mtmp[1, 1]
    # image-to-source Z [mm]
    z_out = d + z0

    # rout = [X, q] at OUT-face of lens
    # r = [x,q] at OUT-face of lens - that is needed to vacuum propagation matrix and plot
    rout = np.matmul(Mtl(focal_length), rin)

    # calculate magnification X_image / X_obj
    # for thin lens: MagOut = Mag(z0,d) % or MagOut = Mag(z0,A(f,z0))
    MagOut = 1/Mtmp[1, 1]

    # add this in later PR:
    """
    # update graph
    # find index of lens 'Cx' where x is 1,2,3
    i = Cfname.index(lens)
    # print MagOut value, which is the magnification factor of image/object
    Cmag[i].set_text(lens + " Mag  = {:.3f}X".format(float(MagOut)))
    # place a mark at the crossover point
    crossoverPoints[i].set_data(z0+f, 0)
    """
    return rout, z_out, d, MagOut
