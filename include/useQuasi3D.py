# This file retrieves the fields from OSIRIS Quasi3D data files stored within the data/ folder.
# Expresses EM fields in azimuthal harmonics up to the first order

import sys
import h5py as h5
import numpy as np
import math
import pdb

# Coordinate System
# z   - Direction of laser propagation (longitudinal)
# xi  - Position along z relative to wavefront (unnecessary?)
# r   - Cylindrical coordinate around z
# phi - Cylindrical coordinate around z, define phi = 0 along x
# x   - Direction of transverse probe
# y   - Direction perpendicular to transverse probe

def getField(fpath):
    f = h5.File(fpath,"r")
    datasetNames = [n for n in f.keys()]
    field = datasetNames[-1]
    Field_dat = f[field][:].astype(float)
    return Field_dat

def getTime():
    f = h5.File('data/OSIRIS/Quasi3D/b1_cyl_m-0-re-000130.h5',"r")
    t0 = f.attrs['TIME']
    t0 = t0[0]
    return t0

def axes():
# Retrieve axes boundaries under staggered mesh
    f = h5.File('data/OSIRIS/Quasi3D/b1_cyl_m-0-re-000130.h5',"r")#('data/OSIRIS/Quasi3D/b1_cyl_m-0-re-000130.h5',"r")
    datasetNames = [n for n in f.keys()] # Three Datasets: AXIS, SIMULATION, Field data
    field = datasetNames[-1]
    Field_dat = f[field][:].astype(float)
    a1_bounds = f['AXIS']['AXIS1'] # zmin and zmax
    a2_bounds = f['AXIS']['AXIS2'] # rmin and rmax - dr/2
    dz = 9.908e-4 # Width of each cell
    dr = 6.59e-3
# Account for specific definitions of bottom-left values for each field component
    z_bounds_1 = [a1_bounds[0], a1_bounds[1]] # Used for E1, B1
    z_bounds_2 = [a1_bounds[0] - dz/2, a1_bounds[1] + dz/2] # Used for E2, E3, B2, B3
    r_bounds_1 = [a2_bounds[0], a2_bounds[1] + dr/2] # Used for E2, B2
    r_bounds_2 = [a2_bounds[0] - dr/2, a2_bounds[1] + dr] # Used for E1, E3, B1, B3
    t0 = getTime()#f.attrs['TIME']

# Field Shape is (433, 25231), where data is written as E(z,r)
    zaxis_1 = np.linspace(z_bounds_1[0] - t0, z_bounds_1[1] - t0, len(Field_dat[0])) # len = 25231
    zaxis_2 = np.linspace(z_bounds_2[0] - t0, z_bounds_2[1] - t0, len(Field_dat[0]))
    raxis_1 = np.linspace(r_bounds_1[0], r_bounds_2[1], len(Field_dat)) # 433
    raxis_2 = np.linspace(r_bounds_2[0], r_bounds_2[1], len(Field_dat))

    return zaxis_1, zaxis_2, raxis_1, raxis_2

zaxis_1, zaxis_2, raxis_1, raxis_2 = axes() # Evenly spaced axes data

def getBoundCond():
# Define when the electron leaves the plasma
    f = h5.File('data/OSIRIS/Quasi3D/b1_cyl_m-0-re-000130.h5',"r")#('data/OSIRIS/Quasi3D/b1_cyl_m-0-re-000130.h5',"r")
    datasetNames = [n for n in f.keys()] # Three Datasets: AXIS, SIMULATION, Field data
    field = datasetNames[-1]
    Field_dat = f[field][:].astype(float)
    a1_bounds = f['AXIS']['AXIS1'] # zmin and zmax
    a2_bounds = f['AXIS']['AXIS2'] # rmin and rmax - dr/2
    dr = 6.59e-3
    return [a1_bounds[0], a1_bounds[1], a2_bounds[1] + dr/2] # zmin, zmax, rmax

# Return cylindrical Electric field components
# E1 - z
# E2 - r
# E3 - phi

def getE1_M0():
    return getField('data/OSIRIS/Quasi3D/e1_cyl_m-0-re-000130.h5')

def getE2_M0():
    return getField('data/OSIRIS/Quasi3D/e2_cyl_m-0-re-000130.h5')

def getE3_M0():
    return getField('data/OSIRIS/Quasi3D/e3_cyl_m-0-re-000130.h5')

def getE1_M1_Re():
    return getField('data/OSIRIS/Quasi3D/e1_cyl_m-1-re-000130.h5')

