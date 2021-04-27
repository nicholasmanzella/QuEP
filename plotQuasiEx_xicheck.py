import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import pdb
import time
import include.simulations.useQuasi3D as sim
import math
import scipy
from scipy.optimize import curve_fit
plt.rcParams.update({'font.size': 16})

xicheck = -5#-5.9#-11.2#-8.2#-18.0

def getFieldArrays():

    xiaxis_1, xi2, raxis_1, r2 = sim.axes()
    xiiter = len(xiaxis_1)
    riter = len(raxis_1)

    Ex = np.empty(riter,dtype=float)

    for ir in range(riter):
        #pdb.set_trace()
        Ex[ir] = sim.EField(2, raxis_1[ir], 0, xicheck, raxis_1[ir])

    return xiaxis_1, raxis_1, Ex

def find_nearest_index(array,value):
    idx = np.searchsorted(array, value, side="right")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1
    else:
        return idx

def linear(x, m, b):
    return m*x + b

def main():

    start_time = time.time()

    xiaxis, raxis, Ex = getFieldArrays()
    xiDex = find_nearest_index(xiaxis, xicheck)

    fig = plt.figure()
    ax = plt.axes()
    ax.set(xlabel = '$R$ ($c/\omega_p$)', ylabel = '$E_r$ ($m_e c \omega_p / e$)')
    ax.set_title("Radial Electric Field as a Function of R, M0 Only")
    ax.plot(raxis, Ex, c='C0')

# Fit linear portion
    x_start = 0.05
    x_end = 0.15
    xDex_start = find_nearest_index(raxis, x_start)
    xDex_end = find_nearest_index(raxis, x_end)

    #m, b = np.polyfit(raxis[xDex_start:xDex_end], Ex[xDex_start:xDex_end], 1)
    opt_params, parm_cov = scipy.optimize.curve_fit(linear, raxis[xDex_start:xDex_end], Ex[xDex_start:xDex_end])
    m = opt_params[0]
    b = opt_params[1]
    merr = np.sqrt(parm_cov[0,0])
    print("EField = ", m, "*x + ", b)
    print("Merr = ", merr)

    x = np.linspace(0,0.8,100)
    y = m*x + b

    ax.plot(x,y,c='C3',linestyle='dashed')

    print((time.time() - start_time)/60, " min")

    #plt.savefig("fields.png",transparent=True)
    #plt.show()

    input()

main()
