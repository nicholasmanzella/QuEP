
#THIS IS FOR MASKS that initiate after all objects(electrons) have been simulated through the wakefield

import sys
import math
import numpy as np
import pdb

# Initializes probe as a rectangular outline of electrons with area 2*s2 * 2*s1 with masks inserted to block electrons

def initProbe(x_c,y_c,xi_c,t0,s1,s2,s3,ydensity,xidensity,res,top_of_masks,bot_of_masks,x_f,y_f,xi_f,z_f,px_f,py_f,pz_f):
    x_f = list(x_f)
    y_f = list(y_f)
    xi_f = list(xi_f)
    z_f = list(z_f)
    px_f = list(px_f)
    py_f = list(py_f)
    pz_f = list(pz_f)
    
#Define masks. Change if different mask is desired

    xistep = 2*s2/xidensity # Can also use resolution here
    ystep = 2*s1/ydensity

# Define corners
    ytop = y_c + s1
    ybot = y_c - s1
    xileft = xi_c - s2
    xiright = xi_c + s2

# Start in top left
    yn = ytop
    xin = xileft
    zn = xileft + t0



#eliminate blocked electrons
    g = 0  #index for top/bot of mask lists
    h = 0
    for i in range(0,ydensity):
        if top_of_masks[g] >= yn >= bot_of_masks[g]: #if yn is within the mask
            for j in range(0,xidensity-1):
                index = (i-h)*xidensity
                x_f = x_f[:index] + x_f[index+1:]
                y_f = y_f[:index] + y_f[index+1:]
                xi_f = xi_f[:index] + xi_f[index+1:]
                z_f = z_f[:index] + z_f[index+1:]
                px_f = px_f[:index] + px_f[index+1:]
                py_f = py_f[:index] + py_f[index+1:]
                pz_f = pz_f[:index] + pz_f[index+1:]
            h+=1
        elif yn <= bot_of_masks[g]:
            g += 1
        if g >= len(bot_of_masks):
            break
        yn-=ystep

    x_f = np.array(x_f)
    y_f = np.array(y_f)
    xi_f = np.array(xi_f)
    z_f = np.array(z_f)
    new_ydensity = ydensity - h

                   
    return x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, new_ydensity
