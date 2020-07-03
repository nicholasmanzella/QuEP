# Here is where the initial conditions of the electron probe are defined
# This filename is the input parameter of the eProbe.py file

simulation_name = 'QUASI3D'
shape = 'rectangle'
density = 30
fill = False
iterations = 50000

# Probe centered at the following initial coordinates:
x_c = -2.4 # Start within region of field
y_c = 0
xi_c = -15

# Initial momentum
px_0 = 100 # Make sure it goes towards the screen!
py_0 = 0
pz_0 = 1000

# Screen Parameters (Assume infinite in y and z)
x_s = 40

# Shape Parameters (Radius or Side Length)
s1 = 0.5 # In y
s2 = 5 # In xi
