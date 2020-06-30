# Script for generating 2D plots of electron trajectories

import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import pdb

def plot(x_dat,y_dat,z_dat,xi_dat,sim_name,shape_name,s1,s2,noElec):
