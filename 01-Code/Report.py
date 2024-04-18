#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Report:
=============

  Collection of derived classes to generate reports, usually in the
  form of a CSV file, based on the Project, WorkPackage, and Task classes

  Derived classes for the creation of various reports included:
    - CommunicationSummary(Report):
      - Summarises the communication with the candidate

    - CandidateList(Report):
      - makes the "candidate list" report

    - OfferAcceptList(Report):
      - makes the "offer and aceptance list" report

    - CommunicationSummary(Report):
      - makes the "communication summary" report

    - RecruitmentSummary(Report):
      - makes the "recruitment summary" report


  Class attributes:
  -----------------
  __Debug  : Boolean: set for debug print out
  instances: List of instances of Project class


  Instance attributes:
  --------------------
    _Name      : (str) name of report
    _ReportPath: Path to directory into which report file will be written
    _FileName  : Report filename
    _Header    : List of header fields; initialised to [].  
                 Filled in derived classes.
    _Lines     : Lines of report; initialised to [].
                 Filled in derived classes.

    
  Methods:
  --------
  Built-in methods __new__, __repr__ and __str__.
      __init__: Creates instance and prints some parameters if __Debug is 
                True.
      __repr__: One liner with call.
      __str__ : Dump of constants.


  Processing methods:
      createPandasDataFrame:  Creates pandas data frame from _Header and
                              _Lines.


  I/o methods:
      createCSV: Creates the report's CSV file.

          asCSV: Create csv file from lines in Report instance.

      createCSV: Create csv from pandas data frame
              Input: _DataFrame: Pandas dataframe instance.


  Exceptions:
        NoReportNameProvided: Report instance call with invalid name

        NoOutputPathProvided: Path to directory for report is not provided

          NoFilenameProvided: No file name provided for report

           OutputPathInvalid: Path to directory for report invalid

   NoWriteAccessToOutputPath: Can not write into report directory

  WorkPackageInstanceInvalid: Instance of w/p for which report requested is 
                              invalid


Created on Wed 19Jun21. Version history:
----------------------------------------
 1.0: 02Jul21: First implementation
 1.1: 20Jun22: Fix reporting of total CG contingency.

@author: kennethlong
"""

import os
import copy
from datetime import date
from operator import itemgetter, attrgetter

import pandas as pnds
import numpy  as np

"""
         -------->  Base "Report" class  <--------
"""
class Report:
    __Debug   = False
    instances = []

    
#--------  "Built-in methods":
    def __init__(self, _Name=None, _ReportPath=None, _FileName=None,
                 _Header=[], _Lines=[]):

        Report.instances.append(self)
        
        if _Name == None:
            raise NoReportNameProvided( \
                  'No report name provided; execution termimated.')
        
        if _ReportPath != None:
            if _FileName   == None:
                raise NoFilenameProvided( \
                        'No CSV filename provided; execution termimated.')

            if not os.path.isdir(_ReportPath):
                raise OutputPathInvalid( \
                            'Output path:', _ReportPath, ' invalid')

            if not os.access(_ReportPath, os.W_OK):
                raise NoWriteAccessToOutputPath( \
                            'No write access to output path:', _ReportPath)
        else:
            _ReportPath, _FileName = os.path.split(_FileName)
            
        self._Name       = _Name
        self._ReportPath = _ReportPath
        self._FileName   = _FileName
        self._Header     = _Header
        self._Lines      = _Lines

        if self.getDebug():
            print(" Report.__init__ start:")
            print("     ----> Name:", _Name)
            print("     ----> Path:", _ReportPath)
            print("     ----> File:", _FileName)
            print("     ----> len(Header):", len(_Header))
            print("     ---->  len(Lines):", len(_Lines))

    def __repr__(self):
        return "Report(ReportName, PathToDirectory, ReportFile)"

    def __str__(self):
        print(" Report: Name: ", self._Name)
        print("     Output directory path: ", self._ReportPath)
        print("     Report file name: ", self._FileName)
        print("     Header fields:", self._Header)
        for i in range(len(self._Lines)):
            print("     ", self._Lines[i])
        return "     <---- Report __str__ done."


#--------  Processing methods
    def createPandasDataFrame(self):
        Data = []
        Data.append(self._Header)
        for i in range(len(self._Lines)):
            Line = self._Lines[i]
            if len(Line) < len(self._Header):
                for iPad in range(len(self._Header)-len(Line)):
                    Line.append("")
            Data.append(self._Lines[i])
        Dataframe = pnds.DataFrame(Data, \
                                   columns=self._Header)
        if self.__Debug:
            print(" Report; createPandasDataframe: \n", Dataframe)
        return Dataframe

    
#--------  Report:
    def asCSV(self):

        Data = []
        Data.append(self._Header)
        for i in range(len(self._Lines)):
            Data.append(self._Lines[i])
        if self.__Debug:
            print(Data)
        
        DataFrame = pnds.DataFrame(Data)
        if self.__Debug:
            print(DataFrame)
            
        if self._ReportPath != None:
            filename = os.path.join(self._ReportPath, self._FileName)
        else:
            filename = self._FileName
            
        if self.__Debug:
            print(filename)

        DataFrame.to_csv(filename, index=False, header=False)
        
    
#--------  I/o methods
    def createCSV(self, _DataFrame):
        _filename = os.path.join(self._ReportPath, self._FileName)
        _DataFrame.to_csv(_filename, index=False, header=False)


    def setDebug(self, Debug):
        self.__Debug = Debug

    def getDebug(self):
        return self.__Debug

