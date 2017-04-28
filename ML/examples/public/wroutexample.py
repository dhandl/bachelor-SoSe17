#!/usr/bin/env python
# ---------------------
# write out data from and ntuple to a
# text file
# --------------------------------------
import os, sys, re
from histutil import *

def main():
    # give name of ntuple and name of tree within it
    filename = '../public/ntuple_HZZ4L.root'
    treename = 'Analysis'
    MAXROWS  = 1000

    # open ntuple object
    ntuple   = Ntuple(filename, treename)

    # open an empty text file in write mode
    outputfilename = 'example.txt'
    out = open(outputfilename, 'w')

    # define which variables are to be written out
    # Note use of triple quotes
    names = '''
    l2pt
    l2eta
    l2phi
    '''
    # convert to a list
    names = map(strip, split(strip(names),'\n'))
    print names

    # write header
    fmt = '%12s'*len(names)
    record = fmt % tuple(names)
    out.write('%s\n' % record)
    print record

    # loop over rows of ntuple
    for rownumber, event in enumerate(ntuple):
        # loop over variable names to be written out
        record = ''
        for name in names:
            # get value of current variable
            x = eval('event.%s' % name)
            record += '%12.3e' % x
        # write out record
        print record
        out.write('%s\n' % record)
        # break out of loop is maximum number of rows
        # has been reached.
        if rownumber > MAXROWS:
            break
    # close text file
    out.close()

try:
    main()
except KeyboardInterrupt:
    print "\ntschuess"

