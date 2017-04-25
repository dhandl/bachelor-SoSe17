import ROOT
import math
import os, sys

from AtlasStyle import *
SetAtlasStyle()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

ROOT.TGaxis().SetMaxDigits(4)

wwwDir = "/afs/cern.ch/user/d/dhandl/www/Run2/SUSY/Stop1l/sigSyst/"
if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

fileName = "nominal_truth_bWN_SR_metVsAmt2"

cut = "( 36500. * weight * xs_weight * sf_total * weight_sherpa22_njets * ((stxe_trigger) && (n_jet>=4) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>130e3) && (met>300e3) && (amt2<110) && (dphi_met_lep<2.5) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) ) )"
truth_cut = "( 36500. * weight * xs_weight * ( (n_lep==1) && (lep_pt[0]>25e3) && (n_jet>=4) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>130e3) && (met>230e3) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4)))"

#c=ROOT.TChain("stop_bWN_350_230_MadSin_m1001L20_truth_Nom")
#c.Add("/afs/cern.ch/work/d/dhandl/public/Stop1L/syst_truth/stop_bWN_350_230_MadSin_m1001L20_truth/*")
c=ROOT.TChain("Nominal_350_230_Nom")
#c.Add("/eos/atlas/user/d/dboerner/stop_bWN_350_230_MadSpin_m1001L20/*")
c.Add("/afs/cern.ch/work/j/jmitrevs/public/bWN_syst/Nominal_350_230/*")

h=ROOT.TH2F("h","h",30,100,700,30,0,600)
c.Draw("amt2:met*0.001>>h",truth_cut,"goff")

c0 = ROOT.TCanvas("c0","c0",600,500)
c0.SetFillColor(10)
c0.SetBorderSize(1)
c0.SetLogz()
c0.SetRightMargin(0.15)
#c0.SetGridy()
#c0.SetGridx()

h.Draw("colz")
h.GetYaxis().SetTitle("am_{T2}")
#h.GetYaxis().SetTitle("#Delta#Phi(E_{T}^{miss},l)")
h.GetXaxis().SetTitle("E_{T}^{miss}")

corr = h.GetCorrelationFactor()

ATLASLabel(0.18,0.9,"Work in progress")
ATLASLumiLabel(0.18,0.89,"36.5")

text = ROOT.TLatex()
text.SetNDC()
text.SetTextSize(0.045)
text.SetTextAlign(11) 
text.DrawLatex(0.1,0.04,"r = %.3f"%corr)
#text.DrawLatex(0.5,0.8,"m(#tilde{t},#tilde{#chi}_{1}^{0})_{3-body}=(%i,%i) GeV"%(sig[0],sig[1]))
#ROOT.myText(0.15,0.335,1,"Data 16, RN 297041")
#ROOT.myText(0.15,0.285,1,"#sqrt{s} = 13TeV")
#ROOT.myText(0.15,0.235,1,"Elec. Noise [MeV], EM1")

c0.SaveAs(wwwDir+fileName+".pdf")
c0.SaveAs(wwwDir+fileName+".root")
c0.SaveAs(wwwDir+fileName+".png")

