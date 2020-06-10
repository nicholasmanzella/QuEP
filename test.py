import h5py as h5
import numpy as np

f = h5.File('data/OSIRIS/Quasi3D/b1_cyl_m-0-re-000130.h5',"r")#('data/OSIRIS/Quasi3D/b1_cyl_m-0-re-000130.h5',"r")
datasetNames = [n for n in f.keys()] # Three Datasets: AXIS, SIMULATION, Field data
field = datasetNames[-1]
Field_dat = f[field][:].astype(float)
a1_bounds = f['AXIS']['AXIS1']
a2_bounds = f['AXIS']['AXIS2']

dr = -1.0 * a2_bounds[0]

t0 = f.attrs['TIME']
t0 = t0[0]
xi_dat = np.linspace(a1_bounds[0] - t0,a1_bounds[1] - t0, len(Field_dat[0]))
r_dat = np.linspace(a2_bounds[0] + dr,a2_bounds[1] + dr, len(Field_dat)) # Account for radius between (-dr,r_max - dr)

def find_nearest_index(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1
    else:
        return idx

z0 = 0

zDex = find_nearest_index(xi_dat,z0)
