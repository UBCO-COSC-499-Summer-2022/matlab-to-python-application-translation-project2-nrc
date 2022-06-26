
#determines path for a given ray based on the UR and Cf values of the lenses
def PlotCL3(UR, Cf, ray, fig, crossoverPoints, Cmag):

    # Array of coordinates of tbe path of the ray
    x, y = [], []  # x = horizontal plot axis, y = vertical plot axis
    
    # ------- Source to C1 to Image 1 -------
    z0 = 0
    rout1, d1 = mvac(0,upper_lenses[0][0],ray) # ray propagation from source to C1
    x.append(z0)
    x.append(d1)
    y.append(ray[0][0])
    y.append(rout1[0][0])

    # effect of C1
    rout_C1, zout_C1, d_C1, Mag1 = mlens(upper_lenses[0][0],Cf[0],rout1,0,'C1', crossoverPoints, Cmag)

    return