import sys
import math
import numpy as np
import pdb

# Initializes probe as a rectangular outline of electrons with area 2*s2 * 2*s1

def initProbe(x_c,y_c,xi_c,t0,s1,s2,s3,ydensity,xidensity,resolution):
    x_0, y_0, xi_0, z_0 = [],[],[],[]

    xistep = resolution
    ystep = resolution#0.05#resolution
    #xstep = s3/(density/20)
    #print("Xstep = ", xstep)

# Define corners
    ytop = y_c + s1 # x_c + s1
    ybot = y_c - s1 # x_c - s2
    xileft = xi_c - s2
    xiright = xi_c + s2

# Start in top left
    yn = ytop
    xin = xileft
    zn = xileft + t0

    for i in range(0,ydensity):
        for j in range(0,xidensity):
            x_0.append(x_c)#yn)
            y_0.append(yn)#x_c)
            xi_0.append(xin)
            z_0.append(xin + t0)
            xin += xistep
        yn -= ystep
        xin = xileft

    return x_0, y_0, xi_0, z_0
