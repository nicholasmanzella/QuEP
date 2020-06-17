import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from mpl_toolkits import mplot3d

def plot(x,y,z,t,xi,gam):
    fig = plt.figure()
    ax = plt.axes()

    ax.set_ylabel("$\\gamma$")
    ax.set_xlabel("t (1/w_p)")
    #plt.ylim(0.995,1.005)

    ax.set_title("Gamma Over One Oscillation")

    ax.plot(t, gam, label = 'Gamma') # Want vertical axis as y

    plt.show()

    input()
