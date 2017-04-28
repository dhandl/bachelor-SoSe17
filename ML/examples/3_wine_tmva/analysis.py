#!/usr/bin/env python
#------------------------------------------------------------------
# File: analysis.py
# Description: make some plots etc.
# Created: 01-Jun-2013 INFN SOS 2013, Vietri sul Mare, Italy, HBP
#          01-Mar-2017 DESY 2017 Statistics School, Hamburg, Germany 
#------------------------------------------------------------------
import os, sys
from ROOT import *
from histutil import *
from time import sleep
#------------------------------------------------------------------
def readAndFill(filename, treename, h):
    # open ntuple (see histutil.py for implementation)
    ntuple = Ntuple(filename, treename)
    
    for rownumber, event in enumerate(ntuple):
        h.Fill(event.Z1mass, event.Z2mass, event.weight)
        if rownumber % 5000 == 0:
            print rownumber
    h.Scale(1.0/h.Integral())
#------------------------------------------------------------------
def readAndFillAgain(filename, treename, bdt, c, h):

    ntuple = Ntuple(filename, treename)
    inputs = vector('double')(2)

    for rownumber, event in enumerate(ntuple):

        inputs[0], inputs[1] = event.Z1mass, event.Z2mass
        D = bdt.GetMvaValue(inputs)
        h.Fill(D, event.weight)

        if rownumber % 5000 == 0:
            c.cd()
            h.Draw('hist')
            c.Update()
            gSystem.ProcessEvents()
            
    h.Scale(1.0/h.Integral())
#------------------------------------------------------------------
def main():

    setStyle()

    XNBINS= 30
    XMIN  =  0
    XMAX  =150

    YNBINS= 30
    YMIN  =  0
    YMAX  =150

    nx = 2
    ny = 2
    pixels = 250

    which  = 'BDT'

    treename = "Analysis"
    
    # ---------------------------------------------------------
    # make 2-D plot
    # ---------------------------------------------------------

    c  = TCanvas("fig_Z1massZ2mass_%s" % which, "",
                     10, 10, nx*pixels, ny*pixels)
    # divide canvas canvas along x-axis
    c.Divide(nx, ny)



    # Fill signal histogram
    sfilename = '../public/ntuple_HZZ4L.root'
    hsig = mkhist2('hsig', "m_{Z1} (GeV)", "m_{Z2} (GeV)",
                       XNBINS, XMIN, XMAX,
                       YNBINS, YMIN, YMAX)
    hsig.SetLineColor(kCyan+1)            
    readAndFill(sfilename, treename, hsig)

    # Fill background histogram
    bfilename = '../public/ntuple_ZZ4L.root'
    hbkg = mkhist2('hbkg', "m_{Z1} (GeV)", "m_{Z2}",
                       XNBINS, XMIN, XMAX,
                       YNBINS, YMIN, YMAX)
    hbkg.SetLineColor(kMagenta+1)        
    readAndFill(bfilename, treename, hbkg)

    # plot 2-D histogram
    c.cd(1)

    hsig.SetMinimum(0)
    hsig.Draw('box')

    xpos = 0.45
    ypos = 0.85
    tsize= 0.05
    s1 = Scribe(xpos, ypos, tsize)
    s1.write('pp #rightarrow H #rightarrow ZZ #rightarrow 4l')
    c.Update()
    gSystem.ProcessEvents()
    
    c.cd(2)
    hbkg.Draw('box')
    s2 = Scribe(xpos, ypos, tsize)
    s2.write('pp #rightarrow ZZ #rightarrow 4l')
    c.Update()        
    gSystem.ProcessEvents()
    
    hD = hsig.Clone('hD')
    hSum = hsig.Clone('hSum')
    hSum.Add(hbkg)
    hD.Divide(hSum)
    hD.SetMinimum(0)
    hD.SetMaximum(1)

    c.cd(3)
    hD.Draw('cont1')
    s3 = Scribe(xpos, ypos, tsize)
    s3.write('D(m_{Z_{1}}, m_{Z_{2}}) (actual)')
    c.Update()
    gSystem.ProcessEvents()
    
    # ---------------------------------------------------------
    # load discriminant
    # ---------------------------------------------------------
    Cfilename = 'results/weights/Z1massZ2mass_%s.class.C' % which
    gROOT.ProcessLine('.L %s' % Cfilename)
    names = vector('string')()
    inputs= vector('double')(2)
    names.push_back('Z1mass')
    names.push_back('Z2mass')
    bdt = ReadBDT(names)

    # ---------------------------------------------------------
    # make 2-D plot of discriminant
    # ---------------------------------------------------------    
    h1 = mkhist2("h1", "m_{Z1} (GeV)", "m_{Z2}",
                XNBINS, XMIN, XMAX, YNBINS, YMIN, YMAX)
    h1.SetMinimum(0)

    xstep = (XMAX-XMIN)/XNBINS
    ystep = (YMAX-YMIN)/YNBINS

    for i in xrange(XNBINS):
        x = XMIN + (i+0.5)*xstep
        inputs[0] = x
        for j in xrange(YNBINS):
            y = YMIN + (j+0.5)*ystep
            inputs[1] = y
            D = bdt.GetMvaValue(inputs)
            h1.Fill(x, y, D)

        c.cd(4)
        h1.Draw('cont1')
        s4 = Scribe(xpos, ypos, tsize)
        s4.write('D(m_{Z_{1}}, m_{Z_{2}}) (%s)' % which)
        c.Update()
        gSystem.ProcessEvents()
        
    c.SaveAs(".gif")
    c.SaveAs(".png")

    # ---------------------------------------------------------
    # plot distributions of D
    # ---------------------------------------------------------
    c1  = TCanvas("fig_Z1massZ2mass_D_%s" % which, "",
                      510, 310, 500, 500)

    hs = mkhist1("hs", "D(m_{Z1}, m_{Z2})", "", 50, -1, 1)
    hs.SetFillColor(kCyan+1)
    hs.SetFillStyle(3001)
    readAndFillAgain(sfilename, treename, bdt, c1, hs)
    sleep(1)

    hb = mkhist1("hb", "D(m_{Z1}, m_{Z2})", "", 50, -1, 1)
    hb.SetFillColor(kMagenta+1)
    hb.SetFillStyle(3001)
    readAndFillAgain(bfilename, treename, bdt, c1, hb)

    c1.cd()
    hb.Draw('hist')
    hs.Draw("hist same")
    c1.Update()
    gSystem.ProcessEvents()
    
    c1.SaveAs(".gif")
    c1.SaveAs(".png")
    #gApplication.Run()
    sleep(10)
#----------------------------------------------------------------------
try:
    main()
except KeyboardInterrupt:
    print '\nciao!'

