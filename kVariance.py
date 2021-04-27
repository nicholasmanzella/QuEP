import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pdb
import math
plt.rcParams.update({'font.size': 20})

C = 299892458

def returnXi(z):
    return z - 52#54.3948 # Hardcoded time for Run 144!!!

def returnZ(xi):
    return xi + 52#54.3948

xi = [-20,-19,-18,-17,-16,-15,-14,-13,-12,-11,-10,-9,-8,-7,-6,-5]
k = [0.17,0.29,0.335,0.277,-0.425,-0.356,0.272,0.456,0.483,0.498,0.462,0.484,0.465,0.418,0.22,0.037]
kerr = [0.004,0.011,0.01,0.02,0.022,0.034,0.05,0.00027,0.00012,0.00039,0.000777,0.000266,0.00126,0.00109,0.0012,0.00038]
ktheory = [0.5 for i in range(0,len(k))]

z = [i + 52 for i in xi]
fig, ax = plt.subplots()

ax.errorbar(z, k, yerr=kerr, fmt='-o', label='QuEP Measured $k$')
ax.plot(z, ktheory, 'r', label='$k$ Theory = 0.5')
ax.set_xlabel('$z$ ($c/\omega_p$)')
ax.set_ylabel('$k$ Value')
ax.set_title('Variation of $k$ with Longitudinal Position')
secax = ax.secondary_xaxis('top', functions= (returnXi, returnZ))
secax.set(xlabel= '$\\xi$ ($c/\omega_p$)')
fig.legend(bbox_to_anchor=(0.2, 0.75), bbox_transform=plt.gcf().transFigure)


plt.show()

input()
