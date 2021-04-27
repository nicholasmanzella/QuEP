import math
import numpy as np

def getTrajectory(x_0,y_0,xi_0,px_0,py_0,pz_0,t0,iter,plasma_bnds,mode,sim_name):
# Returns array of x, y, xi, z, and final x, y, xi, z, px, py, pz

    if (sim_name.upper() == 'OSIRIS_CYLINSYMM'):
        import include.simulations.useOsiCylin as sim
    elif (sim_name.upper() == 'QUASI3D'):
        import include.simulations.useQuasi3D as sim
    else:
        print("Simulation name unrecognized. Quitting...")
        exit()

    def Gamma(p):
        return math.sqrt(1.0 + p**2)

    def Velocity(px,ptot):
    # Returns relativistic velocity from momentum
        return px / Gamma(ptot)

    def sortVelocity(x,y,vx,vy,vr):
    # Obtain proper sign of velocity based on quadrant
        if (x >= 0 and y >= 0):                  # Quadrant 1
            if (vx >= 0 and vy >= 0):
                return vr
            elif (vx < 0 and vy < 0):
                return -1.0 * vr
            elif (abs(vx) > abs(vy)):
                if vx > 0:
                    return vr
                else:
                    return -1.0 * vr
            elif (abs(vy) > abs(vx)):
                if vy > 0:
                    return vr
                else:
                    return -1.0 * vr
        elif (x < 0 and y >= 0):                 # Quadrant 2
            if (vx <= 0 and vy >= 0):
                    return vr
            elif (vx > 0 and vy < 0):
                    return -1.0 * vr
            elif (abs(vx) > abs(vy)):
                if vx > 0:
                    return -1.0 * vr
                else:
                    return vr
            elif (abs(vy) > abs(vx)):
                if vy > 0:
                    return vr
                else:
                    return -1.0 * vr
        elif (x < 0 and y < 0):                   # Quadrant 3
            if (vx >= 0 and vy >= 0):
                return -1.0 * vr
            elif (vx < 0 and vy < 0):
                return vr
            elif (abs(vx) > abs(vy)):
                if vx > 0:
                    return -1.0 * vr
                else:
                    return vr
            elif (abs(vy) > abs(vx)):
                if vy > 0:
                    return vr
                else:
                    return -1.0 * vr
        elif (x >= 0 and y < 0):                 # Quadrant 4
            if (vx >= 0 and vy <= 0):
                return vr
            elif (vx < 0 and vy > 0):
                return -1.0 * vr
            elif (abs(vx) > abs(vy)):
                if vx > 0:
                    return vr
                else:
                    return -1.0 * vr
            elif (abs(vy) > abs(vx)):
                if vy > 0:
                    return -1.0 * vr
                else:
                    return vr

    def Momentum(x,y,xi,dt,px,py,pz,mode):
        # Returns the new momentum after dt, in units of c in the axis direction
        p = math.sqrt(px**2 + py**2 + pz**2)
        vx = Velocity(px, p)
        vy = Velocity(py, p)
        vz = Velocity(pz, p)
        r = math.sqrt(x**2 + y**2)
        vr = math.sqrt(vx**2 + vy**2)
        vr = sortVelocity(x, y, vx, vy, vr)
        if (r > 0):
            vphi = vr/r
        else:
            vphi = 0

        Fx = -1.0 * (sim.EField(2, x, y, xi, r, vx, vy, vz, vr, vphi, mode) + sim.BForce(2, x, y, xi, r, vx, vy, vz, vr, vphi, mode))
        Fy = -1.0 * (sim.EField(3, x, y, xi, r, vx, vy, vz, vr, vphi, mode) + sim.BForce(3, x, y, xi, r, vx, vy, vz, vr, vphi, mode))
        Fz = -1.0 * (sim.EField(1, x, y, xi, r, vx, vy, vz, vr, vphi, mode) + sim.BForce(1, x, y, xi, r, vx, vy, vz, vr, vphi, mode))

        px = px + Fx * dt
        py = py + Fy * dt
        pz = pz + Fz * dt
        p = math.sqrt(px**2 + py**2 + pz**2)
        gam = Gamma(p)
        return px, py, pz, p, gam, Fx, Fy, Fz

    t = t0                       # Start time in 1/w_p
    dt = 0.005 #0.005                   # Time step in 1/w_p
    xn = x_0                     # Positions in c/w_p
    yn = y_0
    xin = xi_0
    zn = xin + t0

    px = px_0                    # Momenta in m_e c
    py = py_0
    pz = pz_0

    # Iterate through position and time using a linear approximation
    for i in range(0, iter):
        # Determine new momentum and velocity from this position
        px, py, pz, p, gam, Fx, Fy, Fz = Momentum(xn, yn, xin, dt, px, py, pz, mode)

        vxn = Velocity(px, p)
        vyn = Velocity(py, p)
        vzn = Velocity(pz, p)

        xn += vxn * dt
        yn += vyn * dt
        zn += vzn * dt
        rn = math.sqrt(xn**2 + yn**2)

        t += dt
        xin = zn - t

        # If electron leaves cell, quit tracking
        if (xin < plasma_bnds[0] or xin > plasma_bnds[1] or rn > plasma_bnds[2]):
            return xn, yn, xin, zn, px, py, pz

    print("Tracking quit due to more than ", iter, " iterations in plasma")
    return xn, yn, xin, zn, px, py, pz
