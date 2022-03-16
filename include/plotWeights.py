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

def plotxv(w, x_0, y_0, xi_0, z_0, w_virt,xv,yv,beamx_c,beamy_c,sigma_x,sigma_y):
# 2D: w_x vs. x
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)

    middle_x = len(w_virt[:,0,0]) // 2 - 1
    middle_y = len(w_virt[0,:,0]) // 2 - 1
    middle_xi = len(w_virt[0,0,:]) // 2 - 1
    
    mu_x = beamx_c
    sigma_x = sigma_x
    mu_y = beamy_c
    sigma_y = sigma_y
    x = np.linspace(mu_x - 3*sigma_x, mu_x + 3*sigma_x, 100)
    y = np.linspace(mu_y - 3*sigma_y, mu_y + 3*sigma_y, 100)
    #multivariate_normalpdf = np.exp((-1/2)*(((x-mu_x)/sigma_x)**2+((y-mu_y)/sigma_y)**2))
    #ax2.plot(y, multivariate_normalpdf, label="mulitvariate normal distribution")

    
    normalpdf = (1/(np.sqrt(2*np.pi)*sigma_y)) * (1/(np.sqrt(2*np.pi)*sigma_x)) * (np.exp((-1/2)*((x-mu_x)/sigma_x)**2)) * (np.exp((-1/2)*((yv[middle_x,middle_y,middle_xi]-mu_y)/sigma_y)**2))
    ax1.plot(x, normalpdf, label="normal distribution")

    normalpdf_func = lambda x: (1/(np.sqrt(2*np.pi)*sigma_y)) * (1/(np.sqrt(2*np.pi)*sigma_x)) * (np.exp((-1/2)*((x-mu_x)/sigma_x)**2)) * (np.exp((-1/2)*((yv[middle_x,middle_y,middle_xi]-mu_y)/sigma_y)**2))
    area = integrate.quad(normalpdf_func,mu_x - 3*sigma_x, mu_x + 3*sigma_x)[0]

    ax1.text(beamx_c,0.5,f"Area under curve = {'%.3f' % area}", fontdict=None, horizontalalignment='center', fontsize=10)
    
    ax1.plot(xv[:,middle_y,middle_xi],w_virt[:,middle_y,middle_xi],"o", label="weighting_function",alpha=0.7)
    
    ax1.legend()
    ax1.set_xlabel("x_0 ($c/\omega_p$)")
    ax1.set_ylabel("w_virt")
    ax1.set_title("Weighting viewing x-direction")

    plt.tight_layout()

    fig1.savefig('weights_x-direction.png',dpi=600,transparent=False)

def plotx(w, x_0, y_0, xi_0, z_0, s2, w_virt,xv,yv,beamx_c,beamy_c,sigma_x,sigma_y):
# Plot w (w_x) vs xi
    ##########################################################################################
    fig3 = plt.figure()
    ax3 = fig3.add_subplot(111)
     
    ax3.plot(xi_0,w,"o", label="weighting_function",alpha=0.7)
    
    #ax3.legend(loc='upper right')
    ax3.set_xlabel("xi_f ($c/\omega_p$)")
    ax3.set_ylabel("w_x")
    ax3.set_title("Weighting viewing xi-direction")

    Deltax = 2*s2
    summ = 0
    for w_x in w:
        summ += w_x*Deltax
    ax3.text(-23,0.2,f"Sum $w_x$ * $\Delta x$ = {summ:.3f}", fontdict=None, horizontalalignment='center', fontsize=10)

    plt.tight_layout()

    fig3.savefig('weights_x-xi-direction.png',dpi=600,transparent=False)

def ploty(w, x_0, y_0, xi_0, z_0, s1, w_virt,xv,yv,beamx_c,beamy_c,sigma_x,sigma_y):
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

def plotyv(w_virt,xv,yv,beamx_c,beamy_c,sigma_x,sigma_y):
# 2D: w_y vs. y
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    
    middle_x = len(w_virt[:,0,0]) // 2 - 1
    middle_y = len(w_virt[0,:,0]) // 2 - 1
    middle_xi = len(w_virt[0,0,:]) // 2 - 1

    mu_x = beamx_c
    sigma_x = sigma_x
    mu_y = beamy_c
    sigma_y = sigma_y
    x = np.linspace(mu_x - 3*sigma_x, mu_x + 3*sigma_x, 100)
    y = np.linspace(mu_y - 3*sigma_y, mu_y + 3*sigma_y, 100)
    #multivariate_normalpdf = np.exp((-1/2)*(((x-mu_x)/sigma_x)**2+((y-mu_y)/sigma_y)**2))
    #ax2.plot(y, multivariate_normalpdf, label="mulitvariate normal distribution")

    
    normalpdf = (1/(np.sqrt(2*np.pi)*sigma_y)) * (1/(np.sqrt(2*np.pi)*sigma_x)) * (np.exp((-1/2)*((x-mu_x)/sigma_x)**2)) * (np.exp((-1/2)*((yv[middle_x,middle_y,middle_xi]-mu_y)/sigma_y)**2))
    ax2.plot(y, normalpdf, label="normal distribution")

    normalpdf_func = lambda y: (1/(np.sqrt(2*np.pi)*sigma_y)) * (1/(np.sqrt(2*np.pi)*sigma_x)) * (np.exp((-1/2)*((xv[middle_x,middle_y,middle_xi]-mu_x)/sigma_x)**2)) * (np.exp((-1/2)*((y-mu_y)/sigma_y)**2))
    area = integrate.quad(normalpdf_func,mu_y - 3*sigma_y, mu_y + 3*sigma_y)[0]

    ax2.text(0.0,0.5,f"Area under curve = {'%.3f' % area}", fontdict=None, horizontalalignment='center', fontsize=10)
     
    ax2.plot(yv[middle_x,:,middle_xi],w_virt[middle_x,:,middle_xi],"o", label="weighting_function", alpha=0.3)
    
    ax2.legend()
    ax2.set_xlabel("y_0 ($c/\omega_p$)")
    ax2.set_ylabel("w_virt")
    ax2.set_title("Weighting viewing y-direction")

    plt.tight_layout()

    fig2.savefig('weights_y-direction.png',dpi=600,transparent=False)

