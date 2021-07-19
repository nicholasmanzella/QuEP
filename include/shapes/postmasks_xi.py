
#THIS IS FOR MASKS that initiate after all objects(electrons) have been simulated through the wakefield

import sys
import math
import numpy as np
import pdb

# Initializes probe as a rectangular outline of electrons with area 2*s2 * 2*s1 with masks inserted to block electrons

def initProbe(x_c,y_c,xi_c,t0,s1,s2,ydensity,xidensity,res,left_of_masks,right_of_masks,x_f,y_f,xi_f,z_f,px_f,py_f,pz_f,new_ydensity,w):

    x_f = list(x_f)
    y_f = list(y_f)
    xi_f = list(xi_f)
    z_f = list(z_f)
    px_f = list(px_f)
    py_f = list(py_f)
    pz_f = list(pz_f)
    w = list(w)
    
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

# Adjusted mask location
    for i in range(0,len(left_of_masks)):
        left_of_masks[i] = left_of_masks[i] + zn
        right_of_masks[i] = right_of_masks[i] + zn

# eliminate blocked electrons
    h = 0
    f = 0
    ydensity = new_ydensity
    for i in range(0,ydensity):
        g = 0
        h = f
        f = 0
        xin = xileft
        for j in range(0,xidensity):
            if left_of_masks[g] <= xin + t0 <= right_of_masks[g]: #if xin is within the mask
                index = (j-f)+i*(xidensity-h)
                x_f = x_f[:index] + x_f[index+1:]
                y_f = y_f[:index] + y_f[index+1:]
                xi_f = xi_f[:index] + xi_f[index+1:]
                z_f = z_f[:index] + z_f[index+1:]
                px_f = px_f[:index] + px_f[index+1:]
                py_f = py_f[:index] + py_f[index+1:]
                pz_f = pz_f[:index] + pz_f[index+1:]
                w = w[:index] + w[index+1:]
                f+=1
            elif xin + t0 >= right_of_masks[g]:
                g += 1
                if g >= len(right_of_masks):
                    g-=1
            xin+=xistep


    x_f = np.array(x_f)
    y_f = np.array(y_f)
    xi_f = np.array(xi_f)
    z_f = np.array(z_f)

                   
    return x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, w
