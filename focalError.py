import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pdb
import math
plt.rcParams.update({'font.size': 20})

y0_rb = [0.076923077,0.153846154,0.230769231,0.307692308,0.384615385,0.461538462,0.538461538,0.615384615,0.692307692,0.769230769,0.846153846,0.923076923]
depthF = [0.002971775,0.012048627,0.02774024,0.050987708,0.083333333,0.12724296,0.186732208,0.268670095,0.385804656,0.56501609,0.876388375,1.6]
focPW = [169.267,171.245,173.911,177.371,182.26,188.409,196.742,207.809,223.099,244.788,278.061,339.208]
focEqn1 = [178.632,180.249,183.044,187.185,192.946,200.768,211.364,225.959,246.824,278.746,334.21,463.103]
perErr = [0.052426217,0.04995312,0.049895107,0.052429415,0.055383372,0.061558615,0.069179236,0.080324307,0.096121123,0.12182417,0.168005146,0.267532277]

perErr = [0 for e in perErr] #[e * 100 for e in perErr]
depthF = [p * 100 for p in depthF]

fig, ax = plt.subplots()

ax.errorbar(y0_rb, focEqn1, yerr=depthF, fmt='-o', label='$f = p_xv_x/2x_pk$ (Theory)')
ax.errorbar(y0_rb, focPW, yerr=perErr, fmt='-o', label='$f = (p_x/p_y)y_0$ (QuEP)')

ax.set_xlabel('$y_0/r_b$')
ax.set_ylabel('Focal Length ($c/\omega_p$)')
ax.set_title('Comparison of Focal Length Measurements and Calculations')
fig.legend(bbox_to_anchor=(0.3, 0.8), bbox_transform=plt.gcf().transFigure)

plt.show()

input()
