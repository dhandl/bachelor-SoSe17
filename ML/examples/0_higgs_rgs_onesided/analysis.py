#!/usr/bin/env python
# ---------------------------------------------------------------------
#  File:        analysis.py
#  Description: Analyze the results of RGS and find the best cuts.
#               Definitions:
#                 1. A cut is a threshold on a single variable.
#                    e.g., x > xcut
#                 2. A cut-point is the AND of a sequence of cuts. This
#                    can be visualized as a point in the space of cuts.
#                 3. A box cut is a two-sided threshold.
#                    e.g., (x > xlow) and (x < xhigh)
#                 4. A ladder cut is the OR of cut-pooints.
# ---------------------------------------------------------------------
#  Created:     10-Jan-2015 Harrison B. Prosper and Sezen Sekmen
#               01-Mar-2017 DESY 2017 Statistics School, Hamburg, Germany
# ---------------------------------------------------------------------
import os, sys, re
from string import *
from rgsutil import *
from time import sleep
from ROOT import *
# ---------------------------------------------------------------------
def writeResults(filename, ntuple, variables,
                     bestrow, bestZ, totals):

    ntuple.read(bestrow)
    
    out = open(filename, 'w')
    
    record = "totals (before optimization)"
    out.write('%s\n' % record); print record
    
    record = "\tVBF: %10.3f +/- %-10.1f events" % (totals[0][0],
                                                   totals[0][1])
    out.write('%s\n' % record); print record

    record = "\tggF: %10.3f +/- %-10.1f events" % (totals[1][0],
                                                   totals[1][1])
    out.write('%s\n' % record); print record    

    record = "\tZZ:  %10.3f +/- %-10.1f events" % (totals[2][0],
                                                   totals[2][1])
    out.write('%s\n' % record); print record
                    
    record = "\nSezen Z = %10.3f" % bestZ
    out.write('%s\n' % record); print record
    
    bestcuts = {}

    for name, count in variables:    
        if name[0:5] in ['count', 'fract', 'cutpo']: continue
        var = ntuple(name)
        bestcuts[name] = var
        if type(var) == type(0.0):
            record = "\t\t%10s\t%10.2f" % (name, var)
            out.write('%s\n' % record); print record
        else:
            record = "\t\t%10s\t%10.2f\t%10.2f" % (name,
                                                    min(var[0], var[1]),
                                                    max(var[0], var[1]))
            out.write('%s\n' % record); print record            
    print
    out.write('\n')
    
    print "Yields and relative efficiencies"
    for name, count in variables:        
        if not (name[0:5] in ['count', 'fract']): continue
        var = ntuple(name)
        record = "\t%-30s %10.3f" % (name, var)
        out.write('%s\n' % record); print record                    
        if name[0:5] == "fract":
            print
            out.write('\n')
    out.close()
    return bestcuts

def plotData():

    msize = 0.15 # marker size

    xbins =   50
    xmin  =  0.0
    xmax  = 10.0

    ybins =    50
    ymin  =   0.0
    ymax  =5000.0    
    
    cmass = TCanvas("fig_example0", "VBF/ggF",
                    10, 10, 500, 500)    
    
    # -- background
    hb = mkhist2("hb",
                 "#Delta#font[12]{#eta_{jj}}",
                 "#font[12]{m_{jj}} (GeV)",
                 xbins, xmin, xmax,
                 ybins, ymin, ymax,
                 color=kMagenta+1)
    hb.Sumw2()
    hb.SetLineWidth(2)
    hb.GetYaxis().SetTitleOffset(1.80)
    
    bntuple = Ntuple('../public/ntuple_HZZ4L.root', 'Analysis')
    btotal  = 0.0
    total   = 0
    for ii, event in enumerate(bntuple):
        btotal += event.weight
        total  += 1
        hb.Fill(event.detajj, event.massjj, event.weight)
        if total % 100 == 0:
            cmass.cd()
            hb.Draw('box')
            cmass.Update()
            gSystem.ProcessEvents()
            
    # -- signal
    hs = mkhist2("hs",
                 "#Delta#font[12]{#eta_{jj}}",
                 "#font[12]{m_{jj}} (GeV)",
                 xbins, xmin, xmax,
                 ybins, ymin, ymax,
                 color=kCyan+1)
    hs.Sumw2()
    hs.SetLineWidth(2)
    hs.GetYaxis().SetTitleOffset(1.80)
    
    sntuple = Ntuple('../public/ntuple_HZZ4L_VBF.root', 'Analysis')
    stotal  = 0.0
    total   = 0
    for event in sntuple:
        stotal += event.weight
        total  += 1
        hs.Fill(event.detajj, event.massjj, event.weight)
        if total % 100 == 0:
            cmass.cd()
            hs.Draw('box')
            cmass.Update()
            gSystem.ProcessEvents()
            
    cmass.cd()
    hs.Draw('box')
    hb.Draw('box same')
    cmass.Update()
    gSystem.ProcessEvents()    
    return (cmass, hs, hb)
