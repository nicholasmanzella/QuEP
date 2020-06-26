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

def plot(x_0,y_0,xi_0,z_0,x_f,y_f,xi_f,z_f,sim_name,shape_name,x_s,s1,s2):

    fin_colors = cm.rainbow(np.linspace(0, 1, len(x_0)))
    init_colors = cm.rainbow(np.linspace(0,1, len(x_0)))
    shape_name = shape_name.capitalize()

    fig = plt.figure(1)
    ax = plt.axes()
    ax.set(xlabel= '$\\xi$ ($c/\omega_p$)', ylabel= 'y ($c/\omega_p$)')
    ax.set_title(shape_name + " eProbe")
    ax.scatter(xi_f, y_f, color= fin_colors, label= "Final Probe on Screen at x = " + str(x_s) + " $c/\omega_p$")
    ax.plot(xi_0, y_0, 'k')
    ax.scatter(xi_0, y_0, color= init_colors, label= "Initial Probe Shape", zorder= 2 )
    ax.plot(xi_0, y_0, 'k', zorder= 1)
    #ax.legend(loc= 'upper right')

    fig2 = plt.figure(2)
    ax2 = plt.axes()
    ax2.set(xlabel='z ($c/\omega_p$)', ylabel='y ($c/\omega_p$)')
    ax2.set_title(shape_name + " eProbe")
    ax2.scatter(z_f, y_f, color= fin_colors, label= "Final Probe on Screen at x = " + str(x_s) + " $c/\omega_p$")
    ax2.scatter(z_0, y_0, color= init_colors, label= "Initial Probe Shape", zorder= 2)
    ax2.plot(z_0, y_0, 'k', zorder= 1)
    #ax2.legend(loc= 'upper right')

    fig.show()
    fig2.show()
    input()

    #slope, intercept = np.polyfit(x, z, 1)
    #print(slope)

    #plt.savefig("fields.png",transparent=True)
