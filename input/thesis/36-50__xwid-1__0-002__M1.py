# Here is where the initial conditions of the electron probe are defined
# This filename is the input parameter of the eProbe.py file

simulation_name = 'QUASI3D'
shape = 'rectangle'
# dt = 0.005, 150000
iterations = 500000
mode = 1
fname = "36-50__xwid-1__0-002__M1.npz"
debugmode = False

# Probe centered at the following initial coordinates (in c/w_p):
x_c = -2.4 # Start within region of field # 2.4 = maximum x_c
y_c = 0
xi_c = -9

# Initial momentum
px_0 = 110 # Make sure it goes towards the screen!
py_0 = 0
pz_0 = 0

# Screen Distances (from z-axis of plasma cell, in mm):
x_s = [10, 50, 100, 250, 500]

# Shape Parameters (Radius or Side Length, in c/w_p):
s1 = 1 # In y
s2 = 6 # In xi

# Densities
ydensity = 1000
xidensity = 6000
xdensity = 1 # Probe width - single layer
resolution = 0.002

