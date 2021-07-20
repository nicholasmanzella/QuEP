import sys
import math
import numpy as np
import pdb

# Creates weights based on distribution and inputted masks (below)

def getWeights(beamx_c,beamy_c,beamxi_c,x_c,y_c,xi_c,s1,s2,xdensity,ydensity,xidensity,resolution,sigma_x,sigma_y,noObj,t0,useWeights_x,useWeights_y,useMasks_xi,useMasks_y):

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
    zn = xiright + t0
    
# Create individual coordiante arrays    
    x_0 = np.linspace(xfront,xback,xdensity)
    y_0 = np.linspace(ytop,ybot,ydensity)
    xi_0 = np.linspace(xiright,xileft,xidensity)

# Create 3d virtual coordinate arrays 
    xv, yv, xiv = np.meshgrid(x_0, y_0, xi_0,indexing='ij')

# Create 3d virtual weight arrays containing weight of each particle
    w_x = np.exp((-1.*(xv-beamx_c)**2)/(2*sigma_x**2))
    w_y = np.exp((-1.*(yv-beamy_c)**2)/(2*sigma_y**2))

# Weighting options evaluator
    if (useWeights_x) and (useWeights_y):
        w_virt = w_x * w_y
    elif (useWeights_x):
        w_virt = w_x
    elif (useWeights_y):
        w_virt = w_y

# MASKING 
    if (useMasks_xi):
        #Define masks in z direction, leftmost z-coordinate = 0. Change if different mask is desired
        left_of_masks= [30,43]  # left most limit of each mask in order
        right_of_masks = [32,48]  # right most limit of each mask in order

        print(zn)
        # Conversion of z-coord to xi-coord
        for i in range(0,len(left_of_masks)):
            left_of_masks[i] = left_of_masks[i] - zn
            right_of_masks[i] = right_of_masks[i] - zn

        for g in range(0,len(left_of_masks)):
            w_virt = np.where(np.logical_and(xiv > left_of_masks[g], xiv < right_of_masks[g]), 0, w_virt)

    if (useMasks_y):
        #Define masks in y direction, 0 is 0 on the y-axis. Change if different mask is desired
        top_of_masks = [-0.3,0.8]  #upper limit of each mask in order
        bot_of_masks = [-0.4,0.5]  #lower limit of each mask in order 

        for h in range(0,len(top_of_masks)):
            w_virt = np.where(np.logical_and(yv > bot_of_masks[h], yv < top_of_masks[h]), 0, w_virt)
# END OF MASKING

# Create final weighting list to return
# Maps 3d virtual particles onto 2d projection
    w = []
    w = [0 for k in range(0,noObj)]
    for i in range(0,xdensity):
        for j in range(0,ydensity):
            for k in range(0,xidensity):
                w[xidensity_ * j + k + i] += w_virt[i,j,k]
    
    return w, w_virt, xv, yv, xiv