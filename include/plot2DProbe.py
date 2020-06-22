import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import pdb

# For Unit Testing:
#import include.plotOsiExample as plotOsiExample
#track='med'

def plot(x,y,xi,z,sim_name,shape_name):

    shape_name = shape_name.capitalize()
    fig = plt.figure(1)
    ax = plt.axes()
    ax.set(xlabel='$\\xi$ ($c/\omega_p$)', ylabel='x ($c/\omega_p$)')
    ax.set_title("Projected " + shape_name + " Electron Probe in X-$\\xi$")
    ax.scatter(xi, x, label=sim_name)
    #xi_OSIRIS, r_OSIRIS = plotOsiExample.get_xir(track)
    #ax.plot(xi_OSIRIS, r_OSIRIS, 'r--', label="Unit Test")
    ax.legend(loc = 'upper right')


    fig2 = plt.figure(2)
    ax2 = plt.axes()
    ax2.set(xlabel='z ($c/\omega_p$)', ylabel='x ($c/\omega_p$)')
    ax2.set_title("Projected " + shape_name + " Electron Probe in X-Z")
    ax2.scatter(z, x, label=sim_name)
    ax2.legend(loc = 'upper right')

    fig.show()
    fig2.show()
    input()

    #slope, intercept = np.polyfit(x, z, 1)
    #print(slope)

    #plt.savefig("fields.png",transparent=True)
