# Here is where the initial conditions of the electron probe are defined
# This filename is the input parameter of the eProbe.py file
#
# This input file is for testing the field data for a0 = 4 sim (sim ID 000067)


simulation_name = 'QUASI3D'
shape = 'rprism_weighted_after'
iterations = 100000
mode = 0
fname = "000033_testing.npz"
debugmode = False

# Probe centered at the following initial coordinates (in c/w_p):
x_c = -8 # Start within boundary of sim, outside bubble, on correct side
y_c = 2 # Off-center to avoid center of bubble?
xi_c = -10

# Initial momentum
px_0 = 100 # Make sure it goes towards the screen!
py_0 = 0
pz_0 = 0

# Screen Parameters (Assume infinite in y and z)
x_s = [10, 50, 100, 250, 500]

# Shape Parameters (Radius or Side Length)
s1 = 2 # In y
s2 = 5 # In xi

# Densities
ydensity = 200
xidensity = 300
xdensity = 1 # Probe width - 1 single layer
resolution = None