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

def plot(x,y,xi,z,sim_name,shape_name,x_s,s1,s2):

    shape_name = shape_name.capitalize()
    fig = plt.figure(1)
    ax = plt.axes()
    ax.set(xlabel='$\\xi$ ($c/\omega_p$)', ylabel='y ($c/\omega_p$)')
    ax.set_title(shape_name + " eProbe Projection onto Screen at x = " + str(x_s) + " $c/\omega_p$")

    #if (shape_name.upper() == 'RIBBON'):
    ax.scatter(xi, y, label="Radius = " + str(s1) + "$c/\omega_p$")

    ax.legend(loc = 'upper right')


    fig2 = plt.figure(2)
    ax2 = plt.axes()
    ax2.set(xlabel='z ($c/\omega_p$)', ylabel='y ($c/\omega_p$)')
    ax2.set_title(shape_name + " eProbe Projection onto Screen at x = " + str(x_s) + " $c/\omega_p$")
    #if (shape_name.upper() == 'RIBBON'):
    ax2.scatter(z, y, label="Radius = " + str(s1) + "$c/\omega_p$")
    ax2.legend(loc = 'upper right')

    fig.show()
    fig2.show()
    input()

    #slope, intercept = np.polyfit(x, z, 1)
    #print(slope)

    #plt.savefig("fields.png",transparent=True)
