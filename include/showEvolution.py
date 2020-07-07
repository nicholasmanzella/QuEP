# Script for generating 2D plots of electron trajectories

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

def getBallisticTraj(x_0,y_0,xi_0,z_0,px,py,pz,x_s):
# Use ballistic matrix to find positions on screens
    dx = x_s - x_0
    y_f = y_0 + dx * (py/px)
    xi_f = xi_0 + dx * (pz/px)
    z_f = z_0 + dx * (pz/px)
    return y_f, xi_f, z_f

def plot(x_dat,y_dat,xi_dat,z_dat,x_f,y_f,xi_f,z_f,px_f,py_f,pz_f,sim_name,shape_name,x_s,noElec,iter):
# Plot evolution of probe after leaving plasma
    if (sim_name.upper() == 'OSIRIS_CYLINSYMM'):
        import include.simulations.useOsiCylin as sim
    elif (sim_name.upper() == 'QUASI3D'):
        import include.simulations.useQuasi3D as sim
    else:
        print("Simulation name unrecognized. Quitting...")
        exit()

    W_P = sim.getPlasFreq()
    shape_name = shape_name.capitalize()
    slices = len(x_s)
    xs_norm = []
    xs_norm.append(x_dat[0, 0] * W_P * 10**(-3) / C)
    for i in range(0,slices):
        xs_norm.append(x_s[i] * W_P * 10**(-3) / C) # Convert screen distances

# Generate arrays of coordinates at origin + each screen
    yslice = np.empty([slices+1, noElec])
    xislice = np.empty([slices+1, noElec])
    zslice = np.empty([slices+1, noElec])
# Fill first position with initial probe shape
    for i in range(0, noElec):
        yslice[0, i] = y_dat[i, 0]
        xislice[0, i] = xi_dat[i, 0]
        zslice[0, i] = z_dat[i, 0]
# Project positions at distances in x_s
    for i in range(1,slices+1):
        for j in range(0,noElec):
            yslice[i, j], xislice[i, j], zslice[i, j] = getBallisticTraj(x_f[j], y_f[j], xi_f[j], z_f[j], px_f[j], py_f[j], pz_f[j], xs_norm[i-1])
# Plot slices
    fig5, axs = plt.subplots(3, sharey=True)
    fig5.suptitle("Progression of " + shape_name + " EProbe")

    x_s = [x_dat[0,0] * W_P * 10**(-3) / C] + x_s

    for i in range(0, 3):
        axs[i].set_title("Snapshot at X = " + str(x_s[i]) + " mm")
        #axs[i].hist2d(xislice[i,:], yslice[i,:], bins=(50,50), cmap=plt.cm.jet)
        axs[i].scatter(xislice[i,:], yslice[i,:], c='C0', zorder=1)
        #axs[i].set_ylim(-2,2)
    #for ax in axs.flat:
        #ax.set(xlabel = '$\\xi$ ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')
        #ax.label_outer()
        axs[2].set(xlabel = '$\\xi$ ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')

    fig6, axs2 = plt.subplots(3, sharey=True)
    fig6.suptitle("Progression of " + shape_name + " EProbe")

    for i in range(0, 3):
        axs2[i].set_title("Snapshot at X = " + str(x_s[i+3]) + " mm")
        #axs2[i].hist2d(xislice[i+3,:], yslice[i+3,:], bins=(50,50), cmap=plt.cm.jet)
        axs2[i].scatter(xislice[i+3,:], yslice[i+3,:], c='C0', zorder=1)
        #axs2[i].set_ylim(-2,2)
    #for ax in axs2.flat:
        #ax.set(xlabel = '$\\xi$ ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')
        #ax.label_outer()
        axs2[2].set(xlabel = '$\\xi$ ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')

    fig7, axs3 = plt.subplots(3, sharey=True)
    fig7.suptitle("Progression of " + shape_name + " EProbe")

    for i in range(0, 3):
        axs3[i].set_title("Snapshot at X = " + str(x_s[i]) + " mm")
        axs3[i].scatter(zslice[i,:], yslice[i,:], zorder=2)
        axs3[i].set_ylim(-2,2)
    for ax in axs3.flat:
        ax.set(xlabel = 'Z ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')
    for ax in axs3.flat:
        ax.label_outer()

    fig8, axs4 = plt.subplots(3, sharey=True)
    fig8.suptitle("Progression of " + shape_name + " EProbe")

    for i in range(0, 3):
        axs4[i].set_title("Snapshot at X = " + str(x_s[i+3]) + " mm")
        axs4[i].scatter(zslice[i+3,:], yslice[i+3,:])
        axs4[i].set_ylim(-2,2)
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
