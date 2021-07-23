# Script for showing full evolution of probe at hardcoded snapshot locations in and out of plasma
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

plt.rcParams.update({'font.size': 12 })
#plt.rcParams['animation.ffmpeg_path'] = '/ffmpeg/bin'
mpl.use('Agg')


# Choose boundaries of screens in mm
xstart_mm = 0
xend_mm = 550
xstep_mm = 1


# Definition of Constants
M_E = 9.109e-31                      # Electron rest mass in kg
EC = 1.60217662e-19                  # Electron charge in C
EP_0 = 8.854187817e-12               # Vacuum permittivity in C/(V m)
C = 299892458                        # Speed of light in vacuum in m/s

# Color Scheme
WB = False # Sequential
Viridis = True # Sequential + Perceptually Uniform
BuPu = False # Sequential
Jet = False

def returnXi(z):
    return z - C * 54.3948 # Hardcoded time for Run 144!!!

def returnZ(xi):
    return xi + C * 54.3948

def Gamma(p):
    return math.sqrt(1.0 + p**2)

def Velocity(px,ptot):
# Returns relativistic velocity from momentum
    return px / Gamma(ptot)

def getBallisticTraj(x_0,y_0,xi_0,z_0,px,py,pz,x_s):
# Use ballistic matrix to find positions on screens
    dx = x_s - x_0
    y_f = y_0 + dx * (py/px)
    z_f = z_0 + dx * (pz/px)

# Find time traveled to get proper xi
    p = math.sqrt(px**2 + py**2 + pz**2)
    vx = Velocity(px, p)
    vy = Velocity(py, p)
    vz = Velocity(pz, p)
    vtot = math.sqrt(vx**2 + vy**2 + vz**2)
    dtot = math.sqrt((x_s - x_0)**2 + (y_f - y_0)**2 + (z_f - z_0)**2)
    t = dtot/vtot

    xi_f = xi_0 + dx * (pz/px) + t

    return y_f, xi_f, z_f

def plot(x_f,y_f,xi_f,z_f,px_f,py_f,pz_f, w, sim_name,shape_name,noObj,iter):
# Plot evolution of probe after leaving plasma
    print("Propagating particle trajectories")
    start_time_prop = time.time()
    t = time.localtime()
    curr_time = time.strftime("%H:%M:%S", t)
    print("Start Time: ", curr_time)

    if (sim_name.upper() == 'OSIRIS_CYLINSYMM'):
        import include.simulations.useOsiCylin as sim
    elif (sim_name.upper() == 'QUASI3D'):
        import include.simulations.useQuasi3D as sim
    else:
        print("Simulation name unrecognized. Quitting...")
        exit()

    W_P = sim.getPlasFreq()
    plasma_bnds = sim.getBoundCond()
    shape_name = shape_name.capitalize()

# Normalize screen distances
    screen_dists = list(range(xstart_mm,xend_mm+1,xstep_mm))
    slices = len(screen_dists) # Number of Screens
    xs_norm = []
    for i in range(0,slices):
        xs_norm.append(screen_dists[i] * W_P * 10**(-3) / C)

# Generate arrays of coordinates at origin + each screen
    yslice = np.empty([slices, noObj])
    xislice = np.empty([slices, noObj])
    zslice = np.empty([slices, noObj])

# Project positions at distances in x_s
    for i in progressbar.progressbar(range(0,slices), redirect_stout=True):
        # If x_s out of plasma, use ballistic trajectory
        if (abs(xs_norm[i]) > plasma_bnds[2]):
            for j in range(0,noObj):
                yslice[i, j], xislice[i, j], zslice[i, j] = getBallisticTraj(x_f[j], y_f[j], xi_f[j], z_f[j], px_f[j], py_f[j], pz_f[j], xs_norm[i])
        else:
            for j in range(0,noObj):
                yslice[i, j] = y_f[j]
                xislice[i, j] = xi_f[j]
                zslice[i, j] = z_f[j]

# Plot slices
# For bin size = 0.006 (lambda/10)
# Run 130 Limits: (27,52), (-6,6), Bins: (4167,2000)
#         (35,40), (-1,1), Bins: (833,333)
# For bin size = 0.03
# Run 130 Limits: (27,52), (-6,6), Bins: (833,400)
# Run 232 Limits: (435,475), (0,6), Bins: (1333,200)

    binsizez = 6000#6000#833#2833#4167#1000#2666#1333
    binsizey = 1000#400#2000#160#666#200

    xmin = 35 #25#27#400
    xmax = 52 #500

    ymin = -5.5
    ymax = 5.5
    
    cmin = 1
    vmin_ = cmin
    vmax_ = 1000

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

    tpropf = time.localtime()
    curr_time_prop_f = time.strftime("%H:%M:%S", tpropf)
    print("Propagation End Time: ", curr_time_prop_f)
    print("Duration of propagation: ", (time.time() - start_time_prop)/60, " min \n")


    ##############################
    # Creating plot
    start_time_plot = time.time()
    print("Making frames...")

    path = os.getcwd()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    new_path = os.path.join(path,f'animation-{timestr}')
    os.mkdir(new_path)

    fig, ax = plt.subplots(1, figsize=(8, 5), dpi=600)
    fig.suptitle("Progression of EProbe")
    
    plt.tight_layout(rect=[0, 0, 1, 0.9])

    for i in progressbar.progressbar(range(0,slices), redirect_stout=True):
        h = ax.hist2d(zslice[i,:], yslice[i,:], weights=w, bins=(binsizez,binsizey), cmap=cmap, vmin=vmin_,vmax=vmax_,cmin=cmin)#, norm=norm)
        temptext = ax.text(xmin+0.3,ymax*0.8,f"x = {screen_dists[i]:03}mm", fontdict=None, horizontalalignment='left', fontsize=10, color="Black")
        
        ax.set_ylim(ymin,ymax)
        ax.set_xlim(xmin,xmax)
        if (WB):
                ax.set_facecolor('white')
        #elif (Viridis):
        #    ax.set_facecolor('#30013b')
        else:
            ax.set_facecolor('white')

        ax.set(xlabel = 'Z ($c/\omega_p$)', ylabel = 'Y ($c/\omega_p$)')

        #cbar5.set_label('Electron Density')
        secax = ax.secondary_xaxis('top', functions= (returnXi, returnZ))
        secax.set(xlabel= '$\\xi$ ($c/\omega_p$)')
        
        cbar = plt.colorbar(h[3], ax=ax, orientation='horizontal')#, pad=0.3)

        #Saving
        filename = str(os.path.join(new_path,f'progression-x-{screen_dists[i]:03}mm.png'))
        fig.savefig(filename,dpi=600,transparent=False)
        plt.cla()
        temptext.remove()
        cbar.remove()
    ################################

    ################################
    # WRITE MOVIE
    fps = 12 # frames per second
    movieWriter.generatemovie(fps,new_path)
    ################################

    # Report timing statistics
    tplotf = time.localtime()
    curr_time_plot_f = time.strftime("%H:%M:%S", tplotf)
    print("Plotting Frames End Time: ", curr_time_plot_f)
    print("Duration of plotting frames: ", (time.time() - start_time_plot)/60, " min \n")
