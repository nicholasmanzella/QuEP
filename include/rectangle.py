import sys
import math
import numpy as np
import pdb

def initProbe(x_c,y_c,xi_c,t0,s1,s2,density):
    x_0, y_0, xi_0, z_0 = [],[],[],[]

    perim = 2 * s1 + 2 * s2
    step = perim / density

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
        x_0.append(x_c)
        y_0.append(yn)
        xi_0.append(xin)
        z_0.append(zn)
        
        if (xin < xiright and yn == ytop):
            yn = ytop
            xin += step
        elif (xin >= xiright and yn <= ytop):
            yn -= step
            xin = xiright
        elif (xin <= xiright and yn <= ybot):
            yn == ybot
            xin -= step
        elif (xin <= xileft and yn < ytop):
            xin == xileft
            yn += step
        zn = xin + t0

    return x_0, y_0, xi_0, z_0
