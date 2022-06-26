
# determines path for a given ray based on the UR and Cf values of the lenses
def PlotCL3(UR, Cf, ray, fig, crossoverPoints, Cmag):

    # Array of coordinates of tbe path of the ray
    x, y = [], []  # x = horizontal plot axis, y = vertical plot axis

    # ------- Source to C1 to Image 1 -------
    z0 = 0
    # ray propagation from source to C1
    rout1, d1 = mvac(0,upper_lenses[0][0],ray)
    x.append(z0)
    x.append(d1)
    y.append(ray[0][0])
    y.append(rout1[0][0])

    # effect of C1
    rout_C1, zout_C1, d_C1, Mag1 = mlens(upper_lenses[0][0],Cf[0],rout1,0,'C1', crossoverPoints, Cmag)

    # ray propagation in vacuum from C1 to Image 1
    rout_Im1, d_Im1 = mvac(upper_lenses[0][0], d_C1, rout_C1)
    x.append(upper_lenses[0][0])
    x.append(upper_lenses[0][0]+d_Im1)
    y.append(rout_C1[0][0])
    y.append(rout_Im1[0][0])

    # ------- Image 1 to C2 to Image 2 -------
    # ray propagation in vacuum from C1 to C2
    rout2, d2 = mvac(upper_lenses[0][0], 
                     upper_lenses[1][0]-upper_lenses[0][0], 
                     rout_C1)
    x.append(upper_lenses[0][0])
    x.append(upper_lenses[0][0]+d2)
    y.append(rout_C1[0][0])
    y.append(rout2[0][0])

    # effect of C2
    rout_C2, zout_C2, d_C2, Mag2 = mlens(upper_lenses[1][0],
                                      Cf[1], rout2, 0, 'C2',
                                      crossoverPoints, Cmag)

    # ray propagation in vacuum from C2 to Image 2 
    rout_Im2,d_Im2 = mvac(upper_lenses[1][0], d_C2,rout_C2)
    x.append(upper_lenses[1][0])
    x.append(upper_lenses[1][0]+d_Im2)
    y.append(rout_C2[0][0])
    y.append(rout_Im2[0][0])

    # ------- Image 2 to C3 to Image 3 -------
    # ray propagation in vacuum from C2 to C3
    rout3,d3 = mvac(upper_lenses[1][0],
                    upper_lenses[2][0]-upper_lenses[1][0],
                    rout_C2)
    x.append(upper_lenses[1][0])
    x.append(upper_lenses[1][0]+d3)
    y.append(rout_C2[0][0])
    y.append(rout3[0][0])

    return x, y

    # effect of C3
    rout_C3,zout_C3,d_C3,Mag3 = mlens(Czz[2],Cf[2],rout3,0,'C3', crossoverPoints, Cmag)


    # ray propagation in vacuum from C3 to Image 3
    rout_Im3,d_Im3 = mvac(Czz[2],d_C3,rout_C3)
    x.append(Czz[2])
    x.append(Czz[2]+d_Im3)
    y.append(rout_C3[0][0])
    y.append(rout_Im3[0][0])


    # ------- C3 to sample plane ------
    # ray propagation in vacuum from C2 to C3
    rout_smpl,d_smpl = mvac(Czz[2],Sample_location-Czz[2],rout_C3)
    x.append(Czz[2])
    x.append(Czz[2]+d_smpl)
    y.append(rout_C3[0][0])
    y.append(rout_smpl[0][0])

    # finding the beam farthest from the optics axis
    global routMax
    if abs(rout_smpl[0]) > abs(routMax[0]):
        routMax = rout_smpl