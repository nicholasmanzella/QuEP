import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D
import pdb

def plot(x_dat,y_dat,z_dat,xi_dat,Fx_dat,Fy_dat,Fz_dat,sim_name,shape_name,s1,s2,noElec):

# 3D: X, Xi, Y
    shape_name = shape_name.capitalize()
    fig = plt.figure(1)
    ax = plt.axes(projection='3d')
    ax.set_xlabel("x ($c/\omega_p$)")
    ax.set_ylabel("$\\xi$ ($c/\omega_p$)")
    ax.set_zlabel("y ($c/\omega_p$)")
    ax.set_title(shape_name + " Electron Probe Trajectories in $\\xi$")
    for i in range(0, noElec):
        ax.plot(x_dat[i,:], xi_dat[i,:], y_dat[i,:], 'k') # Want vertical axis as ya

    #ax.legend(bbox_to_anchor=(0.97, 0.97), bbox_transform=plt.gcf().transFigure)

# 3D: X, Z, Y
    fig2 = plt.figure(2)
    ax2 = plt.axes(projection='3d')
    ax2.set_xlabel("x ($c/\omega_p$)")
    ax2.set_ylabel("z ($c/\omega_p$)")
    ax2.set_zlabel("y ($c/\omega_p$)")
    ax2.set_title(shape_name + " Electron Probe Trajectory in $\\xi$")
    for i in range(0, noElec):
        ax2.plot(x_dat[i,:], z_dat[i,:], y_dat[i,:], 'k') # Want vertical axis as y
    #ax2.legend(bbox_to_anchor=(0.97, 0.97), bbox_transform=plt.gcf().transFigure)

    fn = "/Users/Marisa/Documents/Research/plots/eProbe.png"

# 2D: Xi-X with linear fit, constrained to plasma bubble
    fig3 = plt.figure(3)
    ax3 = plt.axes()
    ax3.set_xlabel("x ($c/\omega_p$)")
    ax3.set_ylabel("xi ($c/\omega_p$)")
    ax3.set_xlim(-3,3)
    ax3.tick_params(axis='y', labelcolor='k')
    ax3.set_title("Xi-X Trajectory within Plasma Bubble")

    # ax3_f = ax3.twinx()
    # ax3_f.set_ylabel("Fz ($m_e c \omega_p$)")
    # ax3_f.tick_params(axis='y', labelcolor='b')

    for i in range(0, noElec):
        ax3.plot(x_dat[i,:], xi_dat[i,:], 'k') # Want vertical axis as y
        #ax3_f.plot(x_dat[i,:], Fz_dat[i,:], 'b')
        #m, b = np.polyfit(x_dat[i,:], xi_dat[i,:], 1)
        #print("Func = ", m, "*x + ", b)

# 2D: Y-X with linear fit
    fig4 = plt.figure(4)
    ax4 = plt.axes()
    ax4.set_xlabel("X ($c/\omega_p$)")
    ax4.set_ylabel("Y ($c/\omega_p$)")
    ax4.tick_params(axis='y', labelcolor='k')
    ax4.set_title("Electron Trajectory through Blowout Regime")

    ax4_f = ax4.twinx()
    ax4_f.set_ylabel("$F_y$ ($m_e c \omega_p$)")
    ax4_f.yaxis.label.set_color('C0')
    ax4_f.tick_params(axis='y', labelcolor='C0', colors='C0')

    for i in range(0, noElec):
        ax4.plot(x_dat[i,:], y_dat[i,:], 'k', label='Y-X Trajectory') # Want vertical axis as y
        ax4_f.plot(x_dat[i,:], Fy_dat[i,:], 'C0', label='Transverse Force')

    fig4.legend(bbox_to_anchor=(0.88, 0.94), bbox_transform=plt.gcf().transFigure)
    #fig.show()
    #fig2.show()
    fig3.tight_layout()
    fig3.show()
    fig4.tight_layout()
    fig4.show()
    input()
