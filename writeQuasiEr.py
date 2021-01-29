import numpy as np
import matplotlib.colors as col
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 20})
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.ticker as ticker
import pdb
import time
import include.simulations.useQuasi3D as sim
import xlsxwriter

def getFieldArrays():

    xiaxis_1, xi2, raxis_1, r2 = sim.axes()
    xiiter = len(xiaxis_1)
    riter = len(raxis_1)

    Er_full = np.empty((riter,xiiter),dtype=float)
    Er_m0 = np.empty((riter,xiiter),dtype=float)
    Er_m1 = np.empty((riter,xiiter),dtype=float)

    for ir in range(riter):
        print(ir)
        for ixi in range(xiiter):
            #pdb.set_trace()
            Er_full[ir, ixi] = sim.EField(2, raxis_1[ir], 0, xiaxis_1[ixi], raxis_1[ir], mode=-1)
            Er_m0[ir, ixi] = sim.EField(2, raxis_1[ir], 0, xiaxis_1[ixi], raxis_1[ir], mode=0)
            Er_m1[ir, ixi] = sim.EField(2, raxis_1[ir], 0, xiaxis_1[ixi], raxis_1[ir], mode=1)

    return xiaxis_1, raxis_1, Er_full, Er_m0, Er_m1

def main():

    start_time = time.time()
    t0 = sim.getTime()

    xiaxis, raxis, Er_full, Er_m0, Er_m1 = getFieldArrays()
    zaxis = [xi + t0 for xi in xiaxis]

    workbook = xlsxwriter.Workbook('TransverseEr.xlsx')
    worksheet = workbook.add_worksheet()

# Write titles of columns
    worksheet.write(0, 0, 'xi')
    worksheet.write(0, 1, 'z')
    worksheet.write(0, 2, 'r')
    worksheet.write(0, 3, 'Er M0')
    worksheet.write(0, 4, 'Er M1')
    worksheet.write(0, 5, 'Er M0+M1')

# Start filling values
    row = 0
    for val in (xiaxis):
        worksheet.write(row, 0, val)
        row += 1

    row = 0
    for val in (zaxis):
        worksheet.write(row, 1, val)
        row += 1

    row = 0
    for val in (raxis):
        worksheet.write(row, 2, val)
        row += 1

    row = 0
    for val in (Er_m0):
        worksheet.write(row, 3, val)
        row += 1

    row = 0
    for val in (Er_m1):
        worksheet.write(row, 4, val)
        row += 1

    row = 0
    for val in (Er_full):
        worksheet.write(row, 5, val)
        row += 1

    workbook.close()

    input()

main()
