import sys
import math
import numpy as np
import pdb

# Initializes a single electron probe

def initProbe(x_c,y_c,xi_c,t0,s1,s2,density):
    z_c = xi_c + t0
    return x_c, y_c, xi_c, z_c
