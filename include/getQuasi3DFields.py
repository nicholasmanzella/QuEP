# This file retrieves the fields from OSIRIS Quasi3D data files stored within the data/ folder.
# Expresses EM fields in azimuthal harmonics up to the first order

import sys
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
  datasetNames = [n for n in f.keys()]
  field = datasetNames[-1]
  Field_dat = f[field][:].astype(float)
  return Field_dat

def axes():
  f = h5.File('data/OSIRIS/Quasi3D/b1_cyl_m-0-re-000130.h5',"r")
  datasetNames = [n for n in f.keys()] # Three Datasets: AXIS, SIMULATION, Field data
  field = datasetNames[-1]
  Field_dat = f[field][:].astype(float)
  a1_bounds = f['AXIS']['AXIS1']
  a2_bounds = f['AXIS']['AXIS2']

  t0 = f.attrs['TIME']
  xi_dat = np.linspace(a1_bounds[0] - t0,a1_bounds[1] - t0,len(Field_dat[0]))
  r_dat = np.linspace(a2_bounds[0],a2_bounds[1],len(Field_dat))

  return r_dat, xi_dat

def getTime():
    f = h5.File('data/OSIRIS/Quasi3D/b1_cyl_m-0-re-000130.h5',"r")
    t0 = f.attrs['TIME']
    return t0

# Return Electric field components

def getEx_M0():
    return getField('data/OSIRIS/Quasi3D/e2_cyl_m-0-re-000130.h5')

def getEy_M0():
    return getField('data/OSIRIS/Quasi3D/e3_cyl_m-0-re-000130.h5')

def getEz_M0():
    return getField('data/OSIRIS/Quasi3D/e1_cyl_m-0-re-000130.h5')

def getEx_M1_Re():
    return getField('data/OSIRIS/Quasi3D/e2_cyl_m-1-re-000130.h5')

def getEy_M1_Re():
    return getField('data/OSIRIS/Quasi3D/e3_cyl_m-1-re-000130.h5')

def getEz_M1_Re():
    return getField('data/OSIRIS/Quasi3D/e1_cyl_m-1-re-000130.h5')

def getEx_M1_Im():
    return getField('data/OSIRIS/Quasi3D/e2_cyl_m-1-im-000130.h5')

def getEy_M1_Im():
    return getField('data/OSIRIS/Quasi3D/e3_cyl_m-1-im-000130.h5')

def getEz_M1_Im():
    return getField('data/OSIRIS/Quasi3D/e1_cyl_m-1-im-000130.h5')

# Return Magnetic Field components

def getBx_M0():
    return getField('data/OSIRIS/Quasi3D/b2_cyl_m-0-re-000130.h5')

def getBy_M0():
    return getField('data/OSIRIS/Quasi3D/b3_cyl_m-0-re-000130.h5')

def getBz_M0():
    return getField('data/OSIRIS/Quasi3D/b1_cyl_m-0-re-000130.h5')

def getBx_M1_Re():
    return getField('data/OSIRIS/Quasi3D/b2_cyl_m-1-re-000130.h5')

def getBy_M1_Re():
    return getField('data/OSIRIS/Quasi3D/b3_cyl_m-1-re-000130.h5')

def getBz_M1_Re():
    return getField('data/OSIRIS/Quasi3D/b1_cyl_m-1-re-000130.h5')

def getBx_M1_Im():
    return getField('data/OSIRIS/Quasi3D/b2_cyl_m-1-im-000130.h5')

def getBy_M1_Im():
    return getField('data/OSIRIS/Quasi3D/b3_cyl_m-1-im-000130.h5')

def getBz_M1_Im():
    return getField('data/OSIRIS/Quasi3D/b1_cyl_m-1-im-000130.h5')

r_sim, xi_sim = axes() # Evenly spaced axes data (What are they written in terms of?)
Ex_M0 = getEx_M0()
Ey_M0 = getEy_M0()
Ez_M0 = getEz_M0()
Ex_M1_Re = getEx_M1_Re()
Ey_M1_Re = getEy_M1_Re()
Ez_M1_Re = getEz_M1_Re()
Ex_M1_Im = getEx_M1_Im()
Ey_M1_Im = getEy_M1_Im()
Ez_M1_Im = getEz_M1_Im()
Bx_M0 = getBx_M0()
By_M0 = getBy_M0()
Bz_M0 = getBz_M0()
Bx_M1_Re = getBx_M1_Re()
By_M1_Re = getBy_M1_Re()
Bz_M1_Re = getBz_M1_Re()
Bx_M1_Im = getBx_M1_Im()
By_M1_Im = getBy_M1_Im()
Bz_M1_Im = getBz_M1_Im()

