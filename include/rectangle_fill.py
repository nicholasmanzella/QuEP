import sys
import math
import numpy as np
import pdb

def initProbe(x_c,y_c,xi_c,t0,s1,s2,density):
# Fills rectangle shaped probe evenly from left to right
    x_0, y_0, xi_0, z_0 = [],[],[],[]

    rho = density/(4 * s1 * s2)
    xistep = (2 * s2)/rho
    ystep = (2 * s1)/rho
    # Define corners
    ytop = y_c + s1
    ybot = y_c - s1
    xileft = xi_c - s2
    xiright = xi_c + s2

    # Start in top left
    yn = ytop - ystep/2
    xin = xileft + xistep/2

    #pdb.set_trace()
    for i in range(0,density):
        x_0.append(x_c)
        y_0.append(yn)
        xi_0.append(xin)
        z_0.append(xin + t0)

        xin += xistep
    # Send back to left side if past right side
        if (xin >= xiright):
            xin = xileft + xistep/2
            yn -= ystep

    return x_0, y_0, xi_0, z_0
