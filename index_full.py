# Include file imports
import sys
import importlib
import numpy as np
import include.plot2DTracks as plot2D
import include.plot3DTracks as plot3D
import include.showQuickEvolution as showEvol_Q
import include.showFullEvolution as showEvol_F
import include.viewProbe as viewProbe

# Plotting Scripts
plot2DTracks = False                 # View 2D projections of trajectories
# plot3DTracks = False                 # View 3D model of trajectories
# viewProbeShape = False               # View initial shape of probe separately
showQuickEvolution = False           # View evolution of probe after leaving plasma at inputted x_s in scatter plots
showFullEvolution = True           # View full evolution of probe at hardcoded locations in colored histograms
# Set all others equal False if want animation saved (dependency issue)
saveMovie = False                    # Save mp4 of probe evolution
if (saveMovie):
    import include.makeAnimation as makeAnimation

input_fname = str(sys.argv[1])
print("Using initial conditions from ", input_fname)
init = importlib.import_module(input_fname)
sim_name = init.simulation_name
shape_name = init.shape
yden = init.ydensity
xiden = init.xidensity
res = init.resolution
iter = init.iterations
mode = init.mode
fname = init.fname
x_c = init.x_c
y_c = init.y_c
xi_c = init.xi_c
px_0 = init.px_0
py_0 = init.py_0
pz_0 = init.pz_0
x_s = init.x_s
s1 = init.s1
s2 = init.s2
s3 = init.s3

if (mode == 0):
    data = np.load('./data/HighResProbe/L30_35-40_055_M0.npz')
    data2 = np.load('./data/HighResProbe/L30_40-45_055_M0.npz')
    data3 = np.load('./data/HighResProbe/L30_45-50_055_M0.npz')
elif (mode == 1):
    data = np.load('./data/HighResProbe/L30_35-40_055_M1.npz')
    data2 = np.load('./data/HighResProbe/L30_40-45_055_M1.npz')
    data3 = np.load('./data/HighResProbe/L30_45-50_055_M1.npz')
else:
    data = np.load('./data/HighResProbe/L30_35-40_055.npz')
    data2 = np.load('./data/HighResProbe/L30_40-45_055.npz')
    data3 = np.load('./data/HighResProbe/L30_45-50_055.npz')

x_f_1 = data['x_dat']
y_f_1 = data['y_dat'] 
xi_f_1 = data['xi_dat']
z_f_1 = data['z_dat']
px_f_1 = data['px_dat']
py_f_1 = data['py_dat']
pz_f_1 = data['pz_dat']

x_f_2 = data2['x_dat']
y_f_2 = data2['y_dat']
xi_f_2 = data2['xi_dat']
z_f_2 = data2['z_dat']
px_f_2 = data2['px_dat']
py_f_2 = data2['py_dat']
pz_f_2 = data2['pz_dat']

x_f_3 = data3['x_dat']
y_f_3 = data3['y_dat']
xi_f_3 = data3['xi_dat']
z_f_3 = data3['z_dat']
px_f_3 = data3['px_dat']
py_f_3 = data3['py_dat']
pz_f_3 = data3['pz_dat']

x_f = np.concatenate((x_f_1,x_f_2,x_f_3))
y_f = np.concatenate((y_f_1,y_f_2,y_f_3))
z_f = np.concatenate((z_f_1,z_f_2,z_f_3))
xi_f = np.concatenate((xi_f_1,xi_f_2,xi_f_3))
px_f = np.concatenate((px_f_1,px_f_2,px_f_3))
py_f = np.concatenate((py_f_1,py_f_2,py_f_3))
pz_f = np.concatenate((pz_f_1,pz_f_2,pz_f_3))

noElec = len(x_f)

# Plot data points
if (plot2DTracks):
    plot2D.plot(x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, sim_name, shape_name, x_s, noElec)
# if (plot3DTracks):
    #     plot3D.plot(x_dat, y_dat, xi_dat, z_dat, x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, sim_name, shape_name, s1, s2, noElec)
if (showQuickEvolution):
    showEvol_Q.plot(x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, sim_name, shape_name, x_s, noElec, iter)
if (showFullEvolution):
    showEvol_F.plot(x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, sim_name, shape_name, noElec, iter)
# if (viewProbeShape):
#     viewProbe.plot(x_dat, y_dat, xi_dat, z_dat, sim_name, shape_name, s1, s2, noElec)
if (saveMovie):
    makeAnimation.animate(x_f, y_f, xi_f, z_f, px_f, py_f, pz_f, sim_name, shape_name, noElec, iter)
