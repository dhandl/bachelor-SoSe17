import ROOT
import math
import os, sys

#ROOT.gInterpreter.ExecuteMacro("~/MyRoot/rootlogon.C")
#ROOT.gROOT.LoadMacro("~/MyRoot/AtlasUtils.C");
#ROOT.gStyle.SetPalette(1)
#ROOT.gROOT.SetStyle("ATLAS")
#ROOT.gStyle.SetTextSize(0.04)

from AtlasStyle import *
SetAtlasStyle()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

ROOT.TGaxis().SetMaxDigits(4)

#wwwDir = ""
#if not os.path.exists(wwwDir):
#  os.makedirs(wwwDir)

fileName = "test"

cut = "( 35000. * weight * xs_weight * sf_total * weight_sherpa22_njets * ( (n_jet>=4) && (jet_pt[0]>25000) && (jet_pt[1]>25000) && (jet_pt[2]>25000) && (jet_pt[3]>25000) && (mt>30000) && (met>250e3) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (dr_bjet_lep>0.7) && (mt>130000.) ) )"

bkg=ROOT.TChain("powheg_ttbar_Nom")
bkg.Add("/afs/cern.ch/work/d/dboerner/public/SUSY_ntuples/powheg_ttbar/*")

sig=ROOT.TChain("stop_bWN_350_200_MET100_Nom")
sig.Add("/afs/cern.ch/work/d/dboerner/public/SUSY_ntuples/stop_bWN_350_200_MET100/*")

#c.Add("/afs/cern.ch/user/j/jkuechle/work/public/susy/ntuples_par/powheg_singletop/mc15_13TeV*")

bkgh=ROOT.TH1F("bkgh","bkgh",100,0,5000)
bkg.Draw("abs(((ht*0.001)-500)**2+(amt2-80)**2-120**2)>>bkgh",cut,"goff")

sigh=ROOT.TH1F("sigh","sigh",100,0,5000)
sig.Draw("abs(((ht*0.001)-500)**2+(amt2-80)**2-120**2)>>sigh",cut,"goff")

c0 = ROOT.TCanvas("c0","c0",600,500)
c0.SetFillColor(10)
c0.SetBorderSize(1)
c0.SetLogz()
c0.SetRightMargin(0.15)
#c0.SetGridy()
#c0.SetGridx()

bkgh.SetLineColor(ROOT.kBlue)
sigh.SetLineColor(ROOT.kRed)
bkgh.Draw("hist")
sigh.Draw("hist same")
#h.GetYaxis().SetTitle("m_{T}")
#h.GetYaxis().SetTitle("am_{T2}")
#h.GetXaxis().SetTitle("E_{T}^{miss}")

#corr = h.GetCorrelationFactor()

ATLASLabel(0.18,0.9,"Work in progress")
ATLASLumiLabel(0.18,0.89,"35")

text = ROOT.TLatex()
text.SetNDC()
text.SetTextSize(0.045)
text.SetTextAlign(11) 
#text.DrawLatex(0.1,0.04,"r = %.3f"%corr)
#text.DrawLatex(0.5,0.8,"m(#tilde{t},#tilde{#chi}_{1}^{0})_{3-body}=(%i,%i) GeV"%(sig[0],sig[1]))
#ROOT.myText(0.15,0.335,1,"Data 16, RN 297041")
#ROOT.myText(0.15,0.285,1,"#sqrt{s} = 13TeV")
#ROOT.myText(0.15,0.235,1,"Elec. Noise [MeV], EM1")

c0.SaveAs(fileName+".pdf")
c0.SaveAs(fileName+".root")
c0.SaveAs(fileName+".png")

