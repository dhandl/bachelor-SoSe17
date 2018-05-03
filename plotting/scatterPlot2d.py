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

wwwDir = "/project/etp5/aschwemmer/bachelor-SoSe17/plots/"
if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

fileName = "SR_350_200_amt2VsMt"

lumi = 36500.
cut = "( "+str(lumi)+" * weight * xs_weight * sf_total * weight_sherpa22_njets * weight_top_mass_reweighting * ( (xe_trigger) && (n_jet>=4) && (jet_pt[0]>25000) && (jet_pt[1]>25000) && (jet_pt[2]>25000) && (jet_pt[3]>25000) && (mt>30000) && (met>230e3) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (met>250000.0) && (dr_bjet_lep>0.7) && (ht>530000.0) ) )"

bkg=ROOT.TChain("powheg_ttbar_Nom")
bkg.Add("/afs/cern.ch/work/d/dboerner/public/SUSY_ntuples/powheg_ttbar/*")

sig=ROOT.TChain("stop_bWN_350_200_MET100_Nom")
sig.Add("/afs/cern.ch/work/d/dboerner/public/SUSY_ntuples/stop_bWN_350_200_MET100/*")
#c.Add("/afs/cern.ch/user/j/jkuechle/work/public/susy/ntuples_par/powheg_singletop/mc15_13TeV*")

bkgh=ROOT.TH2F("bkgh","bkgh",600,0,600,600,0,600)
bkg.Draw("amt2:mt*0.001>>bkgh",cut,"goff")
#if (bkgh.Integral()>0):
#  bkgh.Scale(1./bkgh.Integral())

sigh=ROOT.TH2F("sigh","sigh",600,0,600,600,0,600)
sig.Draw("amt2:mt*0.001>>sigh",cut,"goff")
#if (sigh.Integral()>0):
#  sigh.Scale(1./sigh.Integral())

c0 = ROOT.TCanvas("c0","c0",600,500)
c0.SetFillColor(10)
c0.SetBorderSize(1)
c0.SetLogz()
c0.SetGrid()
c0.SetRightMargin(0.15)
#c0.SetGridy()
#c0.SetGridx()

bkgh.SetLineColor(ROOT.kBlue)
bkgh.SetFillColor(ROOT.kBlue)
bkgh.SetMarkerColor(ROOT.kBlue)
bkgh.SetMarkerStyle(7)
sigh.SetLineColor(ROOT.kRed)
sigh.SetFillColor(ROOT.kRed)
sigh.SetMarkerStyle(7)
sigh.SetMarkerColor(ROOT.kRed)
bkgh.Draw("scat=1")
sigh.Draw("scat=1 same")
sigh.GetXaxis().SetTitle("m_{T} [GeV]")
sigh.GetYaxis().SetTitle("am_{T2} [GeV]")
#h.GetYaxis().SetTitle("am_{T2}")

#corr = h.GetCorrelationFactor()

ATLASLabel(0.18,0.9,"Work in progress")
ATLASLumiLabel(0.18,0.89,str(lumi*0.001))

text = ROOT.TLatex()
text.SetNDC()
text.SetTextSize(0.045)
text.SetTextAlign(11) 
#text.DrawLatex(0.1,0.04,"r = %.3f"%corr)
#text.DrawLatex(0.5,0.8,"m(#tilde{t},#tilde{#chi}_{1}^{0})_{3-body}=(%i,%i) GeV"%(sig[0],sig[1]))
#ROOT.myText(0.15,0.335,1,"Data 16, RN 297041")
#ROOT.myText(0.15,0.285,1,"#sqrt{s} = 13TeV")
#ROOT.myText(0.15,0.235,1,"Elec. Noise [MeV], EM1")

c0.SaveAs(wwwDir+fileName+".pdf")
c0.SaveAs(wwwDir+fileName+".root")
c0.SaveAs(wwwDir+fileName+".png")

