import sys
import math
import numpy as np
import pdb

# Creates weights based on distribution

def getWeights(beamx_c,beamy_c,beamxi_c,x_c,y_c,xi_c,s1,s2,xdensity,ydensity,xidensity,resolution,sigma_x,sigma_y,noPart,useWeights_x,useWeights_y):

    # Recompute necessary parameters (as done in shape file)
    xidensity_ = xidensity + xdensity - 1  # Allows enough particles in xi direction for x layering
    xistep = 2*s2/xidensity # Can also use resolution here
    ystep = 2*s1/ydensity
    xstep = xistep          # Purposefully setting xstep as equal to xistep for projection of x onto xi, unused here

# Calculate s3 
    s3 = xstep*(xdensity-1)/2.0
    print(f"s3 = {s3}")
    
# Define corners (front is first to enter field)
    ytop = y_c + s1
    ybot = y_c - s1
    xileft = xi_c - s2
    xiright = xi_c + s2
    xfront = x_c + s3  
    xback = x_c - s3
    
# Start in front top right
    yn = ytop
    xin = xiright
    xn = xfront
    
    x_0 = np.linspace(xfront,xback,xdensity)
    y_0 = np.linspace(ytop,ybot,ydensity)
    xi_0 = np.linspace(xiright,xileft,xidensity)
    xv, yv, xiv = np.meshgrid(x_0, y_0, xi_0)

    w_x = np.exp((-1.*(xv-beamx_c)**2)/(2*sigma_x**2))
    w_y = np.exp((-1.*(yv-beamy_c)**2)/(2*sigma_y**2))

    if (useWeights_x) and (useWeights_y):
        w_virt = w_x * w_y
    elif (useWeights_x):
        w_virt = w_x
    elif (useWeights_y):
        w_virt = w_y
    
    w = []
    w = [0 for k in range(0,noPart)]
    for i in range(0,xdensity):
        for j in range(0,ydensity):
            for k in range(0,xidensity):
                w[xidensity_ * j + k + i] += w_virt[j,i,k]
    
    return w