def getPhi(x,y):
    return math.atan2(y,x) # From -pi to pi

def find_nearest_index(array,value):
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1
    else:
        return idx

def EField(axis,x,y,z,r=-1,vx=-1,vy=-1,vz=-1,vr=-1,vphi=-1):
# axis = 1 refers to x-axis field
# axis = 2 refers to y-axis field
# axis = 3 refers to z-axis field
    phi = getPhi(x,y)
    xDex = find_nearest_index(x_sim, x)
    yDex = find_nearest_index(y_sim, y)
    zDex = find_nearest_index(xi_sim, z)
    # Return expanded EFields
    if axis == 1:
        return Ex_M0[xDex, yDex, zDex] + Ex_M1_Re[xDex, yDex, zDex] * math.cos(phi) - Ex_M1_Im[xDex, yDex, zDex] * math.sin(phi)
    elif axis == 2:
        return Ey_M0[xDex, yDex, zDex] + Ey_M1_Re[xDex, yDex, zDex] * math.cos(phi) - Ey_M1_Im[xDex, yDex, zDex] * math.sin(phi)
    elif axis == 3:
        return Ez_M0[xDex, yDex, zDex] + Ez_M1_Re[xDex, yDex, zDex] * math.cos(phi) - Ez_M1_Im[xDex, yDex, zDex] * math.sin(phi)

def BField(axis,x,y,z,r=-1,vx=-1,vy=-1,vz=-1,vr=-1,vphi=-1):
# axis = 1 refers to x-axis field
# axis = 2 refers to y-axis field
# axis = 3 refers to z-axis field
    if len(sys.argv) == 10:
    # Return BForce
        phi = getPhi(x,y)
        xDex = find_nearest_index(x_sim, x)
        yDex = find_nearest_index(y_sim, y)
        zDex = find_nearest_index(xi_sim, z)
    # Calculate expanded BFields
        Bx = Bx_M0[xDex, yDex, zDex] + Bx_M1_Re[xDex, yDex, zDex] * math.cos(phi) - Bx_M1_Im[xDex, yDex, zDex] * math.sin(phi)
        By = By_M0[xDex, yDex, zDex] + By_M1_Re[xDex, yDex, zDex] * math.cos(phi) - By_M1_Im[xDex, yDex, zDex] * math.sin(phi)
        Bz = Bz_M0[xDex, yDex, zDex] + Bz_M1_Re[xDex, yDex, zDex] * math.cos(phi) - Bz_M1_Im[xDex, yDex, zDex] * math.sin(phi)
    # Cross-product velocities with BFields and return the BForce
        if axis == 1:
            return vy * Bz - vz * By
        elif axis == 2:
            return -1.0 * (vx * Bz - vz * Bx)
        elif axis == 3:
            return vx * By - vy * Bx

    elif len(sys.argv) == 4:
    # Return BField
        phi = getPhi(x,y)
        xDex = find_nearest_index(x_sim, x)
        yDex = find_nearest_index(y_sim, y)
        zDex = find_nearest_index(xi_sim, z)
    # Calculate expanded BFields
        if axis == 1:
            return Bx_M0[xDex, yDex, zDex] + Bx_M1_Re[xDex, yDex, zDex] * math.cos(phi) - Bx_M1_Im[xDex, yDex, zDex] * math.sin(phi)
        elif axis == 2:
            return By_M0[xDex, yDex, zDex] + By_M1_Re[xDex, yDex, zDex] * math.cos(phi) - By_M1_Im[xDex, yDex, zDex] * math.sin(phi)
        elif axis == 3:
            return Bz_M0[xDex, yDex, zDex] + Bz_M1_Re[xDex, yDex, zDex] * math.cos(phi) - Bz_M1_Im[xDex, yDex, zDex] * math.sin(phi)