def getE2_M1_Re():
    return getField('data/OSIRIS/Quasi3D/e2_cyl_m-1-re-000130.h5')

def getE3_M1_Re():
    return getField('data/OSIRIS/Quasi3D/e3_cyl_m-1-re-000130.h5')

def getE1_M1_Im():
    return getField('data/OSIRIS/Quasi3D/e1_cyl_m-1-im-000130.h5')

def getE2_M1_Im():
    return getField('data/OSIRIS/Quasi3D/e2_cyl_m-1-im-000130.h5')

def getE3_M1_Im():
    return getField('data/OSIRIS/Quasi3D/e3_cyl_m-1-im-000130.h5')

# Return Magnetic Field components
# B1 - z
# B2 - r
# B3 - phi

def getB1_M0():
    return getField('data/OSIRIS/Quasi3D/b1_cyl_m-0-re-000130.h5')

def getB2_M0():
    return getField('data/OSIRIS/Quasi3D/b2_cyl_m-0-re-000130.h5')

def getB3_M0():
    return getField('data/OSIRIS/Quasi3D/b3_cyl_m-0-re-000130.h5')

def getB1_M1_Re():
    return getField('data/OSIRIS/Quasi3D/b1_cyl_m-1-re-000130.h5')

def getB2_M1_Re():
    return getField('data/OSIRIS/Quasi3D/b2_cyl_m-1-re-000130.h5')

def getB3_M1_Re():
    return getField('data/OSIRIS/Quasi3D/b3_cyl_m-1-re-000130.h5')

def getB1_M1_Im():
    return getField('data/OSIRIS/Quasi3D/b1_cyl_m-1-im-000130.h5')

def getB2_M1_Im():
    return getField('data/OSIRIS/Quasi3D/b2_cyl_m-1-im-000130.h5')

def getB3_M1_Im():
    return getField('data/OSIRIS/Quasi3D/b3_cyl_m-1-im-000130.h5')

E1_M0 = getE1_M0()
E2_M0 = getE2_M0()
E3_M0 = getE3_M0()
E1_M1_Re = getE1_M1_Re()
E2_M1_Re = getE2_M1_Re()
E3_M1_Re = getE3_M1_Re()
E1_M1_Im = getE1_M1_Im()
E2_M1_Im = getE2_M1_Im()
E3_M1_Im = getE3_M1_Im()
B1_M0 = getB1_M0()
B2_M0 = getB2_M0()
B3_M0 = getB3_M0()
B1_M1_Re = getB1_M1_Re()
B2_M1_Re = getB2_M1_Re()
B3_M1_Re = getB3_M1_Re()
B1_M1_Im = getB1_M1_Im()
B2_M1_Im = getB2_M1_Im()
B3_M1_Im = getB3_M1_Im()

def getPhi(x,y):
    return math.atan2(y,x) # From -pi to pi

def find_nearest_index(array,value):
    idx = np.searchsorted(array, value, side="right")
    if idx > 0 and (idx == len(array) or math.fabs(value - array[idx-1]) < math.fabs(value - array[idx])):
        return idx-1
    else:
        return idx

def EField(axis,x,y,z,r,vx,vy,vz,vr,vphi):
# axis = 1 refers to z-axis field
# axis = 2 refers to x-axis field
# axis = 3 refers to y-axis field
    phi = getPhi(x,y)
    cos = math.cos(phi)
    sin = math.sin(phi)
    zDex1 = find_nearest_index(zaxis_1, z)
    zDex2 = find_nearest_index(zaxis_2, z)
    rDex1 = find_nearest_index(raxis_1, r)
    rDex2 = find_nearest_index(raxis_2, r)
    # Return expanded EFields
    if axis == 1:
        #return E1_M0[zDex1, rDex2] + E1_M1_Re[zDex1, rDex2]*cos + E1_M1_Im[zDex1, rDex2]*sin
        return E1_M0[rDex2, zDex1] + E1_M1_Re[rDex2, zDex1]*cos + E1_M1_Im[rDex2, zDex1]*sin
    elif axis == 2:
        #return E2_M0[zDex2, rDex1]*cos - E3_M0[zDex2, rDex2]*sin + E2_M1_Re[zDex2, rDex1]*cos**2 - E3_M1_Re[zDex2, rDex2]*cos*sin + E2_M1_Im[zDex2, rDex1]*cos*sin - E3_M1_Im[zDex2, rDex2]*sin**2
        return E2_M0[rDex1, zDex2]*cos - E3_M0[rDex2, zDex2]*sin + E2_M1_Re[rDex1, zDex2]*cos**2 - E3_M1_Re[rDex2, zDex2]*cos*sin + E2_M1_Im[rDex1, zDex2]*cos*sin - E3_M1_Im[rDex2, zDex2]*sin**2
    elif axis == 3:
        #return E3_M0[zDex2, rDex2]*cos + E2_M0[zDex2, rDex1]*sin + E3_M1_Re[zDex2, rDex2]*cos**2 + E2_M1_Re[zDex2, rDex1]*cos*sin + E3_M1_Im[zDex2, rDex2]*cos*sin + E2_M1_Im[zDex2, rDex1]*sin**2
        return E3_M0[rDex2, zDex2]*cos + E2_M0[rDex1, zDex2]*sin + E3_M1_Re[rDex2, zDex2]*cos**2 + E2_M1_Re[rDex1, zDex2]*cos*sin + E3_M1_Im[rDex2, zDex2]*cos*sin + E2_M1_Im[rDex1, zDex2]*sin**2

