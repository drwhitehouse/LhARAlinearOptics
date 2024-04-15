#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "Beam" class
============================

  Beam.py -- set "relative" path to code

"""

import os
import numpy as np

import BeamLine as BL
import Beam as Bm

##! Start:
print("========  Beam: tests start  ========")

##! Test trap of no reference particle:
BeamTest = 0
print()
print("BeamTest:", BeamTest, " check need reference particle first!")
try:
    BmInst = Bm.Beam()
except:
    print("     ----> Successfully trapped no reference beam")
else:
    print("     ----> Failed successfully to trapped no reference beam", \
          " abort")
    raise Exception()
Bm.Beam.cleanBeams()

##! Now create reference beam:
HOMEPATH = os.getenv('HOMEPATH')
filename = os.path.join(HOMEPATH, \
                        '11-Parameters/LIONBeamLine-Params-Gauss.csv')

##! Now create pointer to input data file:
inputdatafile = os.path.join(HOMEPATH, \
                       '11-Parameters/Data4Tests.dat')

##! Now create pointer to output data file:
outputdatafile = os.path.join(HOMEPATH, \
                       '99-Scratch/BeamParamteres.csv')

##! Test input arguments:
BeamTest += 1
print()
print("BeamTest:", BeamTest, " check trap no beam specification file!")
try:
    BmInst = Bm.Beam()
except:
    print("     ----> Successfully trapped no beam specigication file")
else:
    print("     ----> Failed successfully to trap no beam specification file", \
          " abort")
    raise Exception()
Bm.Beam.cleanBeams()

##! Create valid instance
BeamTest += 1
print()
print("BeamTest:", BeamTest, " create valid instance:")
BmInst = Bm.Beam(inputdatafile, 1000, outputdatafile, None, filename)

##! Create valid instance
BeamTest += 1
print()
print("BeamTest:", BeamTest, " test built-in methods:")
#.. __repr__
print("    __repr__:")
print("      ---->", repr(BmInst))
print("    <---- __repr__ done.")
#.. __str__
print("    __str__:")
print(BmInst)
print("    <---- __str__ done.")

##! Check creation of report:
BeamTest += 1
print()
print("BeamTest:", BeamTest, " creation of pandas report.")

BmInst.evaluateBeam()
BmInst.createReport()
print(BmInst)

##! Complete:
print()
print("========  Beam: tests complete  ========")
