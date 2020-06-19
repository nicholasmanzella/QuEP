import numpy as np
import math
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from mpl_toolkits import mplot3d

# Definition of Constants
M_E = 9.109e-31                      #electron rest mass in kg
EC = 1.60217662e-19                  #electron charge in C
EP_0 = 8.854187817e-12               #vacuum permittivity in C/(V m) (not e-12?)
C = 299892458                        #speed of light in vacuum in m/s
N = 1e15                             #electron number density in 1/m^3
W_P = math.sqrt(N*EC**2/(M_E*EP_0))  #plasma frequency in 1/s

def plot(x,y,z,t,xi,gam):

    avgGam = sum(gam)/len(gam)
    kbeta = W_P/(C * math.sqrt(2 * avgGam))
    print("Average Gamma over one oscillation = ", avgGam)
    print("Betatron Wave No = ", kbeta)
    wavel = (2 * math.pi / kbeta) # Normalized
    print("Lambda = ", wavel)

    fig = plt.figure()
    ax = plt.axes()

    ax.set_ylabel("$\\gamma$")
    ax.set_xlabel("t (1/w_p)")
    #plt.ylim(0.995,1.005)

    ax.set_title("Gamma Over One Oscillation")

    ax.plot(t, gam, label = 'Gamma') # Want vertical axis as y

    plt.show()

    input()
