import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import pdb
import statistics as stat
import math

def calculate(x_0,y_0,xi_0,z_0,x_f,y_f,xi_f,z_f,px_f,py_f,pz_f,sim_name,shape_name,x_s,s1,s2):

    dz, dy, dxi, f_z, f_y, f_xi = [],[],[],[],[],[]

# Find amount of deflection in z and y
    for i in range(len(x_0)):
        dz.append(z_f[i] - z_0[i])
        dy.append(y_f[i] - y_0[i])
        dxi.append(xi_f[i] - xi_0[i])

# Find focal length for each data point
    for i in range(len(x_0)):
        f_z.append( - dz[i] * pz_f[i] / px_f[i])
        f_y.append( - dy[i] * py_f[i] / px_f[i])
        f_xi.append( - dxi[i] * pz_f[i] / px_f[i])

# Find average focal length and variance
    focal_z = stat.mean(f_z)
    focal_y = stat.mean(f_y)
    focal_xi = stat.mean(f_xi)
    std_z = math.sqrt(stat.variance(f_z))
    std_y = math.sqrt(stat.variance(f_y))
    std_xi = math.sqrt(stat.variance(f_xi))

    print("Focal Z = " + str(focal_z) + " " + u"\u00B1 " + str(std_z))
    print("Focal Y = " + str(focal_y) + " " + u"\u00B1 " + str(std_y))
    print("Focal Xi = " + str(focal_xi) + " " + u"\u00B1 " + str(std_xi))

    input()
