import sys
import math
import numpy as np
import pdb

# Initializes probe as a rectangular outline of electrons with area 2*s2 * 2*s1

def initProbe(x_c,y_c,xi_c,t0,s1,s2,density):
    x_0, y_0, xi_0, z_0 = [],[],[],[]

    xistep = 2*s2/density
    ystep = 2*s1/density

# Define corners
    ytop = y_c + s1
    ybot = y_c - s1
    xileft = xi_c - s2
    xiright = xi_c + s2

# Start in top left
    yn = ytop
    xin = xileft
    zn = xileft + t0

    for i in range(0,density):
        for j in range(0,density):
            x_0.append(x_c)
            y_0.append(yn)
            xi_0.append(xin)
            z_0.append(xin + t0)

            xin += xistep
        yn -= ystep
        xin = xileft

    return x_0, y_0, xi_0, z_0
