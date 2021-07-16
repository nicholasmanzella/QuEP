# Script for generating 2D plots of electron trajectories

import math
import scipy.stats as stats
import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import pdb
mpl.use('Agg')

def plotx(w_x,x_0,xi_0,beamx_c,sigma_x):
# 2D: w_x vs. x
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    
    mu = beamx_c
    sigma = sigma_x
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    ax1.plot(x, math.sqrt(2*math.pi)*sigma_x*stats.norm.pdf(x, mu, sigma), label="normal distribution")

    ax1.plot(xi_0,w_x,"o", label="weighting_function")
    
    ax1.legend()
    ax1.set_xlabel("xi_0 ($c/\omega_p$)")
    ax1.set_ylabel("w_x")
    ax1.set_title("Weighting in x-direction on xi")

    fig1.savefig('weights_x-direction.png',dpi=600,transparent=False)

def plotxlayer(layerx,weight,beamx_c,sigma_x):
    fig3 = plt.figure()
    ax3 = fig3.add_subplot(111)
    
    mu = beamx_c
    sigma = sigma_x
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    ax3.plot(x, math.sqrt(2*math.pi)*sigma_x*stats.norm.pdf(x, mu, sigma), label="normal distribution")

    ax3.plot(layerx,weight,"o", label="weighting_function")
    
    ax3.legend()
    ax3.set_xlabel("layer x position ($c/\omega_p$)")
    ax3.set_ylabel("weight")
    ax3.set_title("Weighting in x-direction of each x layer")

    fig3.savefig('weights_x-direction-layers.png',dpi=600,transparent=False)

def ploty(w_y,y_0,beamy_c,sigma_y):
# 2D: w_y vs. y
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    
    mu = beamy_c
    sigma = sigma_y
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    ax2.plot(x, math.sqrt(2*math.pi)*sigma_y*stats.norm.pdf(x, mu, sigma), label="normal distribution")

    ax2.plot(y_0,w_y,"o", label="weighting_function")
    
    ax2.legend()
    ax2.set_xlabel("y_0 ($c/\omega_p$)")
    ax2.set_ylabel("w_y")
    ax2.set_title("Weighting in y-direction")

    fig2.savefig('weights_y-direction.png',dpi=600,transparent=False)
