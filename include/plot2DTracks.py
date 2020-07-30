# Script for generating 2D plots of electron trajectories

import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import pdb

def Gamma(p):
    return math.sqrt(1.0 + p**2)

def Velocity(px,ptot):
# Returns relativistic velocity from momentum
    return px / Gamma(ptot)

def getBallisticTraj(x_0,y_0,xi_0,z_0,px,py,pz,x_s):
# Use ballistic matrix to find positions on screens
    dx = x_s - x_0
    y_f = y_0 + dx * (py/px)
    z_f = z_0 + dx * (pz/px)

# Find time traveled to get proper xi
    p = math.sqrt(px**2 + py**2 + pz**2)
    vx = Velocity(px, p)
    vy = Velocity(py, p)
    vz = Velocity(pz, p)
    vtot = math.sqrt(vx**2 + vy**2 + vz**2)
    dtot = math.sqrt((x_s - x_0)**2 + (y_f - y_0)**2 + (z_f - z_0)**2)
    t = dtot/vtot

    xi_f = xi_0 + dx * (pz/px) + t

    return y_f, xi_f, z_f

def plot(x_f,y_f,xi_f,z_f,px_f,py_f,pz_f,sim_name,shape_name,s1,s2,noElec):
# Normalize variables
    W_P = sim.getPlasFreq()
    plasma_bnds = sim.getBoundCond()
    shape_name = shape_name.capitalize()
    shape_name.capitalize()

# Initialize lists of points
    x_dat, xi_dat, y_dat, z_dat = [],[],[],[]
    xs_norm = x_s[-1] * W_P * 10**(-3) / C

    for i in range(0,noElec):
        x_dat.append(x_f)
        y_dat.append(y_f[i])
        xi_dat.append(xi_f[i])
        z_dat.append(z_f[i])

# 2D: Xi-X
    fig1 = plt.figure(1)
    ax1 = plt.axes()
    ax1.set_xlabel("X ($c/\omega_p$)")
    ax1.set_ylabel("$\\xi$ ($c/\omega_p$)")
    ax1.tick_params(axis='y', labelcolor='k')
    ax1.set_title(shape_name + " Electron Probe Trajectory")

    for i in range(0, noElec):
        ax1.plot(x_dat[i,:], xi_dat[i,:], 'k', label='$\\xi$-X Trajectory') # Want vertical axis as y

    #fig1.legend(bbox_to_anchor=(0.88, 0.94), bbox_transform=plt.gcf().transFigure)

# 2D: Y-X
    fig2 = plt.figure(2)
    ax2 = plt.axes()
    ax2.set_xlabel("X ($c/\omega_p$)")
    ax2.set_ylabel("Y ($c/\omega_p$)")
    ax2.tick_params(axis='y', labelcolor='k')
    ax2.set_title(shape_name + " Electron Probe Trajectory")

    for i in range(0, noElec):
        ax2.plot(x_dat[i,:], y_dat[i,:], 'k', label='Y-X Trajectory') # Want vertical axis as y

    #fig2.legend(bbox_to_anchor=(0.88, 0.94), bbox_transform=plt.gcf().transFigure)

    fig1.tight_layout()
    fig1.show()
    fig2.tight_layout()
    fig2.show()
    input()
