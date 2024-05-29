# LhARAlinearOptics
Linear optics code for LhARA -- Tag1

The code in this repository provides linear beam-line optics code and implemetations of the DRACO, LION< and LhARA Stage 1 beamlines.  

## To set up and run:
A guide to setting up and running the package is given in 00-Documentation/00-Setup-n-run/Setup-n-run.pdf.

Execute "startup.bash" from this directory (i.e. run the bash command "source startup.bash").  This will:
  * Set up "LhARAOpticsPATH"; and
  * Add "01-Code" to the PYTHONPATH.  The scripts in "02-Tests" may then be run with the command "python 02-Tests/<filename>.py".

## Directories:
 * Python classes and "library" code stored in "01-Code"
 * Test scripts stored in "02-Tests"
 * Parameters to control the run conditions are stored in "11-Parameters"
 * Example scripts are provided in "03-Scripts"
 * An example user directory is provided in 31-UserDirectory

Rudimentary, but, goal is one test script per class/package file in 01-Code.

## Dependencies:
 * Code and test scripts assume Python 3.  
 * Test scripts assume code directory (01-Code) is in PYTHON path.  A bash script "startup.bash" is provided to update the PYTHON path.

## History
 * January 2024:  Code tidied for "users"/co-developers!

## Updating to new install and set-up -- read this:
 * git clone git@github.com:ImperialCollegeLondon/LhARAlinearOptics.git
 * cd LhARAlineaOptics
 * Set up a virtual environment.  Possible commands:
   - python3 -m venv venv
   - virtualenv venv <br />
   
   Note that you may need to install the virtualenv package for your linux
   distribution.
 * source ./venv/bin/activate
 * pip install -r ./requirements.txt

To execute code from this, the source, directory tree execute:
 * source setup.bash                

## User environment:

Utilities are provided to allow users to use the package and to develop their own analyses.  To set this up:

 * Copy 31-UserDirectory/UserDirectory.tar.gz to your local directory;
 * Unpack the files using:
   * gunzip UserDirectory.tar.gz
   * tar xvf UserDirectort.tar
 * Set-up the environment variables by executing:
  * source setup.bash -p <path to LhARAlinearOptics>
 * Commands from the repository can now be run using:
  * $LhARAopticsPATH/03-Scripts/...
  Scrtipts in the 03-Scripts directory run "standalone" or print a hint on how they are to be run if they are executed without input arguments.
 * A couple of tips:
  * $LhARAopticsPATH/03-Scripts/runBeamSim.py -- runs simulation of particular beam configuration.  Reference configuration files are stored in $LhARAopticsPATH/11-Parameters
  * $LhARAopticsPATH/03-Scripts/readBeamSim.py -- reads simulation file and produces phase space plots in 99-Scratch
  * $LhARAopticsPATH/03-Scripts/plotBeam.py -- plots the beam envelopes by calculating the covariance matrix at the end of each beam-line element
  * $LhARAopticsPATH/03-Scripts/plotextrapolatedBeam -- makes teh same beam-envelope plots, but, propagates the covariance matrices starting from a given location
  * 

