# Here is where the initial conditions of the electron probe are defined
# This filename is the input parameter of the eProbe.py file

simulation_name = 'QUASI3D'
shape = 'rectangle'
density = 500
iterations = 15000
mode = -1

# Probe centered at the following initial coordinates (in c/w_p):
x_c = -2.4 # Start within region of field
y_c = 0
xi_c = -10

# Initial momentum
px_0 = 110 # Make sure it goes towards the screen!
py_0 = 0
pz_0 = 0

# Screen Distances (from z-axis of plasma cell, in mm):
x_s = [300, 400, 500, 600, 700]

# Shape Parameters (Radius or Side Length, in c/w_p):
s1 = 2.65 # In y
s2 = 13.6 # In xi
s3 = 0
