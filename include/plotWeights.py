# Script for generating 2D plots of electron trajectories
import os
import numpy as np
import matplotlib.colors as col
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import pdb
import math
import copy
import time
import progressbar
import include.movieWriter as movieWriter
import multiprocessing as mp
import include.simulations.useQuasi3D as sim
mpl.use('Agg')
plt.rcParams.update({'font.size': 12 })


# Definition of Constants
M_E = 9.109e-31                      # Electron rest mass in kg
EC = 1.60217662e-19                  # Electron charge in C
EP_0 = 8.854187817e-12               # Vacuum permittivity in C/(V m)
C = 299892458                        # Speed of light in vacuum in m/s

WB = False # Sequential
Viridis = True # Sequential + Perceptually Uniform
BuPu = False # Sequential
Jet = False

t0 = sim.getTime()

propspeed = sim.getPropagationSpeed()

def returnXi(z):
    return z - t0*propspeed

def returnZ(xi):
    return xi + t0*propspeed




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
    ax5.text(-23,0.2,f"Sum $w_\\xi$ * $\Delta \\xi$ = {summ:.3f}", fontdict=None, horizontalalignment='center', fontsize=10)

    plt.tight_layout()

    fig5.savefig('weights_xi-xi-direction.png',dpi=600,transparent=False)




def plotweightsxiy(y_f,xi_f, w, rand):
    
    path = os.getcwd()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    new_path = os.path.join(path,f'animation-{timestr}-{rand}')
    os.mkdir(new_path)

    ximin = -40 #36  #25#27#400
    ximax = -10 #50  #500
    
    ymin = -1
    ymax = 1

    bin_resolution = .1 #0.02 #c/w_p
    bin_edges_xi = np.arange(ximin, ximax, 100)
    bin_edges_y = np.arange(ymin, ymax, 100)
    
    cmin = 1       # Minimum density displayed
    vmin_ = cmin    # Minimum color value
    vmax_ = 100    # Maximum color value

    if (WB):
        cmap = plt.cm.binary
    elif (Viridis):
        cmap = plt.cm.viridis
    elif (BuPu):
        cmap = plt.cm.BuPu
    elif (Jet):
        cmap = copy.copy(plt.get_cmap('jet'))
        cmap.set_under(color='white')
    else:
        cmap = plt.cm.gist_gray
    norm = mpl.colors.Normalize(vmin=1, vmax=400)
    
    # Create figure
    fig, ax = plt.subplots(1, figsize=(8, 5), dpi=600)
    fig.suptitle("Xi-Y Weighting Map")
    plt.tight_layout(rect=[0, 0, 1, 0.9])
    
    h = ax.hist2d(xi_f[:], y_f[:], weights=w[:], bins=(bin_edges_xi,bin_edges_y), cmap=cmap, vmin=vmin_,vmax=vmax_,cmin=cmin)#, norm=norm)

    ax.set_ylim(ymin,ymax)
    ax.set_xlim(ximin,ximax)

    if (WB):
        ax.set_facecolor('white')
    #elif (Viridis):
    #    ax.set_facecolor('#30013b')
    else:
        ax.set_facecolor('white')

    ax.set(xlabel = '$\\xi$ ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')

    secax = ax.secondary_xaxis('top', functions= (returnZ, returnXi))
    secax.set(xlabel= 'Z ($c/\omega_p$)')
    
    cbar = plt.colorbar(h[3], ax=ax, orientation='horizontal')#, pad=0.3)
    #cbar.set_label('Electron Density')

    #Saving
    filename = str(os.path.join(new_path,f'weighting-xi-y.png'))
    fig.savefig(filename,dpi=600,transparent=False)
        
    ax.cla()
    fig.clf()
    plt.close(fig)