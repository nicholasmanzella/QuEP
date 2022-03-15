import sys
import math
import numpy as np
import pdb
import progressbar
import time

# Creates weights based on distribution and inputted masks (below)

def getWeights(beamx_c,beamy_c,beamxi_c,x_c,y_c,xi_c,s1,s2,xdensity,ydensity,xidensity,resolution,sigma_x,sigma_y,noObj,t0,useWeights_x,useWeights_y,useMasks_xi,useMasks_y):

# Recompute necessary parameters (as done in shape file)
    xidensity_ = xidensity + xdensity - 1  # Allows enough particles in xi direction for x layering
    xistep = 2*s2/xidensity # Can also use resolution here
    ystep = 2*s1/ydensity
    xstep = xistep          # Purposefully setting xstep as equal to xistep for projection of x onto xi

# Calculate s3 
    s3 = xstep*(xdensity-1)/2.0
    print(f"s3 = {s3}\n")
    
# Define corners (xfront is first to enter field)
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
    
    print("Creating weighting arrays...")
# Create individual coordinate arrays    
    x_0 = np.linspace(xfront,xback,xdensity)      # List of all possible inital x  positions of all particles going through simulation
    y_0 = np.linspace(ytop,ybot,ydensity)         # List of all possible inital y  positions of all particles going through simulation
    xi_0 = np.linspace(xiright,xileft,xidensity)  # List of all possible inital xi positions of all particles going through simulation

# Special single layer case
    #if (xdensity == 1):
    #    x_0 = np.linspace(x_c,x_c,xdensity)



# Create empty weighting list
    w=[]
    w = [0 for k in range(0,noObj)] # Creates weighting array of length noObj, with default value 0
    yv = y_0.reshape(1,ydensity,1) # Reshapes y0 1D line into a 3D line
    w_y = np.exp((-1.*(yv-beamy_c)**2)/(2*sigma_y**2)) # Calculate weights for each y slice

# Loop through x layers to calculate weights with masks and add to 2D Y-Xi projection
    for i in progressbar.progressbar(range(0,len(x_0)), redirect_stout=False):
        start_time_weightcalc = time.time()
        # Create 3d virtual coordinate array for x-slice
        xv, yv, xiv = np.meshgrid(x_0[i], y_0, xi_0,indexing='ij',sparse=True) # Takes possible coordinates in each direction to make 3 3D arrays, containing location in each direction
        
        # Create 3d virtual weight arrays containing weight of each particle in x-slice
        w_x = np.exp((-1.*(x_0[i]-beamx_c)**2)/(2*sigma_x**2))

        # Weighting options evaluator
        if (useWeights_x) and (useWeights_y):
            w_virt = w_x * w_y
        elif (useWeights_x):
            w_virt = w_x
        elif (useWeights_y):
            w_virt = w_y
        else:
            w_y_noweight = np.copy.deepcopy(w_y)
            w_y_noweight.fill(1.0)
            w_virt = np.copy(w_y_noweight)
        print(f"Shape 1: {np.shape(w_virt)}")
        
        # MASKING
        if (not (useMasks_y)) and (not (useMasks_xi)):
            w_virt = np.where(xiv == None, 0, w_virt) # Why is this needed?
        
        if (useMasks_xi):
            # Define masks in xi direction. Change if different mask is desired
            left_of_masks = []  # left most limit of each mask in order, on inital xi position
            left_of_masks = left_of_masks.tolist()
            right_of_masks = []  # right most limit of each mask in order, on initial xi position
            right_of_masks = right_of_masks.tolist()

            # Apply masks to w_virt
            for g in range(0,len(left_of_masks)):
                w_virt = np.where(np.logical_and(xiv > left_of_masks[g], xiv < right_of_masks[g]), 0, w_virt)
                
        if (useMasks_y):
            # Define masks in y direction, 0 is 0 on the y-axis. Change if different mask is desired
            top_of_masks = [-0.3,0.8]  #upper limit of each mask in order
            bot_of_masks = [-0.4,0.5]  #lower limit of each mask in order 

            # Apply masks to w_virt
            w_virt = np.where(xiv == None, 0, w_virt)
            for h in range(0,len(top_of_masks)):
                w_virt = np.where(np.logical_and(yv > bot_of_masks[h], yv < top_of_masks[h]), 0, w_virt)
        # END OF MASKING
            
        print(f"Shape: 2 {np.shape(w_virt)}")
        # Create final weighting list w to return
        # Maps 3d virtual particles in x-layer onto 2d Y-Xi projection appropriate location
        start_time_proj = time.time()
        for j in range(0,ydensity):
            for k in range(0,xidensity):
                w[xidensity_ * j + k + i] += w_virt[0,j,k]
        
        # Delete/Deallocate arrays for memory conservation
        xv = None
        yv = None
        xiv = None
        w_x = None
        w_virt = None
        w_y_noweight = None

    
    return w, w_virt, xv, yv, xiv