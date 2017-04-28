#!/usr/bin/env python
# -----------------------------------------------------------------------------
#  File:        train.py
#  Description: Example of Random Grid Search to find the results of an
#               ensemble cuts. 
#  Created:     10-Jan-2015 Harrison B. Prosper and Sezen Sekmen
#               01-Mar-2017 DESY 2017 Statistics School, Hamburg, Germany
# -----------------------------------------------------------------------------
import os, sys, re
from rgsutil import *
from string import *
from ROOT import *
# -----------------------------------------------------------------------------
def main():
    print "="*80
    print "\t=== Box Cuts ==="
    print "="*80

    # ---------------------------------------------------------------------
    # Load the RGS shared library and check that the various input files
    # exist.
    # ---------------------------------------------------------------------
    gSystem.AddDynamicPath('%s/lib' % os.environ['RGS_PATH'])
    if gSystem.Load("libRGS") < 0:
        error("unable to load libRGS")

    # Name of file containing cut definitions
    # Format of file:
    #   variable-name  cut-type (>, <, <>, |>, |<, ==)
    varfilename = "example1.cuts"
    if not os.path.exists(varfilename):
        error("unable to open variables file %s" % varfilename)

    # Name of signal file
    sigfilename = "../public/ntuple_HZZ4L_VBF.root"
    if not os.path.exists(sigfilename):
        error("unable to open signal file %s" % sigfilename)

    # Name of background file        
    bkgfilename1 = "../public/ntuple_HZZ4L.root"
    if not os.path.exists(bkgfilename1):
        error("unable to open background file %s" % bkgfilename1)

    # Name of background file        
    bkgfilename2 = "../public/ntuple_ZZ4L.root"
    if not os.path.exists(bkgfilename2):
        error("unable to open background file %s" % bkgfilename2)        

    # ---------------------------------------------------------------------
    #  Create RGS object
    #  
    #   The file (cutdatafilename) of cut-points is usually a signal file,
    #   which ideally differs from the signal file on which the RGS
    #   algorithm is run.
    # ---------------------------------------------------------------------
    cutdatafilename = sigfilename
    start      = 0           # start row 
    maxcuts    = 5000        # maximum number of cut-points to consider
    treename   = "Analysis"  # name of Root tree 
    weightname = "weight"    # name of event weight variable
    
    rgs = RGS(cutdatafilename, start, maxcuts, treename, weightname)

    # ---------------------------------------------------------------------
    #  Add signal and background data to RGS object.
    #  Weight each event using the value in the field weightname, if
    #  present.
    #  NB: We asssume all files are of the same format.
    # ---------------------------------------------------------------------
    start    = 0   #  start row
    numrows  =-1   #  scan all the data from the files
    Lumi     = 100 #  1/fb
    # The last (optional) argument is a string, which, if given, will be
    # appended to the "count" and "fraction" variables. The "count" variable
    # contains the number of events that pass per cut-point, while "fraction"
    # is count / total, where total is the total number of events per file.
    # If no string is given, the default is to append an integer to the
    # "count" and "fraction" variables, starting at 0, in the order in which
    # the files are added to the RGS object.
    rgs.add(sigfilename,  start, numrows, "_VBF", Lumi)
    rgs.add(bkgfilename1, start, numrows, "_ggF", Lumi)
    rgs.add(bkgfilename2, start, numrows, "_ZZ",  Lumi)

    # ---------------------------------------------------------------------	
    #  Run RGS and write out results
    # ---------------------------------------------------------------------	    
    rgs.run(varfilename)

    # Write to a root file
    rgsfilename = "%s.root" % nameonly(varfilename)
    rgs.save(rgsfilename)

    # Write to a text file
    rgsfilename = "%s.txt" % nameonly(varfilename)
    rgs.save(rgsfilename)    
# -----------------------------------------------------------------------------
try:
    main()
except KeyboardInterrupt:
    print "\tciao!\n"



