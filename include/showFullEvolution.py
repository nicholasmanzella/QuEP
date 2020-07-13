# Script for showing full evolution of probe at hardcoded snapshot locations in and out of plasma

import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import pdb
import math

# Definition of Constants
M_E = 9.109e-31                      # Electron rest mass in kg
EC = 1.60217662e-19                  # Electron charge in C
EP_0 = 8.854187817e-12               # Vacuum permittivity in C/(V m)
C = 299892458                        # Speed of light in vacuum in m/s

# Snapshot locations (12 total, in mm):
#x_s = [0, 1, 2, 3, 4, 5, 6, 10, 20, 100, 200, 500]
x_s = [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300]

# Color Scheme
BW = False # Sequential
Viridis = True # Sequential + Perceptually Uniform

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

def find_nearest_index(array,value):
    idx = np.searchsorted(array, value, side="right")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1
    else:
        return idx

def plot(x_dat,y_dat,xi_dat,z_dat,x_f,y_f,xi_f,z_f,px_f,py_f,pz_f,sim_name,shape_name,noElec,iter):
# Plot evolution of probe after leaving plasma
    if (sim_name.upper() == 'OSIRIS_CYLINSYMM'):
        import include.simulations.useOsiCylin as sim
    elif (sim_name.upper() == 'QUASI3D'):
        import include.simulations.useQuasi3D as sim
    else:
        print("Simulation name unrecognized. Quitting...")
        exit()

    W_P = sim.getPlasFreq()
    plasma_bnds = sim.getBoundCond()
    shape_name = shape_name.capitalize()
    xaxis = np.linspace(x_dat[0,0], x_dat[0,-1], len(x_dat[0]))

# Normalize screen distances
    slices = len(x_s)
    xs_norm = []
    for i in range(0,slices):
        xs_norm.append(x_s[i] * W_P * 10**(-3) / C)

# Generate arrays of coordinates at origin + each screen
    yslice = np.empty([slices, noElec])
    xislice = np.empty([slices, noElec])
    zslice = np.empty([slices, noElec])

# Project positions at distances in x_s
    for i in range(0,slices):
        # If x_s out of plasma, use ballistic trajectory
        if (abs(xs_norm[i]) > plasma_bnds[2]):
            for j in range(0,noElec):
                yslice[i, j], xislice[i, j], zslice[i, j] = getBallisticTraj(x_f[j], y_f[j], xi_f[j], z_f[j], px_f[j], py_f[j], pz_f[j], xs_norm[i])
        else:
            xIter = find_nearest_index(xaxis, xs_norm[i]) # Find iteration number of current slice
            for j in range(0,noElec):
                yslice[i, j] = y_dat[j, xIter]
                xislice[i, j] = xi_dat[j, xIter]
                zslice[i, j] = z_dat[j, xIter]

# Plot slices
    binsizez = 50
    binsizey = 40
    if (BW):
        cmap = plt.cm.gist_gray
    elif (Viridis):
        cmap = plt.cm.viridis
    else:
        cmap = plt.cm.gist_gray

    fig5, axs = plt.subplots(3, sharey=True, figsize=(8, 10), dpi=80)
    fig5.suptitle("Progression of " + shape_name + " EProbe")
    for i in range(0, 3):
        axs[i].set_title("Snapshot at X = " + str(x_s[i]) + " mm")
        axs[i].hist2d(zslice[i,:], yslice[i,:], bins=(binsizez,binsizey), cmap=cmap)
        #axs[i].scatter(zslice[i,:], yslice[i,:], c='C0', zorder=1)
        axs[i].set_ylim(-7.5,7.5)
        if (BW):
            axs[i].set_facecolor('black')
        elif (Viridis):
            axs[i].set_facecolor('#440154')
        else:
            axs[i].set_facecolor('black')

    axs[2].set(xlabel = 'Z ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')


    fig6, axs2 = plt.subplots(3, sharey=True, figsize=(8, 10), dpi=80)
    fig6.suptitle("Progression of " + shape_name + " EProbe")
    for i in range(0, 3):
        axs2[i].set_title("Snapshot at X = " + str(x_s[i+3]) + " mm")
        axs2[i].hist2d(zslice[i+3,:], yslice[i+3,:], bins=(binsizez,binsizey), cmap=cmap)
        #axs2[i].scatter(zslice[i+3,:], yslice[i+3,:], c='C0', zorder=1)
        axs2[i].set_ylim(-7.5,7.5)
        if (BW):
            axs2[i].set_facecolor('black')
        elif (Viridis):
            axs2[i].set_facecolor('#440154')
        else:
            axs2[i].set_facecolor('black')

    axs2[2].set(xlabel = 'Z ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')


    fig7, axs3 = plt.subplots(3, sharey=True, figsize=(8, 10), dpi=80)
    fig7.suptitle("Progression of " + shape_name + " EProbe")
    for i in range(0, 3):
        axs3[i].set_title("Snapshot at X = " + str(x_s[i+6]) + " mm")
        axs3[i].hist2d(zslice[i+6,:], yslice[i+6,:], bins=(binsizez,binsizey), cmap=cmap)
        #axs3[i].scatter(zslice[i+6,:], yslice[i+6,:], zorder=2)
        axs3[i].set_ylim(-7.5,7.5)
        if (BW):
            axs3[i].set_facecolor('black')
        elif (Viridis):
            axs3[i].set_facecolor('#440154')
        else:
            axs3[i].set_facecolor('black')

    axs3[2].set(xlabel = 'Z ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')


    fig8, axs4 = plt.subplots(3, sharey=True, figsize=(8, 10), dpi=80)
    fig8.suptitle("Progression of " + shape_name + " EProbe")
    for i in range(0, 3):
        axs4[i].set_title("Snapshot at X = " + str(x_s[i+9]) + " mm")
        axs4[i].hist2d(zslice[i+9,:], yslice[i+9,:], bins=(binsizez,binsizey), cmap=cmap)
        #axs4[i].scatter(zslice[i+9,:], yslice[i+9,:])
        axs4[i].set_ylim(-7.5,7.5)
        if (BW):
            axs4[i].set_facecolor('black')
        elif (Viridis):
            axs4[i].set_facecolor('#440154')
        else:
            axs4[i].set_facecolor('black')

    axs4[2].set(xlabel = 'Z ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')


    fig5.show()
    fig6.show()
    fig7.show()
    fig8.show()

    input()
