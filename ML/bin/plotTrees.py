#!/usr/bin/env python
#------------------------------------------------------------------------------
# File: plotTrees.py
# Description: example of classification with TMVA
# Created: 31-May-2013 INFN SOS 2013, Salerno, Italy, HBP
#------------------------------------------------------------------------------
import os, sys
from ROOT import *
from math import *
from string import *
from time import sleep
from array import array
from histutil import *
#------------------------------------------------------------------------------
def main():
    #--------------------------------------------------------------------------    
    argv = sys.argv[1:]
    argc = len(argv)
    if argc < 1:
        sys.exit('''
    Usage:
        plotTrees.py BDT-class-filename [xmin,xmax] [ymin,ymax]
    ''')

    
    Cfilename = argv[0]
    if not os.path.exists(Cfilename):
        sys.exit('''
    ** can't open file %s
    ''' % Cfilename)
        
    # create a Python equivalent
    bdt = BDT(Cfilename)
    xtitle, ytitle = bdt.varnames()
    xlimit, ylimit = bdt.limits()
    
    if argc > 1:
        xmin, xmax = map(atof, split(argv[1], ','))
    else:
        xmin, xmax = xlimit

    if argc > 2:
        ymin, ymax = map(atof, split(argv[2], ','))
    else:
        ymin, ymax = ylimit        

    #--------------------------------------------------------------------------            
    setStyle()
    pixels = 220
    c = TCanvas('fig_6trees', 'trees', 10, 10, 3*pixels, 2*pixels)
    c.Divide(3,2)
    h = []
    for ii in xrange(6):
        h.append(bdt.plot(ii, 'htree', xtitle, ytitle,
                              xmin, xmax, ymin, ymax))
        c.cd(ii+1)
        h[-1].Draw('col')
        c.Update()
        gSystem.ProcessEvents()
        bdt.printTree(ii, [xtitle, ytitle])
    c.SaveAs(".png")
    c.SaveAs(".gif")
    sleep(2)

    #--------------------------------------------------------------------------    
    # Draw 2D plot with increasing numbers of trees
    c1 = TCanvas('fig_forest', 'trees', 10, 10, 3*pixels, 2*pixels)
    c1.Divide(3,2)
    nx = 50
    ny = 50
    xstep = (xmax-xmin) / nx
    ystep = (ymax-ymin) / ny
    ntrees = [6, 50, 100, 250, 500, 1000]

    hh = []
    for ii in xrange(6):
        hname = "h%4.4d" % ntrees[ii]
        hh.append(mkhist2(hname, xtitle, ytitle, nx,
                              xmin, xmax, ny, ymin, ymax))
        for ix in xrange(nx):
            x = xmin + ix * xstep
            for iy in xrange(ny):
                y = ymin + iy * ystep
                z = bdt((x,y), ntrees[ii])
                hh[-1].Fill(x, y, z)
        c1.cd(ii+1)
        hh[-1].Draw('col')
        addTitle('%5d trees' % ntrees[ii], 0.06)
        c1.Update()
        gSystem.ProcessEvents()
    c1.SaveAs(".png")
    c1.SaveAs('.gif')
    sleep(5)
    
    ## os.system('rm -rf fig_manytrees.gif')
    ## c1 = TCanvas('fig_manytrees', 'many trees', 610, 310, 2*pixels, 2*pixels)

    ## option = 'col'
    ## for ii in xrange(100):
    ##     print ii
    ##     h.append(bdt.plot(ii, 'hmtree', 'm_{Z_{1}} (GeV)', 'm_{Z_{2}} (GeV)', 0, xmax, 0, ymax))
    ##     h[-1].Draw('col')
    ##     c1.Update()
    ##     c1.Print('fig_manytrees.gif+10')
#------------------------------------------------------------------------------
try:
    main()
except KeyboardInterrupt:
    print "\nciao"
