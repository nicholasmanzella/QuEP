import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import pdb
import time

def getFieldArrays(sim_name):
    if (sim_name.upper() == 'OSIRIS_CYLINSYMM'):
        import include.useOsiCylin as sim
    elif (sim_name.upper() == 'QUASI3D'):
        import include.useQuasi3D as sim
    t0 = sim.getTime()

    zaxis_1, z2, raxis_1, r2 = sim.axes()
    ziter = len(zaxis_1)
    riter = len(raxis_1)

    xiaxis = zaxis_1 - t0

    Ex = np.empty((riter,ziter),dtype=float)
    Ey = np.empty((riter,ziter),dtype=float)
    Ez = np.empty((riter,ziter),dtype=float)
    Bx = np.empty((riter,ziter),dtype=float)
    By = np.empty((riter,ziter),dtype=float)
    Bz = np.empty((riter,ziter),dtype=float)

    for ir in range(riter):
        print(ir)
        for iz in range(ziter):
            #pdb.set_trace()
            Ex[ir, iz] = sim.EField(2, raxis_1[ir], 0, zaxis_1[iz], raxis_1[ir])
            #Ey[ir, iz] = sim.EField(3, 0, raxis_1[ir], zaxis_1[iz], raxis_1[ir])
            #Ez[ir, iz] = sim.EField(1, raxis_1[ir], 0, zaxis_1[iz], raxis_1[ir])
            #Bx[ir, iz] = sim.BField(2, raxis_1[ir], 0, zaxis_1[iz], raxis_1[ir])
            #By[ir, iz] = sim.BField(3, 0, raxis_1[ir], zaxis_1[iz], raxis_1[ir])
            #Bz[ir, iz] = sim.BField(1, raxis_1[ir], 0, zaxis_1[iz], raxis_1[ir])

    return zaxis_1, xiaxis, raxis_1, Ex, Ey, Ez, Bx, By, Bz

def plot(x,y,z,t,xi,sim_name):

    start_time = time.time()

    zaxis, xiaxis, raxis, Ex, Ey, Ez, Bx, By, Bz = getFieldArrays(sim_name)

    fig = plt.figure()
    ax = plt.axes()
    ax.set(xlabel='$\\xi$ ($c/\omega_p$)', ylabel = 'x ($c/\omega_p$)')
    #fig, axs = plt.subplots(2, 3)
    # fig, axs = plt.subplots(1,3)
    # fig.suptitle("Projected Trajectory in X with Quasi 3D Field Maps ($\Delta y \approx 0$ )")


    # axs[0, 0].plot(xi, x, 'k')
    # axs[0, 0].set_title('Ex')
    # axs[0, 1].plot(xi, x, 'k')
    # axs[0, 1].set_title('Ey')
    # axs[0, 2].plot(xi, x, 'k')
    # axs[0, 2].set_title('Ez')
    # axs[1, 0].plot(xi, x, 'k')
    # axs[1, 0].set_title('Bx')
    # axs[1, 1].plot(xi, x, 'k')
    # axs[1, 1].set_title('By')
    # axs[1, 2].plot(xi, x, 'k')
    # axs[1, 2].set_title('Bz')

    # for ax in axs.flat:
    #     ax.set(xlabel = '$\\xi$ ($c/\omega_p$)', ylabel = 'x ($c/\omega_p$)')
    #
    # for ax in axs.flat:
    #     ax.label_outer()

    raxis = raxis * -1.0

    Ex = ax.pcolormesh(zaxis, raxis, Ex, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-Ex.max(),vmax=Ex.max()),cmap="RdBu_r")
    #Ex = axs[0, 0].pcolormesh(zaxis, raxis, Ex, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-Ex.max(),vmax=Ex.max()),cmap="RdBu_r")
    # Ey = axs[0, 1].pcolormesh(zaxis, raxis, Ey, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-Ey.max(),vmax=Ey.max()),cmap="RdBu_r")
    # Ez = axs[0, 2].pcolormesh(zaxis, raxis, Ez, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-Ez.max(),vmax=Ez.max()),cmap="RdBu_r")
    # Bx = axs[1, 0].pcolormesh(zaxis, raxis, Bx, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-Bx.max(),vmax=Bx.max()),cmap="RdBu_r")
    # By = axs[1, 1].pcolormesh(zaxis, raxis, By, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-By.max(),vmax=By.max()),cmap="RdBu_r")
    # Bz = axs[1, 2].pcolormesh(zaxis, raxis, Bz, norm=col.SymLogNorm(linthresh=0.03,linscale=0.03,vmin=-Bz.max(),vmax=Bz.max()),cmap="RdBu_r")

    cbar = fig.colorbar(Ex, ax=ax)
    #fig.subplots_adjust(right=0.8)
    #cbar_ax = fig.add_axes([0.85, 0.15, 0.05, 0.7])
    #fig.colorbar(Ex, cax=cbar_ax)

    cbar.set_label('Electric Field ($m_e c\omega_p / e$)')

    print((time.time() - start_time)/60, " min")
    #ax.legend()
    #slope, intercept = np.polyfit(x, z, 1)
    #print(slope)
    plt.savefig("fields.png",transparent=True)
    #fig.show()

    # fig2 = plt.figure(2)
    # ax2 = plt.axes()
    #
    # ax2.set_ylabel("y ($c/\omega_p$)")
    # ax2.set_xlabel("$\\xi$ ($c/\omega_p$)")
    # ax2.set_title("Project Trajectory in Y")
    # plt.ylim(-0.005,0.005)
    #
    # ax2.plot(xi, y, 'r', label = sim_name)
    # ax2.legend()
    # fig2.show()
