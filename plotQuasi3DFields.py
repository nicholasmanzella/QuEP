import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import pdb
import time
import include.useQuasi3D as sim

def getFieldArrays():

    xiaxis_1, xi2, raxis_1, r2 = sim.axes()
    xiiter = len(xiaxis_1)
    riter = len(raxis_1)

    Ex = np.empty((riter,xiiter),dtype=float)
    Ey = np.empty((riter,xiiter),dtype=float)
    Ez = np.empty((riter,xiiter),dtype=float)
    Bx = np.empty((riter,xiiter),dtype=float)
    By = np.empty((riter,xiiter),dtype=float)
    Bz = np.empty((riter,xiiter),dtype=float)

    for ir in range(riter):
        print(ir)
        for ixi in range(xiiter):
            #pdb.set_trace()
            Ex[ir, ixi] = sim.EField(2, raxis_1[ir], 0, xiaxis_1[ixi], raxis_1[ir])
            Ey[ir, ixi] = sim.EField(3, 0, raxis_1[ir], xiaxis_1[ixi], raxis_1[ir])
            Ez[ir, ixi] = sim.EField(1, raxis_1[ir], 0, xiaxis_1[ixi], raxis_1[ir])
            Bx[ir, ixi] = sim.BField(2, raxis_1[ir], 0, xiaxis_1[ixi], raxis_1[ir])
            By[ir, ixi] = sim.BField(3, 0, raxis_1[ir], xiaxis_1[ixi], raxis_1[ir])
            Bz[ir, ixi] = sim.BField(1, raxis_1[ir], 0, xiaxis_1[ixi], raxis_1[ir])

    return xiaxis_1, raxis_1, Ex, Ey, Ez, Bx, By, Bz

def main():

    start_time = time.time()

    xiaxis, raxis, Ex, Ey, Ez, Bx, By, Bz = getFieldArrays()

    fig, axs = plt.subplots(2, 3)
    plt.subplots_adjust(left=0.05, bottom=0.1, right=0.8, top=0.9)
    fig.suptitle("Quasi3D Fields for $\\phi = 0$")

    axs[0, 0].set_title('Ex')
    axs[0, 1].set_title('Ey')
    axs[0, 2].set_title('Ez')
    axs[1, 0].set_title('Bx')
    axs[1, 1].set_title('By')
    axs[1, 2].set_title('Bz')

    for ax in axs.flat:
        ax.set(xlabel = '$\\xi$ ($c/\omega_p$)', ylabel = 'x ($c/\omega_p$)')

    for ax in axs.flat:
        ax.label_outer()

    Ex = axs[0, 0].pcolormesh(xiaxis, raxis, Ex, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-100,vmax=100),cmap="RdBu_r")
    Ey = axs[0, 1].pcolormesh(xiaxis, raxis, Ey, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-100,vmax=100),cmap="RdBu_r")
    Ez = axs[0, 2].pcolormesh(xiaxis, raxis, Ez, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-100,vmax=100),cmap="RdBu_r")
    Bx = axs[1, 0].pcolormesh(xiaxis, raxis, Bx, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-100,vmax=100),cmap="RdBu_r")
    By = axs[1, 1].pcolormesh(xiaxis, raxis, By, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-100,vmax=100),cmap="RdBu_r")
    Bz = axs[1, 2].pcolormesh(xiaxis, raxis, Bz, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-100,vmax=100),cmap="RdBu_r")

    cbar_ax = fig.add_axes([0.83, 0.05, 0.03, 0.9])
    cbar = fig.colorbar(Ex, cax=cbar_ax)

    cbar.set_label('Electric or Magnetic Field ($m_e c \omega_p / e$ or $m_e \omega_p / e$)')

    print((time.time() - start_time)/60, " min")

    #plt.savefig("fields.png",transparent=True)
    plt.show()
    input()

main()
