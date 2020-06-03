# This file retrieves the fields from OSIRIS data files stored within the data/ folder.

import h5py as h5
import numpy as np

def getField(fname):
  f = h5.File(fname,"r")
  datasetNames = [n for n in f.keys()] #Two Datasets: AXIS and e2
  field = datasetNames[-1]
  Field_dat = f[field][:].astype(float)
  return Field_dat

def axes():
  f = h5.File('data/EField_r.h5',"r")
  datasetNames = [n for n in f.keys()] #Two Datasets: AXIS and e2
  field = datasetNames[-1]
  Field_dat = f[field][:].astype(float)
  a1_bounds = f['AXIS']['AXIS1']
  a2_bounds = f['AXIS']['AXIS2']

  t0 = 858.95 #time at which field data was simulated, constant for all fields
  xi_dat = np.linspace(a1_bounds[0] - t0,a1_bounds[1] - t0,len(Field_dat[0]))
  r_dat = np.linspace(a2_bounds[0],a2_bounds[1],len(Field_dat))

  return r_dat, xi_dat, t0

def transE():
  return getField('data/EField_r.h5')

def longE():
  return getField('data/EField_z.h5')

def phiB():
  return getField('data/BField_phi.h5')

r_sim, xi_sim, t0 = axes()
Er_sim = transE()
Ez_sim = longE()
Bphi_sim = phiB()

def EField(x,y,z,axis):
# axis = 1 refers to x-axis field
# axis = 2 refers to y-axis field
# axis = 3 refers to z-axis field
# axis = 4 refers to r-axis field
    r = math.sqrt(x**2 + y**2)
    phi = GetPhi(x, y)
    zDex = find_nearest_index(xi_sim, z)
    rDex = find_nearest_index(r_sim, r)
    if axis == 1: # x axis
        return Er_sim[rDex, zDex] * math.cos(phi)
    elif axis == 2:
        return Er_sim[rDex, zDex] * math.sin(phi)
    elif axis == 3:
        return Ez_sim[rDex, zDex]
    elif axis == 4:
        return -1.0*Er_sim[rDex, zDex]

def BField(x,y,z,axis):
# axis = 1 refers to x-axis field
# axis = 2 refers to y-axis field
# axis = 3 refers to z-axis field
    r = math.sqrt(x**2 + y**2)
    phi = GetPhi(x, y)
    zDex = find_nearest_index(xi_sim, z)
    rDex = find_nearest_index(r_sim, r)
    if axis == 1:
        return -1.0 * Bphi_sim[rDex, zDex] * math.sin(phi)
    elif axis == 2:
        return Bphi_sim[rDex, zDex] * math.cos(phi)
    elif axis == 3:
        return 0
