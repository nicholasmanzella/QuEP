# Transverse Electron Probe of Laser Wakefield Tracking Script
# Author: Marisa Petrusky - marisa.petrusky@stonybrook.edu
#   This script is designed to simulate the probing of a laser wakefield
#   with an electron beam.
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

# Include file imports
import include.plotTracks as plotTracks
import include.getOsirisFields as osiris

# Definition of Constants
M_E = 9.109e-31                  #electron rest mass in kg
EC = 1.60217662e-19              #electron charge in C
EP_0 = 8.854187817               #vacuum permittivity in C/(V m) (not e-12?)
C = 299892458                    #speed of light in vacuum in m/s
N = 1e23                         #electron number density in 1/m^3
W_P = math.sqrt(N*EC**2/(M_E*EP_0))   #plasma frequency in 1/s

# Retrieve simulated fields from OSIRIS simulations
r_sim, xi_sim, t0 = osiris.axes()
Er_sim = osiris.transE()
Ez_sim = osiris.longE()
Bphi_sim = osiris.phiB()

def find_nearest_index(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1
    else:
        return idx

def GetPhi(x,y):
    return math.atan2(y,x) # From -pi to pi

def EField(x,y,z,axis):
# axis = 1 refers to x-axis field
# axis = 2 refers to y-axis field
# axis = 3 refers to z-axis field
# axis = 4 refers to r-axis field
    r = math.sqrt(x**2 + y**2)
    phi = GetPhi(x, y)
    zDex = find_nearest_index(xi_sim, z)
    rDex = find_nearest_index(r_sim, r)
    if axis == 1: # x axis
        return Er_sim[rDex, zDex] * math.cos(phi)
    elif axis == 2:
        return Er_sim[rDex, zDex] * math.sin(phi)
    elif axis == 3:
        return Ez_sim[rDex, zDex]
    elif axis == 4:
        return -1.0*Er_sim[rDex, zDex]

def BField(x,y,z,axis):
# axis = 1 refers to x-axis field
# axis = 2 refers to y-axis field
# axis = 3 refers to z-axis field
    r = math.sqrt(x**2 + y**2)
    phi = GetPhi(x, y)
    zDex = find_nearest_index(xi_sim, z)
    rDex = find_nearest_index(r_sim, r)
    if axis == 1:
        return -1.0 * Bphi_sim[rDex, zDex] * math.sin(phi)
    elif axis == 2:
        return Bphi_sim[rDex, zDex] * math.cos(phi)
    elif axis == 3:
        return 0

def Gamma(p):
    return math.sqrt(1.0 + p**2)

def Velocity(px,ptot):
# Returns relativistic velocity from momentum
    return px / Gamma(ptot)

def Momentum(x,y,z,dt,px,py,pz):
# Returns the new momentum after dt, in units of c in the axis direction
    p = math.sqrt(px**2 + py**2 + pz**2)
    vx = Velocity(px,p)
    vy = Velocity(py,p)
    vz = Velocity(pz,p)

    Fx = -1.0 * (EField(x, y, z, 1) - vz * BField(x, y, z, 2))
    Fy = -1.0 * (EField(x, y, z, 2) + vz * BField(x, y, z, 1))
    Fz = -1.0 * (EField(x, y, z, 3) + vx * BField(x, y, z, 2) - vy * BField(x, y, z, 1))

    px = px + Fx * dt
    py = py + Fy * dt
    pz = pz + Fz * dt
    p = math.sqrt(px**2 + py**2 + pz**2)
    return px, py, pz, p

def GetTrajectory(x_0,y_0,z_0,px_0,py_0,pz_0):
# Returns array of x, y, z, t
    x_dat, y_dat, z_dat, t_dat, E_dat, xi_dat = [],[],[],[],[],[]

    t = t0                       # Start time in 1/w_p
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

    while i < 10000000:

# Determine new momentum and velocity from this position
        px, py, pz, p = Momentum(xn, yn, xin, dt, px, py, pz)

        vxn = Velocity(px, p)
        vyn = Velocity(py, p)
        vzn = Velocity(pz, p)

# Add former data points to lists
        x_dat.append(xn)
        y_dat.append(yn)
        z_dat.append(zn)
        E_dat.append( EField(xn, yn, zn, 4) ) # Might want EField in terms of r for plotting?

        xi_dat.append(xin)

        xn += vxn * dt
        yn += vyn * dt
        zn += vzn * dt
        rn = math.sqrt(xn**2 + yn**2)

        t += dt
        i += 1

        xin = zn - t

        if i > 10000000:
            print("Tracking quit due to more than 10k iterations")
            return np.array(x_dat), np.array(y_dat), np.array(z_dat), np.array(t_dat), np.array(E_dat), np.array(xi_dat)
        if xin < 0 or xin > 8 or rn > 6:
            print("Tracking quit due to coordinates out of range")
            return np.array(x_dat), np.array(y_dat), np.array(z_dat), np.array(t_dat), np.array(E_dat), np.array(xi_dat)
    return np.array(x_dat), np.array(y_dat), np.array(z_dat), np.array(t_dat), np.array(E_dat), np.array(xi_dat)

def main():
    if len(sys.argv) == 2:
        input_fname = str(sys.argv[1])
        print("Using initial conditions from ", input_fname)
        init = importlib.import_module(input_fname)
        x_0 = init.x_0
        y_0 = init.y_0
        xi_0 = init.xi_0
        z_0 = xi_0 + t0
        px_0 = init.px_0
        py_0 = init.py_0
        pz_0 = init.pz_0
        track = init.track
    elif len(sys.argv) == 1:
# Get initial position and momentum from user input
        x_0 = float(input("Initial x position (c/w_p): "))
        y_0 = float(input("Initial y position (c/w_p): "))
        z_0 = float(input("Initial z position (c/w_p): "))
        px_0 = float(input("Initial x momentum (m_e c): "))
        py_0 = float(input("Initial y momentum (m_e c): "))
        pz_0 = float(input("Initial z momentum (m_e c): "))
        track = 'med'
    else:
        print("Improper number of arguments. Expected 'python3 eProbe.py' or 'python3 eProbe.py <fname>'")
        return

# Simulate trajectory and create n-length array of data for plotting
    x_dat, y_dat, z_dat, t_dat, E_dat, xi_dat = GetTrajectory(x_0, y_0, z_0, px_0, py_0, pz_0)
    # Plot data points
    plotTracks.plot(x_dat, y_dat, z_dat, t_dat, E_dat)

main()
