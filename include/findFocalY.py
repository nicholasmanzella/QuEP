import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import pdb
import statistics as stat
import math

# Initialize a vertical line of electrons through the blowout regime to find the Y focal length
# Spherical aberrations will cause variance in focal length

def calculate(x_0,y_0,xi_0,z_0,x_f,y_f,xi_f,z_f,px_f,py_f,pz_f,sim_name,shape_name,x_s,s1,s2):

    dy, f_y = [],[]

# With thin lens approximation, dy = y0 - 0
    for i in range(0, len(x_0)-1):
        dy.append(y_0[i])

# Find focal length for each data point by multiplying dy by the angle of the electron leaving the regime
    for i in range(0, len(x_0)-1):
        f_y.append( -dy[i] * px_f[i] / py_f[i])

# Find average focal length and variance
    focal_y = stat.mean(f_y)
    std_y = math.sqrt(stat.variance(f_y))

    print("Focal Y = " + str(focal_y) + " " + u"\u00B1 " + str(std_y))

    input()
