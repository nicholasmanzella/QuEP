# Here is where the initial conditions of the electron probe are defined
# This filename is the input parameter of the eProbe.py file

simulation_name = 'QUASI3D'
shape = 'ribbon'
density = 5000
iterations = 10000

# Probe centered at the following initial coordinates:
x_c = 0
y_c = 0
xi_c = -10

# Initial momentum
px_0 = -100 # Make sure it goes towards the screen!
py_0 = 0
pz_0 = 0

# Screen Parameters (Assume infinite in y and z)
x_s = -40

# Shape Parameters (Radius or Side Length)
s1 = 0.15
s2 = 0.15
