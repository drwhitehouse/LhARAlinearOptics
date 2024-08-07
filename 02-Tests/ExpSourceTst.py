#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Source" class
=============================

  Source.py -- set "relative" path to code

"""

import os
import math  as mth
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

import BeamLineElement as BLE
import BeamLine        as BL
import Particle        as Prtcl

HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
BLI  = BL.BeamLine(filename)

iRefPrtcl = Prtcl.ReferenceParticle.getinstance()


##! Start:
print("========  Source: tests start  ========")

##! Test creation and built-in methods:
SourceTest = 1
print()
print("SourceTest:", SourceTest, \
      " check creation and built-in methods.")

#.. __init__
print("    __init__:")
try:
    Src = BLE.Source()
except:
    print('      ----> Correctly trapped no argument exception.')
rStrt = np.array([0.,0.,0.])
vStrt = np.array([[np.pi/2.,np.pi/2.],[0.,0.]])
drStrt = np.array([0.,0.,0.])
dvStrt = np.array([[0.,0.],[0.,0.]])
try:
    Src = BLE.Source(rStrt, vStrt, drStrt, dvStrt)
except:
    print('      ----> Correctly trapped no Source paramters exception.')

#.. Create valid instance:
Mode  = 0
Param = [0.000004, 0.000004, 0.998,    \
          1., 25., 1000, 2.50e15, 70., 0.8, 2.80e-14, 4.00e-07, 4.00e20, 25.]
Src = BLE.Source("Source0", rStrt, vStrt, drStrt, dvStrt, Mode, Param)
    
#.. __repr__
print("    __repr__:")
print("      ---->", repr(Src))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(str(Src))
print("    <---- __str__ done.")

print(" <---- Creation and built in method tests done!  --------  --------")


##! Next: check paramterised laser-driven source distribution:
SourceTest += 1
print()
print("SourceTest:", SourceTest, \
      " test parameterised laser-driven source distribution ", \
      "check.")
Src1 = BLE.Source("Source2", rStrt, vStrt, drStrt, dvStrt, \
                  0, [0.000004, 0.000004, 0.998, 1., 25., 1000, 2.50e15, 70., 0.8, 2.80e-14, 4.00e-07, 4.00e20, 25.])
print(Src1)
print(" Test generation:")
print("     ----> First particle: KE, cosThetaPhi:", \
      Src1.getParticle())

##! Next: Get data for plots:
PrtclX   = np.array([])
PrtclY   = np.array([])
PrtclKE  = np.array([])
PrtclcT  = np.array([])
PrtclPhi = np.array([])

SrcX     = np.array([])
SrcY     = np.array([])
SrcXp    = np.array([])
SrcYp    = np.array([])
SrcE     = np.array([])

g_E       = Src1.getLaserDrivenProtonEnergyProbDensity()
E_max_MeV = Src1.getderivedParameters()[4] / (1.6e-19 * 1e6)
E_min_MeV = Src1.getderivedParameters()[5] / (1.6e-19 * 1e6)

print("     ----> Generate many particles:")
for i in range(100000):
    X, Y, KE, cTheta, Phi = Src1.getParticle()
    
    PrtclX   = np.append(PrtclX , X)
    PrtclY   = np.append(PrtclY , Y)
    PrtclKE  = np.append(PrtclKE , KE)
    PrtclcT  = np.append(PrtclcT , cTheta)
    PrtclPhi = np.append(PrtclPhi, Phi)

    TrcSpcFrmSrc = Src1.getParticleFromSource()
    PhsSpcFrmSrc = Prtcl.Particle.RPLCTraceSpace2PhaseSpace(TrcSpcFrmSrc)
    
    SrcX         = np.append(SrcX,  TrcSpcFrmSrc[0])
    SrcY         = np.append(SrcY,  TrcSpcFrmSrc[2])
    SrcXp        = np.append(SrcXp, TrcSpcFrmSrc[1])
    SrcYp        = np.append(SrcYp, TrcSpcFrmSrc[3])
    SrcE         = np.append(SrcE,  TrcSpcFrmSrc[5])
print("     <---- Done.")
    
##! Next: Make plots:
print("     ----> Make plots:")

#.. ----> Energy:
print("         ----> Energy:")

Ee, g_E = Src1.getLaserDrivenProtonEnergyProbDensity()

dE2     = (E_max_MeV - E_min_MeV) / 100. / 2.
Ee[-1] -= dE2

# Normalise:
hist_heights, bin_edges = np.histogram(PrtclKE, bins=100)
histCntnts = np.sum(hist_heights)
g_scaled   = g_E * histCntnts

# Plot required distribution:
plt.plot(Ee, g_scaled, color='r', label='Required Distribution', linewidth=1)

y_max_cutoff = g_scaled[-1]
x            = E_max_MeV
plt.vlines(x, ymin=0, ymax=y_max_cutoff, color='r', \
           linestyle='-', linewidth=1)  # [MeV]

plt.xlabel('Energy (MeV)')
plt.ylabel('Entries')
plt.yscale("log")
plt.legend(loc="best")
today = date.today().strftime("%m/%d/%Y")

plt.title('ExpSourceTst (' + today + '): Energy distribution',
          weight='bold', size=12)
plt.savefig('99-Scratch/SourceTst_plot13_Dist.pdf')
plt.close()

print("         <---- Done.")
exit()

#.. ----> Cumulative probability:
n, bins, patches = plt.hist(PrtclX, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('X (m)')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: X position distribution')
plt.savefig('99-Scratch/SourceTst_plot11.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclY, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Y (m)')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: Y position distribution')
plt.savefig('99-Scratch/SourceTst_plot12.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclKE, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Energy (MeV)')
plt.ylabel('Entries')
plt.yscale("log")
plt.title('LsrDrvnSrc: Energy distribution')
plt.savefig('99-Scratch/SourceTst_plot13.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclKE, \
                            bins=100, color='k', \
                            histtype='step', label='Generated Distribution')


cumPROB = []
for eps in Ee:
    eps1 = eps * (1.6e-19 * 1e6)
    cumPROB.append(Src1.getLaserCumProb(eps1))
plt.plot(Ee, cumPROB, color='k', label='Required Distribution', linewidth=2)
plt.xlabel('Energy (MeV)')
plt.ylabel('Cumulative probability')
plt.yscale("linear")
plt.legend(loc="best")
plt.title('LsrDrvnSrc: cumulative probability')
plt.savefig('99-Scratch/SourceTst_plot13_cumulative.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclcT, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('cos(theta)')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: (cos) polar angle distribution')
plt.savefig('99-Scratch/SourceTst_plot14.pdf')
plt.close()

n, bins, patches = plt.hist(PrtclPhi, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Phi')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: Azimuthal; angle distribution')
plt.savefig('99-Scratch/SourceTst_plot15.pdf')
plt.close()

n, bins, patches = plt.hist(SrcX, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('X')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: X position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot16.pdf')
plt.close()

n, bins, patches = plt.hist(SrcY, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Y')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: Y position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot17.pdf')
plt.close()

n, bins, patches = plt.hist(SrcXp, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('X-prime')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: X-prime position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot18.pdf')
plt.close()

n, bins, patches = plt.hist(SrcYp, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('Y-prime')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: Y-prime position at exit from source')
plt.savefig('99-Scratch/SourceTst_plot19.pdf')
plt.close()

n, bins, patches = plt.hist(SrcE, \
                            bins=50, color='y', \
                            log=False)
plt.xlabel('delta')
plt.ylabel('Entries')
plt.title('LsrDrvnSrc: delta at exit from source')
plt.savefig('99-Scratch/SourceTst_plot20.pdf')
plt.close()


##! Complete:
print()
print("========  Source: tests complete  ========")
