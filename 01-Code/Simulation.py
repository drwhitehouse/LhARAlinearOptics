#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Simulation
================

  CEO class for linear optics simulation of beam lines.

  Class attributes:
  -----------------
  __instance : Set on creation of first (and only) instance.
  __Debug    : Debug flag
__RandomSeed : Seed for random number, set to time at load of class.  
__Facility : Address of instance of a facility

  Packages loaded:
  ----------------
  "time"  : to get current date/time
  "random": uniform random number generator
      
  Methods defined at Module level:
  --------------------------------
    getRandom : no input, returns random numerm calls random.random.
 getParabolic : Generate random number distributed as an inverted parabola
                from -p1 to p1.
           Input : p1 [float]
       Return : Probability [float]

  Instance attributes:
  --------------------
            _NEvt : Number of events to generate
   _ParamFileName : csv file containing parameters of the simulation
    _RootFileName : Root file for o/p
    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __new__ : Creates singleton class and prints version, PDG
                reference, and values of constants used.
      __repr__: One liner with call.
      __str__ : Dump of contents

  Get/set methods:
      CdVrsn()     : Returns code version number.
      getRandomSeed: Returns random seed
           setDebug: Set debug flag
           getDebug: Get debug flag
   getFacility: Get __Facility
            getNEvt: Get NEvt
  
  Simulation methods:
      getRandom    : Returns uniformly distributed randum number
      getParabolic : Generates a parabolic distributed random number from
                     -p1 to p1 (p1 input)
            RunSim : CEO method to run simulation.

          Utilities:
                print : Print summary of paramters


Created on Thu 10Jan21;11:04: Version history:
----------------------------------------------
 1.0: 21Jul23: First implementation

@author: kennethlong
"""

#--------  Module dependencies
import random as __Rnd
import numpy as np
import sys

import BeamIO   as BmIO
import BeamLine as BL
import Particle as Prtcl

#--------  Module methods
def getRandom():
    return __Rnd.random()

def getParabolic(p1):
    ran = getRandom()
    a = np.array( [ 1., 0., (-3.*p1*p1), (2.*p1*p1*p1*(2.*ran - 1.)) ] )
    r = np.roots(a)
    isol = 0
    for ri in r:
        if not isinstance(ri, complex):
            if ri >= -p1:
                if ri <= p1:
                    isol += 1
                    p = ri
    if isol != 1:
        raise Exception("Simulation.getParabolic; p multiply defined")

    return p

#--------  Simulation class  --------
class Simulation(object):
    import random as __Rnd
    import time as __T
    
    __RandomSeed = __T.time()

    __Debug     = False
    __instance  = None


#--------  "Built-in methods":
    def __new__(cls, NEvt=5, filename=None, 
                _dataFileDir=None, _dataFileName=None):
        if cls.__instance is None:
            if cls.getDebug():
                print('Simulation.__new__: creating the Simulation object')
                print('-------------------')
            cls.__instance = super(Simulation, cls).__new__(cls)
            
            cls.__Rnd.seed(int(cls.__RandomSeed))

            cls._NEvt          = NEvt
            cls._ParamFileName = filename
            cls._dataFileDir   = _dataFileDir
            cls._dataFileName  = _dataFileName

            # Create Facility instance:
            cls._Facility = BL.BeamLine(filename)

            # Open file for write:
            cls._iBmIOw   = BmIO.BeamIO(_dataFileDir, _dataFileName, True)
            
            # Summarise initialisation
            if cls.getDebug():
                cls.print(cls)

        return cls.__instance

    def __repr__(self):
        return "Simulation()"

    def __str__(self):
        self.__repr__()
        self.print()

            
#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)

    def CdVrsn(self):
        return 1.0

    def getRandomSeed(self):
        return Simulation.__RandomSeed

    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def setDebug(cls, _Debug=False):
        cls.__Debug = _Debug

    @classmethod
    def getFacility(cls):
        return cls._Facility

    @classmethod
    def getdataFileDir(cls):
        return cls._dataFileDir

    @classmethod
    def getdataFileName(cls):
        return cls._dataFileName

    def getNEvt(self):
        return self._NEvt

    def getiBmIOw(self):
        return self._iBmIOw

#--------  Utilities:
    def print(self):
        print(" Simulation.print:")
        print("                        Version:", self.CdVrsn(self))
        print("      State of random generator:", self.__Rnd.getstate()[0])
        print("   Number of events to generate:", self._NEvt)
        print("   Beam line specification file:", self._ParamFileName)
        print(" data file directory for output:", self._dataFileDir)
        print("       data filename for output:", self._dataFileName)
        print(" BeamIO output file instance id:", id(self.getiBmIOw()))

        
#--------  Simulation run methods
    def RunSim(self):
        if self.getDebug():
            print()
            print('Simulation.RunSim: simulation begins')
            print('-----------------')

        """
        #.. Open file to store events:
        ParticleFILE = None
        if self.getdataFileDir()  != None and \
           self.getdataFileName() != None:
            ParticleFILE = Prtcl.Particle.createParticleFile( \
                                            self.getdataFileDir(), \
                                            self.getdataFileName() )
        """

        #.. Write facility:
        BL.BeamLine.getinstance().writeBeamLine( \
                                        self.getiBmIOw().getdataFILE())

        #.. Transport particles through facility:
        
        nEvt = self.getFacility().trackBeam(self.getNEvt(), \
                                            self.getiBmIOw().getdataFILE())

        #.. Flush and close particle file:
        self.getiBmIOw().flushNclosedataFile( \
                                    self.getiBmIOw().getdataFILE())
        
