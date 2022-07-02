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
def Mspc(distance):
    return np.array([[1, distance], [0, 1]], dtype=float)


# transfer matrix for thin lens
def Mtl(focal_length):
    return np.array([[1, 0], [-1/focal_length, 1]], dtype=float)


# determines path for a given ray based on the UR and Cf values of the lenses
def ray_path(Cf, ray, crossoverPoints, Cmag):

    # Array of coordinates of tbe path of the ray
    x, y = [], []  # x = horizontal plot axis, y = vertical plot axis

    # ------- Source to C1 to Image 1 -------
    z0 = 0
    # ray propagation from source to C1
    ray_out1, d1 = vacuum_matrix(0, upper_lenses[0][0], ray)
    x.append(z0)
    x.append(d1)
    y.append(ray[0][0])
    y.append(ray_out1[0][0])

    # effect of C1
    ray_out_C1, d_C1 = thin_lens_matrix(upper_lenses[0][0],
                                     Cf[0], ray_out1, 0, 'C1',
                                     crossoverPoints, Cmag)

    # ray propagation in vacuum from C1 to Image 1
    ray_out_Image1, d_Image1 = vacuum_matrix(upper_lenses[0][0], d_C1, ray_out_C1)
    x.append(upper_lenses[0][0])
    x.append(upper_lenses[0][0]+d_Image1)
    y.append(ray_out_C1[0][0])
    y.append(ray_out_Image1[0][0])

    # ------- Image 1 to C2 to Image 2 -------
    # ray propagation in vacuum from C1 to C2
    ray_out2, d2 = vacuum_matrix(upper_lenses[0][0],
                     upper_lenses[1][0]-upper_lenses[0][0], 
                     ray_out_C1)
    x.append(upper_lenses[0][0])
    x.append(upper_lenses[0][0]+d2)
    y.append(ray_out_C1[0][0])
    y.append(ray_out2[0][0])

    # effect of C2
    ray_out_C2, d_C2 = thin_lens_matrix(upper_lenses[1][0],
                                      Cf[1], ray_out2, 0, 'C2',
                                      crossoverPoints, Cmag)

    # ray propagation in vacuum from C2 to Image 2 
    ray_out_Image2, d_Image2 = vacuum_matrix(upper_lenses[1][0], d_C2,ray_out_C2)
    x.append(upper_lenses[1][0])
    x.append(upper_lenses[1][0]+d_Image2)
    y.append(ray_out_C2[0][0])
    y.append(ray_out_Image2[0][0])

    # ------- Image 2 to C3 to Image 3 -------
    # ray propagation in vacuum from C2 to C3
    ray_out3, d3 = vacuum_matrix(upper_lenses[1][0],
                              upper_lenses[2][0]-upper_lenses[1][0],
                              ray_out_C2)
    x.append(upper_lenses[1][0])
    x.append(upper_lenses[1][0]+d3)
    y.append(ray_out_C2[0][0])
    y.append(ray_out3[0][0])

    # effect of C3
    ray_out_C3, d_C3 = thin_lens_matrix(upper_lenses[2][0], Cf[2],
                                     ray_out3, 0, 'C3', crossoverPoints, Cmag)

    # ray propagation in vacuum from C3 to Image 3
    ray_out_Image3, d_Image3 = vacuum_matrix(upper_lenses[2][0], d_C3, ray_out_C3)
    x.append(upper_lenses[2][0])
    x.append(upper_lenses[2][0]+d_Image3)
    y.append(ray_out_C3[0][0])
    y.append(ray_out_Image3[0][0])

    # ------- C3 to sample plane ------
    # ray propagation in vacuum from C2 to C3
    ray_out_sample, d_sample = vacuum_matrix(upper_lenses[2][0],
                                             sample[0]-upper_lenses[2][0],
                                             ray_out_C3)
    x.append(upper_lenses[2][0])
    x.append(upper_lenses[2][0]+d_sample)
    y.append(ray_out_C3[0][0])
    y.append(ray_out_sample[0][0])


# transfer matrix for vacuum & plot of corresponding ray
def vacuum_matrix(distance, ray_in):
    """ inputs:
        distance    =distance in space traveled [mm]
        ray_in  =height [mm] IN beam, angle of IN beam [rad]: column vector
    """
    # beam height X [mm], beam angle [rad] after propagation
    ray_out = np.matmul(Mspc(distance), ray_in)

    """outputs: 
        ray_out=height X [mm] OUT-beam, angle of OUT beam [rad]: column vector
        ditance=distance beam traveled along z [mm]
    """
    return ray_out, distance


# transfer matrix for a thin lens & plot of corresponding ray from lens to image
def thin_lens_matrix(location, focal_length, ray_in, obj_location, lens, crossover_points, Cmag):
    """ inputs:   location ... lens distance from source [mm]
                  focal_length    ... focal length [mm]
                  ray_in    ... [height" of IN beam [mm]; angle of IN beam [rad]]; column vector
                  obj_location    ... location of object [mm] from source
                  lens   ... string name of the lens
        outputs:  height_out   ... [height X [mm] OUT-beam-at-image, angle of OUT-beam [rad]]; column vector
                  zout   ... image location Z [mm] from source
                  distance ... lens centre-image distance along z [mm]
                  MagOut ... magnification image/object
    """

    # locate image z & crossover
    # temporary matrix calculating transfer vacuum to lens, and lens
    Mtmp = np.matmul(Mtl(focal_length), Mspc(location-obj_location))
    # lens-to-image [mm] # for thin lens # AA = A(f,z0)
    distance = -Mtmp[0, 1]/Mtmp[1, 1]
    # image-to-source Z [mm]
    z_out = distance + location

    # ray_out = [X, q] at OUT-face of lens
    # r = [x,q] at OUT-face of lens - that is needed to vacuum propagation matrix and plot
    ray_out = np.matmul(Mtl(focal_length), ray_in)

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
    crossover_points[i].set_data(z0+f, 0)
    """
    return ray_out, z_out, distance, MagOut
