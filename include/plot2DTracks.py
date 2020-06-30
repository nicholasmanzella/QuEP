# Script for generating 2D plots of electron trajectories

import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import pdb

def plot(x_dat,y_dat,z_dat,xi_dat,sim_name,shape_name,s1,s2,noElec):

    shape_name.capitalize()
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
