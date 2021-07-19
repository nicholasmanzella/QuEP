# index.py can be used to propagate objects after simulation through fields in main.py
# Available features include weighting of particles and masking of regions

# Include file imports
import sys
import time
import importlib
import numpy as np
import include.plot2DTracks as plot2D
import include.plot3DTracks as plot3D
import include.showQuickEvolution as showEvol_Q
import include.showFullEvolution as showEvol_F
import include.viewProbe as viewProbe
import include.writeFullEvolData as writeHist
import include.shapes.postmasks_y as postmasks_y
import include.shapes.postmasks_xi as postmasks_xi
import include.weighting_function as weightFunc
import include.plotWeights as plotWeights

# Be sure to change .npz file name location from main.py output!

# Weighting Options (Only applicable for showFullEvolution plot):
useWeights_x = True                 # Use weights in x-direction
useWeights_y = True                 # Use weights in y-direction
singleLayerBeam = False             # Use beam with thickness xden=1 in x-direction

# Masking Options:
useMasks = False                      # Use masks in either direction (Note: Masking must be done after weighting!)

# Plotting Scripts
plot2DTracks = False                 # View 2D projections of trajectories
showQuickEvolution = False           # View evolution of probe after leaving plasma at inputted x_s in scatter plots # Use for low density probes
showFullEvolution = True             # View full evolution of probe at hardcoded locations in colored histograms # Use for high density probes
writeHistData = False
plotWeightsy = False                  # Plot w_x vs xi
plotWeightsx = False                  # Plot w_y vs y
# Set all others equal False if want animation saved (dependency issue)
#saveMovie = False                   # Save gif of probe evolution
#if (saveMovie):
#    import include.makeAnimation as makeAnimation

if (len(sys.argv) == 3):
    
    # Begin timing index file runtime
    start_time = time.time()
    t = time.localtime()
    curr_time = time.strftime("%H:%M:%S", t)
    print("Start Time: ", curr_time)
    
    # Get inital conditions of probe again
    input_fname_1 = str(sys.argv[1])
    print("Using initial conditions from ", input_fname_1)
    init = importlib.import_module(input_fname_1)
    sim_name = init.simulation_name
    shape_name = init.shape
    xden = init.xdensity
    yden = init.ydensity
    xiden = init.xidensity
    res = init.resolution
    iter = init.iterations
    mode = init.mode
    fname = init.fname
    x_c = init.x_c
    y_c = init.y_c
    xi_c = init.xi_c
    px_0 = init.px_0
    py_0 = init.py_0
    pz_0 = init.pz_0
    x_s = init.x_s
    s1 = init.s1
    s2 = init.s2

    # Get initial conditions of beam
    input_fname_2 = str(sys.argv[2])
    print("Using beam conditions from ", input_fname_2)
    beaminit = importlib.import_module(input_fname_2)
    beamx_c = beaminit.beamx_c
    beamy_c = beaminit.beamy_c
    beamxi_c = beaminit.beamxi_c
    sigma_x=beaminit.sigma_x
    sigma_y=beaminit.sigma_y

    # Load data from npz file export from main.py
    data = np.load('./data/' + fname) # Change this line as needed
    x_0 = data['x_init']
    y_0 = data['y_init']
    xi_0 = data['xi_init']
    z_0 = data['z_init']
    x_f = data['x_dat']
    y_f = data['y_dat']
    xi_f = data['xi_dat']
    z_f = data['z_dat']
    px_f = data['px_dat']
    py_f = data['py_dat']
    pz_f = data['pz_dat']
    t0 = 0#data['t_dat']

    if (singleLayerBeam):
        xden = 1

    noPart = len(x_0) # Number of particles in the simulation

    # Create weighting array
    w = []
    w = [1 for k in range(0,noPart)]
    
    if (useWeights_x) or (useWeights_y):
        w = weightFunc.getWeights(beamx_c,beamy_c,beamxi_c,x_c,y_c,xi_c,s1,s2,xden,yden,xiden,res,sigma_x,sigma_y,noPart,useWeights_x,useWeights_y)

    # MASKING
    if (useMasks):
        #Define masks in y direction, 0 is 0 on the y-axis. Change if different mask is desired
        top_of_masks = []  #upper limit of each mask in order
        bot_of_masks = []  #lower limit of each mask in order 

        #Define masks in z direction, leftmost z-coordinate = 0. Change if different mask is desired
        left_of_masks= []  #left most limit of each mosk in order
        right_of_masks = []  #right most limit of each mask in order

        new_ydensity = yden  #just in case there are no horizontal masks

        if len(top_of_masks)>0:
            x_f,y_f,xi_f,z_f,px_f,py_f,pz_f,new_ydensity, w = postmasks_y.initProbe(x_c,y_c,xi_c,t0,s1,s2,yden,xiden,res,top_of_masks,bot_of_masks,x_f,y_f,xi_f,z_f,px_f,py_f,pz_f,w)

        if len(left_of_masks)>0:
            x_f,y_f,xi_f,z_f,px_f,py_f,pz_f, w = postmasks_xi.initProbe(x_c,y_c,xi_c,t0,s1,s2,yden,xiden,res,left_of_masks,right_of_masks,x_f,y_f,xi_f,z_f,px_f,py_f,pz_f,new_ydensity,w)    
    # END OF MASKING
    
    
    # Plot data points
    print("Plotting...")
    if (plot2DTracks):
        plot2D.plot(x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, sim_name, shape_name, x_s, noPart)
    if (showQuickEvolution):
        showEvol_Q.plot(x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, sim_name, shape_name, x_s, noPart, iter) # Note: does not use weights
    if (showFullEvolution):
        showEvol_F.plot(x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, w, sim_name, shape_name, noPart, iter)
    if (writeHistData):
        writeHist.plot(x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, sim_name, shape_name, noPart, iter)
    #if (plotWeightsy):
    #    plotWeights.ploty(w_y,y_0,beamy_c,sigma_y)
    #if (plotWeightsx):
    #    plotWeights.plotx(w_x,x_0,xi_0,beamx_c,sigma_x)
    
    #if (saveMovie):
    #    makeAnimation.animate(x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, sim_name, shape_name, noPart, iter)

    # End timing index file runtime
    tf = time.localtime()
    curr_time_f = time.strftime("%H:%M:%S", tf)
    print("End Time: ", curr_time_f)
    print("Duration: ", (time.time() - start_time)/60, " min")
else:
    print("Improper number of arguments. Expected 'python3 index.py <fname> <fname>'")
    exit()
