#Script for generating plots of electron trajectories

import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from mpl_toolkits import mplot3d

def plot(x,y,z,t,xi,sim_name):

    fig = plt.figure(1)
    ax = plt.axes(projection='3d')
    ax.set_xlabel("x ($c/\omega_p$)")
    ax.set_ylabel("$\\xi$ ($c/\omega_p$)")
    ax.set_zlabel("y ($c/\omega_p$)")
    ax.set_title("Electron Probe Trajectory in $\\xi$")
    ax.set_zlim(-0.005,0.005)
    ax.plot3D(x, xi, y, 'k', label = sim_name) # Want vertical axis as y
    ax.legend()

    fig2 = plt.figure(2)
    ax2 = plt.axes(projection='3d')
    ax2.set_xlabel("x ($c/\omega_p$)")
    ax2.set_ylabel("z ($c/\omega_p$)")
    ax2.set_zlabel("y ($c/\omega_p$)")
    ax2.set_title("Electron Probe Trajectory in z")
    ax2.set_zlim(-0.005,0.005)
    ax2.plot3D(x, z, y, 'k',label = sim_name) # Want vertical axis as y
    ax2.legend()

    fn = "/Users/Marisa/Documents/Research/plots/eProbe.png"

    fig.show()
    fig2.show()
    input()
