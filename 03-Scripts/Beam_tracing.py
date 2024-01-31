#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import Beam_tracer_code as Bt
import os
HOMEPATH = os.getenv('HOMEPATH')

beamline_file = 'DipoleTest.csv'
data_file     = 'DipoleTest.dat'



#We start with beamline plotting 

Bt.BeamlinePlotter.Tracer(0, 100, colour='b', label='20MeV', filename=data_file, facility = beamline_file, maxz = 0.1, HOMEPATH = HOMEPATH, NEvts = 10)
#Tr.BeamlinePlotter.Tracer(12.5, 13.5, colour='r', label='E=21MeV', filename=data_file, facility = beamline_file, maxz = 0.1, HOMEPATH = HOMEPATH, NEvts = 200)
#Tr.BeamlinePlotter.Tracer(17, 18, colour='r', label='E=11MeV', filename=data_file, facility = beamline_file, maxz = 2.135, HOMEPATH = HOMEPATH)

