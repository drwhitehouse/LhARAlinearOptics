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
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import date
from scipy.optimize import curve_fit

import BeamLineElement   as BLE
import BeamLine          as BL
import Particle          as Prtcl
import PhysicalConstants as PhysCnst


#.. Physical Constants:
constants_instance = PhysCnst.PhysicalConstants()
protonMASS         = constants_instance.mp()

#.. Initialise:
HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-LsrDrvn.csv')
BLI  = BL.BeamLine(filename)

iRefPrtcl = Prtcl.ReferenceParticle.getinstances()


##! Start:
print("========  Source: tests start  ========")

##! Test creation and built-in methods:
SourceTest = 1

Src = BLE.Source.getinstances()[0]
Src.getParticle()

print(Src)
print("     ----> Generation:")

PrtclKE  = np.array([])
PrtclcT  = np.array([])
PrtclT   = np.array([])

g_E       = Src.getLaserDrivenProtonEnergyProbDensity()
E_max_MeV = Src.getderivedParameters()[4] / (1.6e-19 * 1e6)
E_min_MeV = Src.getderivedParameters()[5] / (1.6e-19 * 1e6)

for i in range(100000):
    X, Y, KE, cTheta, Phi = Src.getParticle()

    TrcSpcFrmSrc = Src.getParticleFromSource()
    PhsSpcFrmSrc = Prtcl.Particle.RPLCTraceSpace2PhaseSpace(TrcSpcFrmSrc)

    p        = mth.sqrt(np.dot(PhsSpcFrmSrc[1], PhsSpcFrmSrc[1]))
    Etot     = mth.sqrt(protonMASS**2 + \
                        np.dot(PhsSpcFrmSrc[1], PhsSpcFrmSrc[1]))

    KE       = Etot - protonMASS
    PrtclKE  = np.append(PrtclKE , KE)

    cTheta   = PhsSpcFrmSrc[1][2] / p
    PrtclcT  = np.append(PrtclcT , cTheta)

    Theta    = mth.acos(cTheta) * 180. / mth.pi
    PrtclT   = np.append(PrtclT , Theta)

    
##! Next: calculate and plot RMSs
bin_width = 0.15
energy_bins = np.arange(E_min_MeV, E_max_MeV, bin_width)
rms_theta = []

for i in range(len(energy_bins) - 1):
    min_ke = energy_bins[i]
    max_ke = energy_bins[i+1]
    
    Nbin = 0
    thetasum = 0.0
    theta2sum = 0.0

    for j in range(len(PrtclKE)):
        kE = PrtclKE[j]
        theta = PrtclT[j]
        
        if min_ke < kE <= max_ke:
            Nbin += 1
            thetasum += theta
            theta2sum += theta**2

    if Nbin > 0:
        mean_theta = thetasum / Nbin
        mean_theta2 = theta2sum / Nbin
        rms_theta_value = np.sqrt(mean_theta2 - mean_theta**2)
        rms_theta.append(rms_theta_value)
    else:
        rms_theta.append(0)

energy_bins_center = (energy_bins[:-1] + energy_bins[1:]) / 2 
rms_theta = np.array(rms_theta)

coefficients, covariance_matrix = \
    np.polyfit(energy_bins_center, rms_theta, 1, cov=True)
linear_fit = np.poly1d(coefficients)

slope_error = np.sqrt(covariance_matrix[0, 0])
intercept_error = np.sqrt(covariance_matrix[1, 1])

x_fit = np.linspace(min(energy_bins_center), max(energy_bins_center), 500)
y_fit = linear_fit(x_fit)

plt.figure(figsize=(8, 5))
plt.scatter(energy_bins_center, rms_theta, s=5, color='black')

Scl = mth.sqrt(1. - 2./mth.pi)
expectation = [-Src.getParameters()[14]/E_max_MeV*Scl, Src.g_theta(0.)*Scl]
plt.plot(x_fit, y_fit, color='red', \
         label=f'    Linear Fit:    RMS $\\theta_S = ({coefficients[0]:.3f} \\pm {slope_error:.3f})$K$ + ({coefficients[1]:.2f} \\pm {intercept_error:.2f})$')
plt.plot([], [], ' ', \
         label=f'Expectation:    RMS $\\theta_S = {expectation[0]:.3f}$K$ + {expectation[1]:.2f}$')

plt.xlabel('Kinetic energy, $K$ (MeV)')
plt.ylabel('RMS $\\theta_S$ (degrees)')
plt.title('RMS $\\theta_S$ versus kinetic energy')
plt.legend()
plt.savefig('99-Scratch/RMS_Set_kE.pdf')
plt.close()
