# Script for generating 2D plots of electron trajectories

import math
import scipy.stats as stats
import scipy.integrate as integrate
import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import pdb
mpl.use('Agg')
plt.rcParams.update({'font.size': 12 })

def plotx(w, x_0, y_0, xi_0, z_0, s1, s2, beamx_c,beamy_c,beamxi_c,sigma_x,sigma_y,sigma_xi):
# Plot w (w_x) vs xi
    ##########################################################################################
    fig3 = plt.figure()
    ax3 = fig3.add_subplot(111)
     
    ax3.plot(xi_0,w,"o", label="weighting_function",alpha=0.7)
    
    #ax3.legend(loc='upper right')
    ax3.set_xlabel("xi_0 ($c/\omega_p$)")
    ax3.set_ylabel("w_x")
    ax3.set_title("Weighting viewing xi-direction")

    Deltax = 2*s2
    summ = 0
    for w_x in w:
        summ += w_x*Deltax
    ax3.text(-23,0.2,f"Sum $w_x$ * $\Delta x$ = {summ:.3f}", fontdict=None, horizontalalignment='center', fontsize=10)

    plt.tight_layout()

    fig3.savefig('weights_x-xi-direction.png',dpi=600,transparent=False)

def ploty(w, x_0, y_0, xi_0, z_0, s1, s2, beamx_c,beamy_c,beamxi_c,sigma_x,sigma_y,sigma_xi):
# Plot w (w_x) vs xi
    ##########################################################################################
    fig4 = plt.figure()
    ax4 = fig4.add_subplot(111)
     
    ax4.plot(y_0,w,"o", label="weighting_function",alpha=0.7)
    
    #ax3.legend(loc='upper right')
    ax4.set_xlabel("y_0 ($c/\omega_p$)")
    ax4.set_ylabel("w_y")
    ax4.set_title("Weighting viewing y-direction")

    Deltay = 2*s1/len(w)
    summ = 0
    for w_y in w:
        summ += w_y*Deltay
    ax4.text(0,0.2,f"Sum $w_y$ * $\Delta y$ = {summ:.3f}", fontdict=None, horizontalalignment='center', fontsize=10)

    plt.tight_layout()

    fig4.savefig('weights_y-sum-direction.png',dpi=600,transparent=False)


def plotxi(w, x_0, y_0, xi_0, z_0, s1, s2, beamx_c,beamy_c,beamxi_c,sigma_x,sigma_y,sigma_xi):
# Plot w (w_xi) vs xi
    ##########################################################################################
    fig5 = plt.figure()
    ax5 = fig5.add_subplot(111)
     
    ax5.plot(xi_0,w,"o", label="weighting_function",alpha=0.7)
    
    #ax5.legend(loc='upper right')
    ax5.set_xlabel("xi_0 ($c/\omega_p$)")
    ax5.set_ylabel("w_xi")
    ax5.set_title("Weighting viewing xi-direction")

    Deltaxi = 2*s2/len(w)
    summ = 0
    for w_xi in w:
        summ += w_xi*Deltaxi
    ax5.text(-23,0.2,f"Sum $w_\xi$ * $\Delta \xi$ = {summ:.3f}", fontdict=None, horizontalalignment='center', fontsize=10)

    plt.tight_layout()

    fig5.savefig('weights_xi-xi-direction.png',dpi=600,transparent=False)