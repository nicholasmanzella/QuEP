# Initial conditions for sending vertical line of electrons through blowout regime of Quasi3D simulation
# useQuasi3D.py has all BField = 0 and only Mode 0 for EFields

simulation_name = 'QUASI3D'
shape = 'vline'
density = 20
iterations = 15000

# Probe centered at the following initial coordinates:
x_c = -2.4 # Start within region of field
y_c = 0
xi_c = -5.9#-8.2 # (Front Bubble) #-18.3 (Back Bubble)

# Initial momentum
px_0 = 110 # Make sure it goes towards the screen!
py_0 = 0
pz_0 = 0

# Screen Parameters (Assume infinite in y and z)
x_s = 500

# Shape Parameters (Radius or Side Length)
s1 = 0.25 # In y
s2 = 0.01 # In xi
