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
    ax1.set_ylabel("X ($c/\omega_p$)")
    ax1.set_xlabel("Z ($c/\omega_p$)")
    ax1.tick_params(axis='y', labelcolor='k')
    ax1.set_title(shape_name + " Electron Probe Trajectory")

    for i in range(0, noElec):
        ax1.plot(z_dat[i,:], x_dat[i,:], 'r', label='$X-Z Trajectory') # Want vertical axis as y

    fig1.tight_layout()
    fig1.show()
    input()
