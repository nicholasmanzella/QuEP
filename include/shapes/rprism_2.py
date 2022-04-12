import sys
import math
import numpy as np
import pdb

# Initializes probe as a rectangular prism outline of electrons with volume = 2*s3 * 2*s2 * 2*s1

def initProbe(x_c,y_c,xi_c,t0,s1,s2,xdensity,ydensity,xidensity,resolution):
    print("Using shape rprism_2")
    
    x_0, y_0, xi_0, z_0 = [],[],[],[]

    xistep = 2*s2/xidensity # Can also use resolution here
    ystep = 2*s1/ydensity

    
# Define corners (front is first to enter field)
    ytop = y_c + s1
    ybot = y_c - s1
    xileft = xi_c - s2
    xiright = xi_c + s2

# Start in front top right
    yn = ytop
    xin = xiright
    zn = xiright + t0
    xn = x_c
    
# Place 2D particle sheet
    for i in range(0,ydensity):
        for j in range(0,xidensity):
            x_0.append(xn)
            y_0.append(yn)
            xi_0.append(xin)
            z_0.append(xin + t0)
            xin -= xistep
        yn -= ystep
        xin = xiright

    return x_0, y_0, xi_0, z_0
