# Transverse Electron Probe of Laser Wakefield Tracking Script
# Author: Marisa Petrusky - marisa.petrusky@stonybrook.edu
#   This script is designed to take the Lorentz fields of a simulated laser wakefield
#   and obtain the trajectory of an electron probe through a first order Runge Kutta

#   Implemented Simulations:
#   - Quasi3D

#   Instructions on how to add more simulations can be found in the README

#   Derived from Audrey Farrell's electron tracking script: eTracks.py

# Coordinate System
#   z   - Direction of laser propagation (longitudinal)
#   xi  - Position along z relative to wavefront (unnecessary?)
#   r   - Cylindrical coordinate around z
#   phi - Cylindrical coordinate around z, define phi = 0 along x
#   x   - Direction of transverse probe
#   y   - Direction perpendicular to transverse probe

# Python Imports
import sys
import math
import numpy as np
import h5py as h5
import importlib
import pdb
import time
import multiprocessing as mp

# Include file imports
import include.plot2DTracks as plot2D
import include.plot3DTracks as plot3D
import include.showQuickEvolution as showEvol_Q
import include.showFullEvolution as showEvol_F
import include.viewProbe as viewProbe

# Definition of Constants
M_E = 9.109e-31                      # Electron rest mass in kg
EC = 1.60217662e-19                  # Electron charge in C
EP_0 = 8.854187817e-12               # Vacuum permittivity in C/(V m)
C = 299892458                        # Speed of light in vacuum in m/s

# Plotting Scripts
plot2DTracks = False                 # View 2D projections of trajectories
# plot3DTracks = False                 # View 3D model of trajectories
# viewProbeShape = False               # View initial shape of probe separately
showQuickEvolution = False           # View evolution of probe after leaving plasma at inputted x_s in scatter plots
showFullEvolution = False            # View full evolution of probe at hardcoded locations in colored histograms
# Set all others equal False if want animation saved (dependency issue)
saveMovie = False                    # Save mp4 of probe evolution
if (saveMovie):
    import include.makeAnimation as makeAnimation

if __name__ == '__main__':

    # Initialize multiprocessing.Pool()
    pool = mp.Pool(mp.cpu_count())

    # Start of main()

    start_time = time.time()
    t = time.localtime()
    curr_time = time.strftime("%H:%M:%S", t)
    print("Start Time: ", curr_time)

    if (len(sys.argv) == 2):
    # Initialize probe
        input_fname = str(sys.argv[1])
        print("Using initial conditions from ", input_fname)
        init = importlib.import_module(input_fname)
        sim_name = init.simulation_name
        shape_name = init.shape
        den = init.density
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
        s3 = init.s3

        if (sim_name.upper() == 'OSIRIS_CYLINSYMM'):
            import include.simulations.useOsiCylin as sim
        elif (sim_name.upper() == 'QUASI3D'):
            import include.simulations.useQuasi3D as sim
        else:
            print("Simulation name unrecognized. Quitting...")
            exit()

        t0 = sim.getTime()
        plasma_bnds = sim.getBoundCond()

        if (shape_name.upper() == 'CIRCLE'):
            import include.shapes.circle as shape
        elif (shape_name.upper() == 'DISC'):
            import include.shapes.disc as shape
        elif (shape_name.upper() == 'RECTANGLE'):
            import include.shapes.rectangle as shape
        elif (shape_name.upper() == 'VLINE'):
            import include.shapes.vline as shape
        elif (shape_name.upper() == 'HLINE'):
            import include.shapes.hline as shape
        elif (shape_name.upper() == 'SINGLE'):
            import include.shapes.single as shape
        else:
            print("Electron probe shape unrecognized. Quitting...")
            exit()

    # Get arrays of initial coordinates in shape of probe
        x_0, y_0, xi_0, z_0 = shape.initProbe(x_c, y_c, xi_c, t0, s1, s2, s3, den)

        noElec = len(x_0) # Number of electrons to track

    else:
        print("Improper number of arguments. Expected 'python3 eProbe.py <fname>'")

    x_f, y_f, xi_f, z_f, px_f, py_f, pz_f = [pool.apply(eProbe.getTrajectory, args=(x_0[i], y_0[i], xi_0[i], px_0, py_0, pz_0, t0, iter, plasma_bnds, mode)) for i in range(0,noElec)]
    pool.close()

    #x_f, y_f, xi_f, z_f, px_f, py_f, pz_f = [],[],[],[],[],[],[] # Final positions and momenta of electrons

    # for i in range (0, noElec):
    #     xn, yn, xin, zn, pxn, pyn, pzn = getTrajectory(x_0[i], y_0[i], xi_0[i], px_0, py_0, pz_0, t0, iter, plasma_bnds, mode)
    #     x_f.append(xn)
    #     y_f.append(yn)
    #     xi_f.append(xin)
    #     z_f.append(zn)
    #     px_f.append(pxn)
    #     py_f.append(pyn)
    #     pz_f.append(pzn)

    tf = time.localtime()
    curr_time_f = time.strftime("%H:%M:%S", tf)
    print("End Time: ", curr_time_f)
    print("Duration: ", (time.time() - start_time)/60, " min")

    np.savez(fname, x_dat=x_f, y_dat=y_f, xi_dat=xi_f, z_dat=z_f, px_dat=px_f, py_dat=py_f, pz_dat=pz_f)

# Plot data points
    if (plot2DTracks):
        plot2D.plot(x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, sim_name, shape_name, x_s, noElec)
    # if (plot3DTracks):
    #     plot3D.plot(x_dat, y_dat, xi_dat, z_dat, x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, sim_name, shape_name, s1, s2, noElec)
    if (showQuickEvolution):
        showEvol_Q.plot(x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, sim_name, shape_name, x_s, noElec, iter)
    if (showFullEvolution):
        showEvol_F.plot(x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, sim_name, shape_name, noElec, iter)
    # if (viewProbeShape):
    #     viewProbe.plot(x_dat, y_dat, xi_dat, z_dat, sim_name, shape_name, s1, s2, noElec)
    if (saveMovie):
        makeAnimation.animate(x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, sim_name, shape_name, noElec, iter)

#main()
