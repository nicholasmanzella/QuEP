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
import matplotlib.pyplot as plt
import matplotlib.colors as col
import pdb
import time

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
plot2DTracks = True                 # View 2D projections of trajectories
# plot3DTracks = False                 # View 3D model of trajectories
# viewProbeShape = False               # View initial shape of probe separately
showQuickEvolution = False           # View evolution of probe after leaving plasma at inputted x_s in scatter plots
showFullEvolution = False            # View full evolution of probe at hardcoded locations in colored histograms
# Set all others equal False if want animation saved (dependency issue)
saveMovie = False                    # Save mp4 of probe evolution
if (saveMovie):
    import include.makeAnimation as makeAnimation

def main():

    def Gamma(p):
        return math.sqrt(1.0 + p**2)

    def Velocity(px,ptot):
    # Returns relativistic velocity from momentum
        return px / Gamma(ptot)

    def sortVelocity(x,y,vx,vy,vr):
    # Obtain proper sign of velocity based on quadrant
        if (x >= 0 and y >= 0):                  # Quadrant 1
            if (vx >= 0 and vy >= 0):
                return vr
            elif (vx < 0 and vy < 0):
                return -1.0 * vr
            elif (abs(vx) > abs(vy)):
                if vx > 0:
                    return vr
                else:
                    return -1.0 * vr
            elif (abs(vy) > abs(vx)):
                if vy > 0:
                    return vr
                else:
                    return -1.0 * vr
        elif (x < 0 and y >= 0):                 # Quadrant 2
            if (vx <= 0 and vy >= 0):
                return vr
            elif (vx > 0 and vy < 0):
                return -1.0 * vr
            elif (abs(vx) > abs(vy)):
                if vx > 0:
                    return -1.0 * vr
                else:
                    return vr
            elif (abs(vy) > abs(vx)):
                if vy > 0:
                    return vr
                else:
                    return -1.0 * vr
        elif (x < 0 and y < 0):                   # Quadrant 3
            if (vx >= 0 and vy >= 0):
                return -1.0 * vr
            elif (vx < 0 and vy < 0):
                return vr
            elif (abs(vx) > abs(vy)):
                if vx > 0:
                    return -1.0 * vr
                else:
                    return vr
            elif (abs(vy) > abs(vx)):
                if vy > 0:
                    return vr
                else:
                    return -1.0 * vr
        elif (x >= 0 and y < 0):                 # Quadrant 4
            if (vx >= 0 and vy <= 0):
                return vr
            elif (vx < 0 and vy > 0):
                return -1.0 * vr
            elif (abs(vx) > abs(vy)):
                if vx > 0:
                    return vr
                else:
                    return -1.0 * vr
            elif (abs(vy) > abs(vx)):
                if vy > 0:
                    return -1.0 * vr
                else:
                    return vr

    def Momentum(x,y,xi,dt,px,py,pz,mode):
    # Returns the new momentum after dt, in units of c in the axis direction
        p = math.sqrt(px**2 + py**2 + pz**2)
        vx = Velocity(px, p)
        vy = Velocity(py, p)
        vz = Velocity(pz, p)
        r = math.sqrt(x**2 + y**2)
        vr = math.sqrt(vx**2 + vy**2)
        vr = sortVelocity(x, y, vx, vy, vr)
        if (r > 0):
           vphi = vr/r
        else:
           vphi = 0

        Fx = -1.0 * (sim.EField(2, x, y, xi, r, vx, vy, vz, vr, vphi, mode) + sim.BForce(2, x, y, xi, r, vx, vy, vz, vr, vphi, mode))
        Fy = -1.0 * (sim.EField(3, x, y, xi, r, vx, vy, vz, vr, vphi, mode) + sim.BForce(3, x, y, xi, r, vx, vy, vz, vr, vphi, mode))
        Fz = -1.0 * (sim.EField(1, x, y, xi, r, vx, vy, vz, vr, vphi, mode) + sim.BForce(1, x, y, xi, r, vx, vy, vz, vr, vphi, mode))

        px = px + Fx * dt
        py = py + Fy * dt
        pz = pz + Fz * dt
        p = math.sqrt(px**2 + py**2 + pz**2)
        gam = Gamma(p)
        return px, py, pz, p, gam, Fx, Fy, Fz

    def getTrajectory(x_0,y_0,xi_0,px_0,py_0,pz_0,t0,iter,plasma_bnds,mode):
    # Returns array of x, y, xi, z, and final x, y, xi, z, px, py, pz

        t = t0                       # Start time in 1/w_p
        dt = 0.005                   # Time step in 1/w_p
        xn = x_0                     # Positions in c/w_p
        yn = y_0
        xin = xi_0
        zn = xin + t0

        px = px_0                    # Momenta in m_e c
        py = py_0
        pz = pz_0

    # Iterate through position and time using a linear approximation
        for i in range(0, iter):
        # Determine new momentum and velocity from this position
            px, py, pz, p, gam, Fx, Fy, Fz = Momentum(xn, yn, xin, dt, px, py, pz, mode)

            vxn = Velocity(px, p)
            vyn = Velocity(py, p)
            vzn = Velocity(pz, p)

            xn += vxn * dt
            yn += vyn * dt
            zn += vzn * dt
            rn = math.sqrt(xn**2 + yn**2)

            t += dt
            xin = zn - t

            # If electron leaves cell, quit tracking
            if (xin < plasma_bnds[0] or xin > plasma_bnds[1] or rn > plasma_bnds[2]):
                return xn, yn, xin, zn, px, py, pz

        print("Tracking quit due to more than ", iter, " iterations in plasma")
        return xn, yn, xin, zn, px, py, pz

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
        milestone = np.linspace(0, noElec, 11)
        percent = np.linspace(0, 100, 11)

    else:
        print("Improper number of arguments. Expected 'python3 eProbe.py <fname>'")
        return

    x_f, y_f, xi_f, z_f, px_f, py_f, pz_f = [],[],[],[],[],[],[] # Final positions and momenta of electrons

    j = 0
    for i in range (0, noElec):
        if (j == 10 and i == noElec-1):
            print("Simulation " + str(percent[j]) + "% Complete", end='\n')
        elif (i == milestone[j]):
            print("Simulation " + str(percent[j]) + "% Complete", end='\r' )
            #print("i = ", i)
            j += 1
            #pdb.set_trace()
        xn, yn, xin, zn, pxn, pyn, pzn = getTrajectory(x_0[i], y_0[i], xi_0[i], px_0, py_0, pz_0, t0, iter, plasma_bnds, mode)
        x_f.append(xn)
        y_f.append(yn)
        xi_f.append(xin)
        z_f.append(zn)
        px_f.append(pxn)
        py_f.append(pyn)
        pz_f.append(pzn)

    tf = time.localtime()
    curr_time_f = time.strftime("%H:%M:%S", tf)
    print("End Time: ", curr_time_f)
    print("Duration: ", (time.time() - start_time)/60, " min")

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
main()
