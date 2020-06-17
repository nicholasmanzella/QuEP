import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import pdb

def plot(x,y,z,t,xi,sim_name):

    fig = plt.figure(1)
    ax = plt.axes()
    ax.set(xlabel='$\\xi$ ($c/\omega_p$)', ylabel='x ($c/\omega_p$)')
    ax.set_title("Projected X-$\\xi$ Trajectory")
    ax.plot(xi, x, label=sim_name)
    ax.legend()


    fig2 = plt.figure(2)
    ax2 = plt.axes()
    ax2.set(xlabel='z ($c/\omega_p$)', ylabel='x ($c/\omega_p$)')
    ax2.set_title("Projected X-Z Trajectory")
    ax2.plot(z, x, 'r', label = sim_name)
    ax2.legend()

    fig.show()
    fig2.show()
    input()

    #slope, intercept = np.polyfit(x, z, 1)
    #print(slope)

    #plt.savefig("fields.png",transparent=True)
