# Here is where the initial conditions of the electron probe are defined
# This filename is the input parameter of the eProbe.py file

simulation_name = 'QUASI3D'
shape = 'single'
density = 1
iterations = 15000
mode = 0

# Probe centered at the following initial coordinates (in c/w_p):
x_c = -2.4 # Start within region of field
y_c = -0.5
xi_c = -9

# An electron placed here will have x_f = 2.81, y_f = -0.497
#   px_f = 100, py_f = 0.0896. For y_f = 0, dx = 94 mm.
#   For y_f = 0.5 (full lensing), dx = 188 m. Double check
#   with ballistic trajectory code for confirmation.

# Initial momentum
px_0 = 100 # Make sure it goes towards the screen!
py_0 = 0
pz_0 = 0

# Screen Distances (from z-axis of plasma cell, in mm):
#x_s = [100, 200, 300, 400, 500] # Only 5
x_s = [10, 20, 100, 250, 500]

# Shape Parameters (Radius or Side Length, in c/w_p):
s1 = 0.5 # In y
s2 = 10 # In xi
s3 = 1 # In x
