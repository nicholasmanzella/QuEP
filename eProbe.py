# Transverse Electron Probe of Laser Wakefield Tracking Script
# Author: Marisa Petrusky - marisa.petrusky@stonybrook.edu
#   This script is designed to take the Lorentz fields of a simulated laser wakefield
#   and obtain the trajectory of an electron probe going through them.

#   Implemented Simulations:
#   - Quasi3D

#   Instructions on how to add more simulations can be found in the README

#   Derived from Audrey Farrell's electron tracking script: eTracks.py

# Coordinate System
# z   - Direction of laser propagation (longitudinal)
# xi  - Position along z relative to wavefront (unnecessary?)
# r   - Cylindrical coordinate around z
# phi - Cylindrical coordinate around z, define phi = 0 along x
# x   - Direction of transverse probe
# y   - Direction perpendicular to transverse probe

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
import include.plot3DProbe as plot3DProbe
import include.plot2DProbe as plot2DProbe

# Definition of Constants
M_E = 9.109e-31                      #electron rest mass in kg
EC = 1.60217662e-19                  #electron charge in C
EP_0 = 8.854187817e-12               #vacuum permittivity in C/(V m) (not e-12?)
C = 299892458                        #speed of light in vacuum in m/s
N = 1e15                             #electron number density in 1/m^3
W_P = math.sqrt(N*EC**2/(M_E*EP_0))  #plasma frequency in 1/s

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

    def Momentum(x,y,xi,dt,px,py,pz):
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

        Fx = -1.0 * (sim.EField(2, x, y, xi, r, vx, vy, vz, vr, vphi) + sim.BForce(2, x, y, xi, r, vx, vy, vz, vr, vphi))
        Fy = -1.0 * (sim.EField(3, x, y, xi, r, vx, vy, vz, vr, vphi) + sim.BForce(3, x, y, xi, r, vx, vy, vz, vr, vphi))
        Fz = -1.0 * (sim.EField(1, x, y, xi, r, vx, vy, vz, vr, vphi) + sim.BForce(1, x, y, xi, r, vx, vy, vz, vr, vphi))

        px = px + Fx * dt
        py = py + Fy * dt
        pz = pz + Fz * dt
        p = math.sqrt(px**2 + py**2 + pz**2)
        gam = Gamma(p)
        return px, py, pz, p, gam

    def GetTrajectory(x_0,y_0,xi_0,px_0,py_0,pz_0,t0,iter,plasma_bnds,x_s):
    # Returns array of x, y, z, t

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
            #print("Iter = ", i)
            px, py, pz, p, gam = Momentum(xn, yn, xin, dt, px, py, pz)

            vxn = Velocity(px, p)
            vyn = Velocity(py, p)
            vzn = Velocity(pz, p)

            xn += vxn * dt
            yn += vyn * dt
            zn += vzn * dt
            rn = math.sqrt(xn**2 + yn**2)

            t += dt
            xin = zn - t

            # If electron leaves cell, switch to ballistic trajectory
            if (xin < plasma_bnds[0] or xin > plasma_bnds[1] or rn > plasma_bnds[2]):
                return xn, yn, xin, zn

        print("Tracking quit due to more than ", iter, " iterations")
        return xn, yn, xin, zn

    # Start of main()

    if len(sys.argv) == 2:
    # Initialize probe
        input_fname = str(sys.argv[1])
        print("Using initial conditions from ", input_fname)
        init = importlib.import_module(input_fname)
        sim_name = init.simulation_name
        shape_name = init.shape
        den = init.density
        iter = init.iterations
        x_c = init.x_c
        y_c = init.y_c
        xi_c = init.xi_c
        px_0 = init.px_0
        py_0 = init.py_0
        pz_0 = init.pz_0
        x_s = init.x_s
        s1 = init.s1
        s2 = init.s2

        if (sim_name.upper() == 'OSIRIS_CYLINSYMM'):
            import include.simulations.useOsiCylin as sim
        elif (sim_name.upper() == 'QUASI3D'):
            import include.simulations.useQuasi3D as sim
        else:
            print("Simulation name unrecognized. Quitting...")

        t0 = sim.getTime()
        plasma_bnds = sim.getBoundCond()

        if (shape_name.upper() == 'RIBBON'):
            import include.ribbon as shape
        else:
            print("Electron probe shape unrecognized. Quitting...")

    # Get arrays of initial coordinates in shape of probe
        x_0, y_0, xi_0 = shape.initProbe(x_c, y_c, xi_c, s1, s2, den)
        noElec = len(x_0) # Number of electrons to track

    else:
        print("Improper number of arguments. Expected 'python3 eProbe.py <fname>'")
        return

    x_f, y_f, xi_f, z_f = [],[],[],[] # Final positions of electrons

    for i in range (0, noElec):
        x, y, xi, z = GetTrajectory(x_0[i], y_0[i], xi_0[i], px_0, py_0, pz_0, t0, iter, plasma_bnds, x_s)
        x_f.append(x)
        y_f.append(y)
        xi_f.append(xi)
        z_f.append(z)

# Plot data points
    plot3DProbe.plot(x_f, y_f, xi_f, z_f, sim_name, shape_name)
    plot2DProbe.plot(x_f, y_f, xi_f, z_f, sim_name, shape_name)

main()
