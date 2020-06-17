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
import include.plot3DTracks as plot3DTracks
import include.plotGamma as plotGamma
import include.plot2DTracks as plot2DTracks

# Definition of Constants
M_E = 9.109e-31                  #electron rest mass in kg
EC = 1.60217662e-19              #electron charge in C
EP_0 = 8.854187817e-12               #vacuum permittivity in C/(V m) (not e-12?)
C = 299892458                    #speed of light in vacuum in m/s
N = 1e15                         #electron number density in 1/m^3
W_P = math.sqrt(N*EC**2/(M_E*EP_0))   #plasma frequency in 1/s

def main():

    def Gamma(p):
        return math.sqrt(1.0 + p**2)

    def Velocity(px,ptot):
    # Returns relativistic velocity from momentum
        return px / Gamma(ptot)

    def sortVelocity(x,y,vx,vy,vr):
    # Would prefer a shorter way to do this
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
        #pdb.set_trace()
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

    def GetTrajectory(x_0,y_0,z_0,px_0,py_0,pz_0,t0,iter,bounds):
    # Returns array of x, y, z, t
        x_dat, y_dat, z_dat, t_dat, xi_dat, gam_dat = [],[],[],[],[],[]

        t = t0            # Start time in 1/w_p
        dt = 0.005                   # Time step in 1/w_p
        xn = x_0                     # Positions in c/w_p
        yn = y_0
        zn = z_0

        px = px_0                    # Momenta in m_e c
        py = py_0
        pz = pz_0

        xin = zn - t0

    # Iterate through position and time using a linear approximation until (?)
        i = 0

        while i < iter:
    # Determine new momentum and velocity from this position
            #print("Iter = ", i)
            px, py, pz, p, gam = Momentum(xn, yn, xin, dt, px, py, pz)

            vxn = Velocity(px, p)
            vyn = Velocity(py, p)
            vzn = Velocity(pz, p)

    # Add former data points to lists
            x_dat.append(xn)
            y_dat.append(yn)
            z_dat.append(zn)
            xi_dat.append(xin)
            gam_dat.append(gam)
            t_dat.append(t)

            xn += vxn * dt
            yn += vyn * dt
            zn += vzn * dt
            rn = math.sqrt(xn**2 + yn**2)

            t += dt
            i += 1

            xin = zn - t

            if (i > iter):
                print("Tracking quit due to more than ", iter, " iterations")
                return np.array(x_dat), np.array(y_dat), np.array(z_dat), np.array(t_dat), np.array(xi_dat), np.array(gam_dat)
            if (xin < bounds[0] or xin > bounds[1] or rn > bounds[2]):
                print("Tracking quit due to coordinates out of range")
                return np.array(x_dat), np.array(y_dat), np.array(z_dat), np.array(t_dat), np.array(xi_dat), np.array(gam_dat)
        return np.array(x_dat), np.array(y_dat), np.array(z_dat), np.array(t_dat), np.array(xi_dat), np.array(gam_dat)

    if len(sys.argv) == 2:
        input_fname = str(sys.argv[1])
        print("Using initial conditions from ", input_fname)
        init = importlib.import_module(input_fname)
        x_0 = init.x_0
        y_0 = init.y_0
        xi_0 = init.xi_0
        px_0 = init.px_0
        py_0 = init.py_0
        pz_0 = init.pz_0
        iter = init.iterations
        sim_name = init.simulation_name
        if (sim_name.upper() == 'OSIRIS_CYLINSYMM'):
            import include.useOsiCylin as sim
        elif (sim_name.upper() == 'QUASI3D'):
            import include.useQuasi3D as sim

        t0 = sim.getTime()
        z_0 = xi_0 + t0
        print("z0 = ", z_0)
        bounds = sim.getBoundCond()

    elif len(sys.argv) == 1:
# Get initial position and momentum from user input
        x_0 = float(input("Initial x position (c/w_p): "))
        y_0 = float(input("Initial y position (c/w_p): "))
        xi_0 = float(input("Initial z position (c/w_p): "))
        px_0 = float(input("Initial x momentum (m_e c): "))
        py_0 = float(input("Initial y momentum (m_e c): "))
        pz_0 = float(input("Initial z momentum (m_e c): "))
        sim = str(input("Simulation Type: "))
        if (sim_name.upper() == 'OSIRIS_CYLINSYMM'):
            import include.useOsiCylin as sim
        elif (sim_name.upper() == 'QUASI3D'):
            import include.useQuasi3D as sim
        t0 = sim.getTime() # Get normalized time units
        z_0 = xi_0 + t0
        bounds = sim.getBoundCond()
    else:
        print("Improper number of arguments. Expected 'python3 eProbe.py' or 'python3 eProbe.py <fname>'")
        return

# Simulate trajectory and create n-length array of data for plotting
    x_dat, y_dat, z_dat, t_dat, xi_dat, gam_dat = GetTrajectory(x_0, y_0, z_0, px_0, py_0, pz_0, t0, iter, bounds)
# Plot data points

    avgGam = sum(gam_dat)/len(gam_dat)
    kbeta = W_P/(C * math.sqrt(2 * avgGam))
    print("Average Gamma over one oscillation = ", avgGam)
    print("Betatron Wave No = ", kbeta)
    wavel = (2 * math.pi / kbeta) # Normalized
    print("Lambda = ", wavel)

    #plot3DTracks.plot(x_dat, y_dat, z_dat, t_dat, xi_dat, sim_name)
    plot2DTracks.plot(x_dat, y_dat, z_dat, t_dat, xi_dat, sim_name)
    plotGamma.plot(x_dat, y_dat, z_dat, t_dat, xi_dat, gam_dat)

main()
