# Here is where the initial conditions of the electron probe are defined
# This filename is the input parameter of the eProbe.py file

simulation_name = 'QUASI3D'
shape = 'disc'
density = 7
fill = False
iterations = 15000

# Probe centered at the following initial coordinates (in c/w_p):
x_c = -2.4 # Start within region of field
y_c = 0
xi_c = -10

# Initial momentum
px_0 = 100 # Make sure it goes towards the screen!
py_0 = 0
pz_0 = 1000

# Screen Distances (from z-axis of plasma cell, in mm):
x_s = [20, 40, 60, 80, 100] # Only 5

# Shape Parameters (Radius or Side Length, in c/w_p):
s1 = 0.5 # In y
s2 = 5 # In xi
