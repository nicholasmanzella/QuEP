#Script for generating plots of electron trajectories

import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import include.plotSimTracks as plotSimTracks
from mpl_toolkits import mplot3d

#def plot(r, z, t, xi, E, r_sim, xi_sim, SHM, track):
def plot(x,y,z,t,xi):
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    ax.set_xlabel("x ($c/\omega_p$)")
    ax.set_ylabel("$\\xi$ ($c/\omega_p$)")
    #ax.set_ylabel("z ($c/\omega_p$)")
    ax.set_zlabel("y ($c/\omega_p$)")
    ax.set_title("Electron Probe Trajectory")

    ax.plot3D(x, xi, y, 'k',label = "Quasi3D") # Want vertical axis as y

    #ax.legend()

    fn = "/Users/Marisa/Documents/Research/PWFA-eTracks/plots/eProbe.png"
    #plt.savefig(fn,dpi=200,transparent=True)
    plt.show()
