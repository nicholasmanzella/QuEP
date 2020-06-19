# This file retrieves the fields from OSIRIS 2D data files stored within the data/ folder.

import h5py as h5
import numpy as np
import math

# Coordinate System
# z   - Direction of laser propagation (longitudinal)
# xi  - Position along z relative to wavefront (unnecessary?)
# r   - Cylindrical coordinate around z
# phi - Cylindrical coordinate around z, define phi = 0 along x
# x   - Direction of transverse probe
# y   - Direction perpendicular to transverse probe

def getField(fname):
  f = h5.File(fname,"r")
  datasetNames = [n for n in f.keys()] #Two Datasets: AXIS and e2
  field = datasetNames[-1]
  Field_dat = f[field][:].astype(float)
  return Field_dat

def axes():
  f = h5.File('data/OSIRIS/CylinSymm/EField_r.h5',"r")
  datasetNames = [n for n in f.keys()] #Two Datasets: AXIS and e2
  field = datasetNames[-1]
  Field_dat = f[field][:].astype(float)
  a1_bounds = f['AXIS']['AXIS1']
  a2_bounds = f['AXIS']['AXIS2']

  t0 = getTime() #time at which field data was simulated, constant for all fields
  xi_dat = np.linspace(a1_bounds[0] - t0,a1_bounds[1] - t0,len(Field_dat[0]))
  r_dat = np.linspace(a2_bounds[0],a2_bounds[1],len(Field_dat))

  return r_dat, xi_dat

def getTime():
