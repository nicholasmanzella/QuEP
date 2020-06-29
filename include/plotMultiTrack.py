import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import pdb

def plot(x_dat,y_dat,z_dat,xi_dat,sim_name,shape_name,s1,s2,noElec):

    shape_name = shape_name.capitalize()
    fig = plt.figure(1)
    ax = plt.axes(projection='3d')
    ax.set_xlabel("x ($c/\omega_p$)")
    ax.set_ylabel("$\\xi$ ($c/\omega_p$)")
    ax.set_zlabel("y ($c/\omega_p$)")
    ax.set_title(shape_name + " Electron Probe Trajectories in $\\xi$")
    for i in range(0, noElec-1):
        ax.plot(x_dat[i,:], xi_dat[i,:], y_dat[i,:], 'k') # Want vertical axis as y

    #ax.legend(bbox_to_anchor=(0.97, 0.97), bbox_transform=plt.gcf().transFigure)

    fig2 = plt.figure(2)
    ax2 = plt.axes(projection='3d')
    ax2.set_xlabel("x ($c/\omega_p$)")
    ax2.set_ylabel("z ($c/\omega_p$)")
    ax2.set_zlabel("y ($c/\omega_p$)")
    ax2.set_title(shape_name + " Electron Probe Trajectory in $\\xi$")
    for i in range(0, noElec-1):
        ax2.plot(x_dat[i,:], z_dat[i,:], y_dat[i,:], 'k') # Want vertical axis as y
    #ax2.legend(bbox_to_anchor=(0.97, 0.97), bbox_transform=plt.gcf().transFigure)

    fn = "/Users/Marisa/Documents/Research/plots/eProbe.png"

    fig3 = plt.figure(3)
    ax3 = plt.axes()
    ax3.set_xlabel("x ($c/\omega_p$)")
    ax3.set_ylabel("z ($c/\omega_p$)")
    for i in range(0, noElec-1):
        ax3.plot(x_dat[i,:], y_dat[i,:], 'k') # Want vertical axis as y

    fig.show()
    fig2.show()
    fig3.show()
    input()