def BForce(axis,x,y,z,r,vx,vy,vz,vr,vphi):
# axis = 1 refers to z-axis field
# axis = 2 refers to x-axis field
# axis = 3 refers to y-axis field
    phi = getPhi(x,y)
    cos = math.cos(phi)
    sin = math.sin(phi)
    zDex1 = find_nearest_index(zaxis_1, z)
    zDex2 = find_nearest_index(zaxis_2, z)
    rDex1 = find_nearest_index(raxis_1, r)
    rDex2 = find_nearest_index(raxis_2, r)
    # Calculate expanded BFields
    #Bx = B2_M0[zDex2, rDex1]*cos - B3_M0[zDex2, rDex2]*sin + B2_M1_Re[zDex2, rDex1]*cos**2 - B3_M1_Re[zDex2, rDex2]*cos*sin + B2_M1_Im[zDex2, rDex1]*cos*sin - B3_M1_Im[zDex2, rDex2]*sin**2
    #By = B3_M0[zDex2, rDex2]*cos + B2_M0[zDex2, rDex1]*sin + B3_M1_Re[zDex2, rDex2]*cos**2 + B2_M1_Re[zDex2, rDex1]*cos*sin + B3_M1_Im[zDex2, rDex2]*cos*sin + B2_M1_Im[zDex2, rDex1]*sin**2
    #Bz = B1_M0[zDex1, rDex2] + B1_M1_Re[zDex1, rDex2]*cos + B1_M1_Im[zDex1, rDex2]*sin
    Bz = B1_M0[rDex2, zDex1] + B1_M1_Re[rDex2, zDex1]*cos + B1_M1_Im[rDex2, zDex1]*sin
    Bx = B2_M0[rDex1, zDex2]*cos - B3_M0[rDex2, zDex2]*sin + B2_M1_Re[rDex1, zDex2]*cos**2 - B3_M1_Re[rDex2, zDex2]*cos*sin + B2_M1_Im[rDex1, zDex2]*cos*sin - B3_M1_Im[rDex2, zDex2]*sin**2
    By = B3_M0[rDex2, zDex2]*cos + B2_M0[rDex1, zDex2]*sin + B3_M1_Re[rDex2, zDex2]*cos**2 + B2_M1_Re[rDex1, zDex2]*cos*sin + B3_M1_Im[rDex2, zDex2]*cos*sin + B2_M1_Im[rDex1, zDex2]*sin**2
    # Cross-product velocities with BFields and return the BForce
    if axis == 1:
        return vx * By - vy * Bx
    elif axis == 2:
        return vy * Bz - vz * By
    elif axis == 3:
        return -1.0 * (vx * Bz - vz * Bx)

    # elif len(sys.argv) == 4:
    # # Return BField
    #     phi = getPhi(x,y)
    #     rDex = find_nearest_index(r_sim, r)
    #     zDex = find_nearest_index(xi_sim, z)
    # # Calculate expanded BFields
    #     if axis == 1:
    #         return Bx_M0[rDex, zDex] + Bx_M1_Re[rDex, zDex] * math.cos(phi) - Bx_M1_Im[rDex, zDex] * math.sin(phi)
    #     elif axis == 2:
    #         return By_M0[rDex, zDex] + By_M1_Re[rDex, zDex] * math.cos(phi) - By_M1_Im[rDex, zDex] * math.sin(phi)
    #     elif axis == 3:
    #         return Bz_M0[rDex, zDex] + Bz_M1_Re[rDex, zDex] * math.cos(phi) - Bz_M1_Im[rDex, zDex] * math.sin(phi)