# ---------------------------------------------------------------------
def main():
    print "="*80
    print "\t=== Obtain Best One-Sided Cuts ==="
    print "="*80

    resultsfilename = "example0.root"
    treename = "RGS"
    print "\n\topen RGS file: %s"  % resultsfilename
    ntuple = Ntuple(resultsfilename, treename)
    
    variables = ntuple.variables()
    for name, count in variables:
        print "\t\t%-30s\t%5d" % (name, count)        
    print "\tnumber of cut-points: ", ntuple.size()
  
    # -------------------------------------------------------------
    # Plot results of RGS, that is, the fraction of events that
    # pass a given cut-point.
    #  1. Loop over cut points and compute a significance measure
    #     for each cut-point.
    #  2. Find cut-point with highest significance.
    # -------------------------------------------------------------
    # Set up a standard Root graphics style (see histutil.py in the
    # python directory).
    setStyle()

    cmass, hs, hb = plotData()

    
    # Create a 2-D histogram for ROC plot
    msize = 0.30  # marker size for points in ROC plot
    
    xbins =   50  # number of bins in x (background)
    xmin  =  0.0  # lower bound of x
    xmax  =  0.1  # upper bound of y

    ybins =   50
    ymin  =  0.0
    ymax  =  1.0

    color = kBlue+1
    hist  = mkhist2("hroc",
                    "#font[12]{#epsilon_{B}}",
                    "#font[12]{#epsilon_{S}}",
                    xbins, xmin, xmax,
                    ybins, ymin, ymax,
                    color=color)
    hist.SetMinimum(0)
    hist.SetMarkerSize(msize)


    # loop over all cut-points, compute a significance measure Z
    # for each cut-point, and find the cut-point with the highest
    # significance and the associated cuts.
    print "\tfilling ROC plot..."	
    bestZ = -1      # best Z value
    bestRow = -1    # row with best cut-point


    totals = ntuple.totals()
    print "\ntotals:"
    for ii, (total, etotal) in enumerate(totals):
        print "\ttotal[%d]: %10.3f +/- %-10.3f events" % (ii, total, etotal)
       
    ts, es  = totals[0]
    t1, et1 = totals[1]
    t2, et2 = totals[2]
    tb = t1 + t2
    for row, cuts in enumerate(ntuple):
        s  = cuts.count_VBF #  signal count
        b1 = cuts.count_ggF #  background 1
        b2 = cuts.count_ZZ  #  background 2
        b  = b1 + b2
        
        fs = s / ts
        fb = b / tb
                
        #  Plot fs vs fb
        hist.Fill(fb, fs)
        	
        # Compute measure of significance
        #   Z  = sign(LR) * sqrt(2*|LR|)
        # where LR = log(Poisson(s+b|s+b)/Poisson(s+b|b))
        Z = 0.0
        if b > 1:
            Z = 2*((s+b)*log((s+b)/b)-s)
            absZ = abs(Z)
            if absZ != 0:
                Z = Z*sqrt(absZ)/absZ                    
        if Z > bestZ:
            bestZ = Z
            bestrow = row

    # -------------------------------------------------------------            
    # Write out best cut
    # -------------------------------------------------------------
    bestcuts = writeResults('results_onesided.txt',
                                ntuple, variables,
                                bestrow, bestZ,
                                totals)
    
    # -------------------------------------------------------------
    # Save plots
    # -------------------------------------------------------------
    print "\t== plot ROC ==="	
    croc = TCanvas("fig_%s_ROC" % nameonly(resultsfilename),
                   "ROC", 520, 10, 500, 500)
    croc.cd()
    #croc.SetLogx()
    hist.Draw()
    croc.Update()
    gSystem.ProcessEvents()    


    print "\t=== plot one-sided cuts ==="
    
    xbins= hs.GetNbinsX()
    xmin = hs.GetXaxis().GetBinLowEdge(1)
    xmax = hs.GetXaxis().GetBinUpEdge(xbins)

    ybins= hs.GetNbinsY()
    ymin = hs.GetYaxis().GetBinLowEdge(1)
    ymax = hs.GetYaxis().GetBinUpEdge(ybins)

    xcut = array('d')
    xcut.append(bestcuts['detajj'])
    xcut.append(bestcuts['detajj'])
    xcut.append(xmax)

    ycut = array('d')
    ycut.append(ymax)
    ycut.append(bestcuts['massjj'])
    ycut.append(bestcuts['massjj'])
    hcut = TGraph(3, xcut, ycut)

    cmass.cd()
    hcut.Draw('same')
    cmass.Update()
    gSystem.ProcessEvents()    
    croc.SaveAs(".png")    
    cmass.SaveAs('.png')
    
    sleep(5)
# ---------------------------------------------------------------------
try:
    main()
except KeyboardInterrupt:
    print "bye!"


