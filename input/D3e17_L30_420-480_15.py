# Here is where the initial conditions of the electron probe are defined
# This filename is the input parameter of the eProbe.py file

simulation_name = 'QUASI3D'
shape = 'rectangle'
# dt = 0.005, 150000
iterations = 500000
mode = 1
fname = "D3e17_L30_420-480_3.npz"

# Probe centered at the following initial coordinates (in c/w_p):
x_c = -5 # Start within region of field
y_c = 0
xi_c = -119 # (t0 = 569)

# Initial momentum
px_0 = 110 # Make sure it goes towards the screen!
py_0 = 0
pz_0 = 0

# Screen Distances (from z-axis of plasma cell, in mm):
#x_s = [100, 200, 300, 400, 500] # Only 5
x_s = [10, 50, 100, 250, 500]

# Shape Parameters (Radius or Side Length, in c/w_p):
s1 = 3 # In y
s2 = 30 # In xi
s3 = 1 # In x

# Densities
ydensity = 181
xidensity = 1818
resolution = 0.033
