#Script for generating plots of electron trajectories

import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import pdb

def plot(x,y,xi,z,sim_name,shape_name,x_s):

    shape_name = shape_name.capitalize()
    fig = plt.figure(1)
    ax = plt.axes(projection='3d')
    ax.set_xlabel("x ($c/\omega_p$)")
    ax.set_ylabel("$\\xi$ ($c/\omega_p$)")
    ax.set_zlabel("y ($c/\omega_p$)")
    ax.set_title(shape_name + " Electron Probe Trajectory in $\\xi$")
    ax.set_xlim(x_s - 0.005, x_s + 0.005)
    ax.scatter(x, xi, y, 'k', label=sim_name) # Want vertical axis as y
    ax.legend(bbox_to_anchor=(0.97, 0.97), bbox_transform=plt.gcf().transFigure)

    fig2 = plt.figure(2)
    ax2 = plt.axes(projection='3d')
    ax2.set_xlabel("x ($c/\omega_p$)")
    ax2.set_ylabel("z ($c/\omega_p$)")
    ax2.set_zlabel("y ($c/\omega_p$)")
    ax2.set_title(shape_name + " Electron Probe Trajectory in $\\xi$")
    ax2.set_xlim(x_s - 0.005, x_s + 0.005)
    ax2.scatter(x, z, y, 'k',label=sim_name) # Want vertical axis as y
    ax2.legend(bbox_to_anchor=(0.97, 0.97), bbox_transform=plt.gcf().transFigure)

    fn = "/Users/Marisa/Documents/Research/plots/eProbe.png"

    fig.show()
    fig2.show()
    input()
