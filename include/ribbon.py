import sys
import math
import numpy as np
import pdb

# Constants
PI = math.pi

def initProbe(x_c,y_c,xi_c,r1,r2,density):
    x, y, xi = [],[],[]
    step = (2 * PI) / density
    theta = 0

    while (theta <= PI):
        x.append(x_c)
        xi.append(xi_c + r*math.cos(theta))
        y.append(y_c + r*math.sin(theta))
        theta += step

    return x, y, xi
