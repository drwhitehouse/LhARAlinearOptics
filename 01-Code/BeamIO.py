#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class BeamIO:
=============

  Class provides management of file handling and i/o for the Beam
  package.

"""

import io
import os
import struct as strct

import BeamLine as BL
import Particle as Prtcl

class BeamIO:
    instances = []
    __Debug   = False

#--------  "Built-in methods":
    def __init__(self, _datafilePATH=None, _datafileNAME=None, \
                 _create=False):
        if self.getDebug():
            print(' BeamIO.__init__: ', \
                  'creating BeamIO object')

        BeamIO.instances.append(self)

        self.setAll2None()

        #.. Sanity checks on i/p arguments:
        if not isinstance(_create, bool):
            raise badCreate( \
                         " BeamIO.__init__: bad create flag")

        if _datafilePATH == None and _datafileNAME == None:
            raise noPATH( \
                         " BeamIO.__init__: neither path or file name set.")
        
        elif _datafileNAME == None: 
            raise noNAME( \
                    " BeamIO.__init__: file name not set.")

        #.. Check path and, if necessary, join to file:
        if _datafilePATH != None:
            if not os.path.exists(_datafilePATH):
                raise noPATH( \
                    " Particle.createParticleFile: path does not exist.")

            pathFILE = os.path.join(_datafilePATH, _datafileNAME)

        else:
            pathFILE = _datafileNAME

        if self.getDebug():
            print("     ----> Proced with data file:", pathFILE)

        #.. open file; if file doesnt exist or _create is true, create it:
        if not os.path.isfile(pathFILE) or _create:
            dataFILE = open(pathFILE, "wb")
            if self.getDebug():
                print("         ----> File opened for write.")
                
            record = strct.pack(">i", 9999)
            dataFILE.write(record)
            if self.getDebug():
                print("         ----> First word:", \
                        strct.unpack(">i", record), \
                      " is a large integer to distinguish v2 from v1")
                
            version  = "BeamIO v2"
            bversion = bytes(version, 'utf-8')
            record   = strct.pack(">i", len(version))
            dataFILE.write(record)
            if self.getDebug():
                print("         ----> Length of version record:", \
                      strct.unpack(">i", record))
            record   = bversion
            dataFILE.write(record)
            if self.getDebug():
                print("         ----> Version:", bversion.decode('utf-8'))

        else:
            dataFILE = open(pathFILE, "rb")
            if self.getDebug():
                print("         ----> File opened for read.")

        if self.getDebug():
            print("     <---- File ready.")

        self.setdataFILE(dataFILE)
        
        if self.__Debug:
            print("     ----> New BeamIO instance: \n", \
                  BeamIO.__str__(self))
            print(" <---- BeamIO instance created.")
            
    def __repr__(self):
        return "BeamIO(<data file path>, <data file name>)"

    def __str__(self):
        self.print()
        return " <---- BeamIO __str__ done. \n"

    def print(self):
        print("\n BeamIO:")
        print(" -------")
        print("     ----> Debug flag:", self.getDebug())
        print("     ----> Data file:", self.getdataFILE())

        
#.. Flush and close
    def flushNclosedataFile(self, dataFILE=None):
        if self.getDebug():
            print(" BeamIO.flushNclosedataFile starts")
            print("     ----> File:", dataFILE)

        if not isinstance(dataFILE, io.BufferedWriter):
            raise noFILE( \
                    " BeamIO.flushNcloseParticle: file does not exist.")

        dataFILE.flush()
        dataFILE.close()

#.. Manage read:
    def readBeamDataRecord(self):
        if self.getDebug():
            print(" BeamIO.readBeamDataRecord starts.")
            print("     ----> Read first record:", \
                  self.getReadFirstRecord())

        if not isinstance(self.getdataFILE(), io.BufferedReader):
            raise noFILE( \
                    " BeamIO.readBeamDataRecord: file does not exist.")

        EoF = False

        #.. First record identifies first version of data format:
        if not self.getReadFirstRecord():
            brecord = self.getdataFILE().read(4)
            if brecord == b'':
                if self.getDebug():
                    print(" <---- end of file, return.")
                return True
            
            self.setReadFirstRecord(True)
            record = strct.unpack(">i", brecord)
            nId    = record[0]
            if self.getDebug():
                print("     ----> Id number:", nId)
                
            self.setdataFILEversion(1)
            if nId == 9999:
                if self.getDebug():
                    print("           Not version 1!")
                Version = self.readVersion()
                self.setdataFILEversion(int(Version[-1]))
                if self.getDebug():
                    print("           Version:", \
                          self.getdataFILEversion())
                    
                BL.BeamLine.readBeamLine(self.getdataFILE())
            else:
                if self.getDebug():
                    print("           Handle version 1!")
                self.getdataFILE().seek(0)
                #EoF = Prtcl.Particle.readParticle(self.getdataFILE())
                
            if self.getDebug():
                print("     <---- Data file format version:", \
                      self.getdataFILEversion())
        else:
            EoF = Prtcl.Particle.readParticle(self.getdataFILE())
            if self.getDebug():
                print("     <---- BeamIO.readBeamDataRecord particle read.")
            
        if self.getDebug():
            print(" <---- BeamIO.readBeamDataRecord Done.")

        return EoF

    def readVersion(self):
        if self.getDebug():
            print(" BeamIO.readVersion start.")

        brecord = self.getdataFILE().read(4)
        record  = strct.unpack(">i", brecord)
        len     = record[0]
        if self.getDebug():
            print("         ----> Length of version:", len)
            
        brecord  = self.getdataFILE().read(len)
        Version = brecord.decode('utf-8')
        if self.getDebug():
            print(" <---- Version:", Version)

        return Version
        
        
#--------  "Set method" only Debug
#.. Method believed to be self documenting(!)

    @classmethod
    def setDebug(cls, Debug=False):
        if cls.__Debug:
            print(" BeamIO.setdebug: ", Debug)
        cls.__Debug = Debug
        
    def setAll2None(self):
        self._dataFile        = None
        self._Rd1stRcrd       = False
        self._dataFILEversion = None

    @classmethod
    def resetinstances(cls):
        cls.instances = []
        
    def setdataFILE(self, _dataFILE):
        self._dataFILE = _dataFILE

    def setReadFirstRecord(self, _Rd1stRcrd):
        if not isinstance(_Rd1stRcrd, bool):
            raise badArgument()
        self._Rd1stRcrd = _Rd1stRcrd 

    def setdataFILEversion(self, dataFILEversion):
        if not isinstance(dataFILEversion, int):
            raise badArgument()
        self._dataFILEversion = dataFILEversion

        
#--------  "Get methods" only; version, reference, and constants
#.. Methods believed to be self documenting(!)
    @classmethod
    def getDebug(cls):
        return cls.__Debug

    @classmethod
    def getinstances(cls):
        return cls.instances

    def getdataFILE(self):
        return self._dataFILE

    def getReadFirstRecord(self):
        return self._Rd1stRcrd

    def getdataFILEversion(self):
        return self._dataFILEversion


#--------  Utilities:
    @classmethod
    def cleanBeamIOfiles(cls):
        DoneOK = False
        
        for iIOfl in cls.getinstances():
            del iIOfl
            
        cls.resetinstances()
        DoneOK = True

        return DoneOK

    
#--------  Exceptions:
class noPATH(Exception):
    pass

class noNAME(Exception):
    pass

class noFILE(Exception):
    pass
        
class badCreate(Exception):
    pass

class badArgument(Exception):
    pass
        
