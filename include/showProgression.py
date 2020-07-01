# Script for generating 2D plots of electron trajectories

import numpy as np
import scipy as sp
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import pdb
import math
from scipy.interpolate import make_interp_spline, BSpline

slices = 5

def find_nearest_index(array,value):
    idx = np.searchsorted(array, value, side="right")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1
    else:
        return idx

def plot(x_dat,y_dat,z_dat,xi_dat,sim_name,shape_name,x_s,noElec,iter):
    shape_name = shape_name.capitalize()
# Get x-axis
    if (sim_name.upper() == 'OSIRIS_CYLINSYMM'):
        import include.simulations.useOsiCylin as sim
    elif (sim_name.upper() == 'QUASI3D'):
        import include.simulations.useQuasi3D as sim
    else:
        print("Simulation name unrecognized. Quitting...")
        exit()
    xaxis = np.linspace(x_dat[0,0], x_dat[0,-1], len(x_dat[0]))

# Define locations of "snapshots" of probe
    dx = x_s - x_dat[0,0]
    step = dx / slices
    xsnap = []
    for i in range(0,slices+1):
        xn = x_dat[0,0] + i * step
        xsnap.append(xn)

# Retrieve arrays of y, z, and xi at snapshots
    yslice = np.empty([slices+1, noElec])
    zslice = np.empty([slices+1, noElec])
    xislice = np.empty([slices+1, noElec])

    for i in range(0,slices+1):
        #print("Slice # ", i)
        xIter = find_nearest_index(xaxis, xsnap[i]) # Find iteration number of current slice
        #print("xIter = ", xIter)
        for j in range(0,noElec):
            yslice[i, j] = y_dat[j, xIter]
            xislice[i, j] = xi_dat[j, xIter]
            zslice[i, j] = z_dat[j, xIter]
            #print("(y,xi) = ", yslice[i, j], xislice[i,j])

    fig5, axs = plt.subplots(3, sharex=True)
    fig5.suptitle("Progression of " + shape_name + " EProbe")

    for i in range(0, 3):
        axs[i].set_title("Snapshot at X = " + str(xsnap[i]) + " c/$\omega_p$")
        axs[i].scatter(xislice[i,:], yslice[i,:])
        axs[i].set_ylim(-1,1)
    for ax in axs.flat:
        ax.set(xlabel = '$\\xi$ ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')
    for ax in axs.flat:
        ax.label_outer()

    fig6, axs2 = plt.subplots(3, sharex=True)
    fig6.suptitle("Progression of " + shape_name + " EProbe")

    for i in range(0, 3):
        axs2[i].set_title("Snapshot at X = " + str(xsnap[i+3]) + " c/$\omega_p$")
        axs2[i].scatter(xislice[i+3,:], yslice[i+3,:], zorder=2)
        axs2[i].plot(xislice[i+3,:], yslice[i+3,:], 'C3', zorder=1)
        axs2[i].set_ylim(-1,1)
    for ax in axs2.flat:
        ax.set(xlabel = '$\\xi$ ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')
    for ax in axs2.flat:
        ax.label_outer()

    fig7, axs3 = plt.subplots(3, sharex=True)
    fig7.suptitle("Progression of " + shape_name + " EProbe")

    for i in range(0, 3):
        axs3[i].set_title("Snapshot at X = " + str(xsnap[i]) + " c/$\omega_p$")
        axs3[i].scatter(zslice[i,:], yslice[i,:],zorder=2)
        axs3[i].set_ylim(-1,1)
    for ax in axs3.flat:
        ax.set(xlabel = 'Z ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')
    for ax in axs3.flat:
        ax.label_outer()

    fig8, axs4 = plt.subplots(3, sharex=True)
    fig8.suptitle("Progression of " + shape_name + " EProbe")

    for i in range(0, 3):
        axs4[i].set_title("Snapshot at X = " + str(xsnap[i+3]) + " c/$\omega_p$")
        axs4[i].scatter(zslice[i+3,:], yslice[i+3,:])
        axs4[i].set_ylim(-1,1)
    for ax in axs4.flat:
        ax.set(xlabel = 'Z ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')
    for ax in axs4.flat:
        ax.label_outer()

    fig5.show()
    #fig.tight_layout()
    fig6.show()
    #fig7.show()
    #fig8.show()
    input()
