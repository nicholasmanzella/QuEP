import sys
import math
import numpy as np
import pdb

# Constants
PI = math.pi

def initProbe(x_c,y_c,xi_c,t0,r1,r2,density):
    x_0, y_0, xi_0, z_0 = [],[],[],[]
    step = (2 * PI) / density
    theta = 0

    while (theta <= 2*PI):
        x_0.append(x_c)
        xi_0.append(xi_c + r1*math.cos(theta))
        y_0.append(y_c + r1*math.sin(theta))
        z_0.append(xi_c + r1*math.cos(theta) + t0)
        theta += step

    return x_0, y_0, xi_0, z_0
