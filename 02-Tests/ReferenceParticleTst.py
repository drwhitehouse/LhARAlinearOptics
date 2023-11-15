#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for "ReferenceParticle" derived class
=================================================

  ReferenceParticle.py -- set "relative" path to code

"""

import Particle as Prtcl
import sys

##! Start:
print("========  ReferenceParticle: tests start  ========")

##! Test singleton class feature:
ReferenceParticleTest = 1
print()
print("ReferenceParticleTest:", ReferenceParticleTest, \
      " check if class is a singleton.")
refPrtcl  = Prtcl.ReferenceParticle()
try:
    refPrtcl1 = Prtcl.ReferenceParticle()
except:
    print("    refPrtcl singleton test: success")
else:
    print("    refPrtcl singleton test: FAIL!")
    raise Exception("ReferenceParticle is not a singleton class!")

##! Check built-in methods:
ReferenceParticleTest = 2
print()
print("ReferenceParticleTest:", ReferenceParticleTest, \
      " check built-in methods.")
print("    __repr__:")
print(refPrtcl)

##! Check get methods:
ReferenceParticleTest = 3
print()
print("ReferenceParticleTest:", ReferenceParticleTest, " check get methods.")
print("    ----> Tests all get methods")
print(refPrtcl)

##! Check set method:
ReferenceParticleTest = 4
print()
print("ReferenceParticleTest:", ReferenceParticleTest, " check set method.")
refPrtcl.setRPDebug(True)
print(refPrtcl)
refPrtcl.setRPDebug(False)

##! Check get instance methodd:
ReferenceParticleTest += 1
print()
print("ReferenceParticleTest:", ReferenceParticleTest, \
      " check get instane method.")
print(Prtcl.ReferenceParticle.getinstance())

##! Complete:
print()
print("========  ReferenceParticle: tests complete  ========")
