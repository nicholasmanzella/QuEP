import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker

def plot(x,y,z,t,xi,sim_name):

    fig = plt.figure(1)
    ax = plt.axes()

    ax.set_ylabel("x ($c/\omega_p$)")
    ax.set_xlabel("$\\xi$ ($c/\omega_p$)")
    ax.set_title("Project Trajectory in X")

    ax.plot(xi, x, label = sim_name)
    ax.legend()
    slope, intercept = np.polyfit(x, xi, 1)
    print(slope)
    fig.show()

    fig2 = plt.figure(2)
    ax2 = plt.axes()

    ax2.set_ylabel("y ($c/\omega_p$)")
    ax2.set_xlabel("$\\xi$ ($c/\omega_p$)")
    ax2.set_title("Project Trajectory in Y")
    plt.ylim(-0.005,0.005)

    ax2.plot(xi, y, 'r', label = sim_name)
    ax2.legend()
    fig2.show()

    input()
