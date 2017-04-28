#!/usr/bin/env python
#------------------------------------------------------------------
#- File: analysis.py
#- Description: plot results of training with FBM
#  Created: 01-Jun-2013 INFN SOS 2013, Vietri sul Mare, Italy, HBP
#    adapt to CMSDAS 2015 Bari HBP
#           01-Jun-2016 HBP adapt again for Bari Lectures
#           09-Mar-2017 DESY 2017 Statistics School, Hamburg, Germany
#------------------------------------------------------------------
import os, sys
from histutil import *
from time import sleep
from ROOT import *
#------------------------------------------------------------------
def readAndFill(filename, treename, bnn, c, h, nn=-1):
    h.Reset()
    ntuple = Ntuple(filename, treename)
    for rownumber, event in enumerate(ntuple):
        if rownumber < 500: continue
        # evaluate discriminant
        if nn < 0:
            D = bnn(event.SO2tota,
                    event.alcohol,
                    event.sulfate,
                    event.SO2free)
        else:
            D = bnn(event.SO2tota,
                    event.alcohol,
                    event.sulfate,
                    event.SO2free,
                        nn, nn)
        h.Fill(D)
        if rownumber % 100 == 0:
            c.cd()
            h.Draw('hist')
            c.Update()
            gSystem.ProcessEvents()
            
    h.Scale(1.0/h.Integral())
#------------------------------------------------------------------
def main():
    # set up a standard graphics style	
    setStyle()

    treename    = "Analysis"
    sigfilename = 'goodwine.root'
    bkgfilename = 'badwine.root'

    # compile BNN
    gROOT.ProcessLine(open('wino.cpp').read())
    bnn = wino
    
    # ---------------------------------------------------------
    # plot distributions of D
    # ---------------------------------------------------------
    c1  = TCanvas("fig_wine_D", "", 10, 10, 500, 500)

    xbins= 25
    xmin = 0
    xmax = 1
        
    hs = mkhist1("hs", "#font[12]{D}(#font[12]{x})", "", xbins, xmin, xmax)
    hs.SetFillColor(kCyan+1)
    hs.SetFillStyle(3001)
    readAndFill(sigfilename, treename, bnn, c1, hs)

    hb = mkhist1("hb", "#font[12]{D}(#font[12]{x})", "", xbins, xmin, xmax)    
    hb.SetFillColor(kMagenta+1)
    hb.SetFillStyle(3001)
    readAndFill(bkgfilename, treename, bnn, c1, hb)

    c1.cd()
    hb.Draw('hist')
    hs.Draw("hist same")
    c1.Update()
    gSystem.ProcessEvents()
    c1.SaveAs(".png")

    # ---------------------------------------------------------
    # plot ROCs
    # ---------------------------------------------------------
    c2  = TCanvas("fig_wine_ROC", "", 200, 10, 500, 500)
    roc = TFile('fig_wine_ROC.root', 'recreate')
    option = 'ac'
    hroc = []
    for ii in xrange(0,100,2):
        print "NN %d" % ii
        readAndFill(sigfilename, treename, bnn, c1, hs, ii)
        readAndFill(bkgfilename, treename, bnn, c1, hb, ii)
        hroc.append(mkroc('h%3.3d' % ii, hs, hb))
        hroc[-1].SetLineStyle(2)
        hroc[-1].SetLineColor(kGreen+1)
        c2.cd()
        hroc[-1].Draw(option)
        option = 'c same'
        c2.Update()
        gSystem.ProcessEvents()

        # write to root file
        roc.cd()
        hroc[-1].Write()    
    roc.Close()    
    c2.SaveAs('.png')
    sleep(5)
#----------------------------------------------------------------------
try:
    main()
except KeyboardInterrupt:
    print "\nciao!"

