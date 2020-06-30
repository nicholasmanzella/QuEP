# Script for generating 2D plots of electron trajectories with option for plotting force

import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import pdb

plotYForce = False # Plot transverse force with trajectories, not useful for many trajectories
plotZForce = False # Plot force along WF propagation

def plot(x_dat,y_dat,z_dat,xi_dat,Fx_dat,Fy_dat,Fz_dat,sim_name,shape_name,s1,s2,noElec):

# 2D: Xi-X, constrained to blowout regime
    fig1 = plt.figure(1)
    ax1 = plt.axes()
    ax1.set_xlabel("X ($c/\omega_p$)")
    ax1.set_ylabel("$\\xi$ ($c/\omega_p$)")
    ax1.set_xlim(-3,3)
    ax1.tick_params(axis='y', labelcolor='k')
    ax1.set_title("Electron Trajectories through Blowout Regime")

    for i in range(0, noElec):
        ax1.plot(x_dat[i,:], xi_dat[i,:], 'k', label='$\\xi$-X Trajectory') # Want vertical axis as y

    if (plotZForce):
        ax1_f = ax1.twinx()
        ax1_f.set_ylabel("$F_z$ ($m_e c \omega_p$)")
        ax1_f.yaxis.label.set_color('C0')
        ax1_f.tick_params(axis='y', labelcolor='C0', colors='C0')

        for i in range(0, noElec):
            ax1_f.plot(x_dat[i,:], Fz_dat[i,:], 'C0', label='Z Force')

        fig1.legend(bbox_to_anchor=(0.88, 0.94), bbox_transform=plt.gcf().transFigure)

# 2D: Y-X
    fig2 = plt.figure(2)
    ax2 = plt.axes()
    ax2.set_xlabel("X ($c/\omega_p$)")
    ax2.set_ylabel("Y ($c/\omega_p$)")
    ax2.tick_params(axis='y', labelcolor='k')
    ax2.set_title("Electron Trajectories through Blowout Regime")

    for i in range(0, noElec):
        ax2.plot(x_dat[i,:], y_dat[i,:], 'k', label='Y-X Trajectory') # Want vertical axis as y

    if (plotYForce):
        ax2_f = ax2.twinx()
        ax2_f.set_ylabel("$F_y$ ($m_e c \omega_p$)")
        ax2_f.yaxis.label.set_color('C0')
        ax2_f.tick_params(axis='y', labelcolor='C0', colors='C0')

        for i in range(0, noElec):
            ax2_f.plot(x_dat[i,:], Fy_dat[i,:], 'C0', label='Transverse Force')

        fig2.legend(bbox_to_anchor=(0.88, 0.94), bbox_transform=plt.gcf().transFigure)

    fig1.tight_layout()
    fig1.show()
    fig2.tight_layout()
    fig2.show()
    input()
