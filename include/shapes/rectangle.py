import sys
import math
import numpy as np
import pdb

# Initializes probe as a rectangular outline of electrons with area 2*s2 * 2*s1

def initProbe(x_c,y_c,xi_c,t0,s1,s2,s3,density):
    x_0, y_0, xi_0, z_0 = [],[],[],[]

    xistep = 2*s2/density
    ystep = 2*s1/density
    #xstep = s3/(density/20)
    #print("Xstep = ", xstep)

# Define corners
    ytop = y_c + s1
    ybot = y_c - s1
    xileft = xi_c - s2
    xiright = xi_c + s2
    # if (x_c < 0):
    #     xmax = x_c - s3
    # else:
    #     xmax = x_c + s3
    # print("Xmax = ", xmax)

# Start in top left
    yn = ytop
    xin = xileft
    zn = xileft + t0
    #xn = x_c

    for i in range(0,density):
        for j in range(0,density):
            x_0.append(x_c)
            y_0.append(yn)
            xi_0.append(xin)
            z_0.append(xin + t0)
            xin += xistep
        yn -= ystep
        xin = xileft

    # while (abs(xn) < abs(xmax)):
    #     for i in range(0,density):
    #         for j in range(0,density):
    #             x_0.append(xn)
    #             y_0.append(yn)
    #             xi_0.append(xin)
    #             z_0.append(xin + t0)
    #             xin += xistep
    #         yn -= ystep
    #         xin = xileft
    #     if (x_c < 0):
    #         xn -= xstep
    #     else:
    #         xn += xstep
    #         print("xn = ", xn)

    return x_0, y_0, xi_0, z_0
