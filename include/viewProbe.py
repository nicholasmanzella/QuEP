import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import pdb
import math

def plot(x_dat,y_dat,z_dat,xi_dat,sim_name,shape_name,s1,s2,noElec):

    fig9 = plt.figure()
    ax9 = plt.axes()
    ax9.set_xlabel("$\\xi$ ($c/\omega_p$)")
    ax9.set_ylabel("Y ($c/\omega_p$)")
    ax9.set_title("Initial Electron Probe Shape")

    for i in range(0,len(xi_dat)):
        ax9.scatter(xi_dat[i,0], y_dat[i,0], c='C1')

    fig9.show()
    input()
