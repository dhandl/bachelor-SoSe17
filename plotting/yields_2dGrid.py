import ROOT
from math import *
import os, sys
from array import array

#ROOT.gInterpreter.ExecuteMacro("~/MyRoot/rootlogon.C")
#ROOT.gROOT.LoadMacro("~/MyRoot/AtlasUtils.C");
#ROOT.gStyle.SetPalette(1)
#ROOT.gROOT.SetStyle("ATLAS")
#ROOT.gStyle.SetTextSize(0.04)

from AtlasStyle import *
SetAtlasStyle()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPaintTextFormat("4.1f")
ROOT.TGaxis().SetMaxDigits(4)

wwwDir = "/afs/cern.ch/user/d/dhandl/www/Run2/SUSY/Stop1l/2dPlots/ShapeFit/"
if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

fileName = "yieldsGrid_metVsamt2"

amt2Binning = [80, 90, 110, 130, 170, 250]
metBinning = [230, 300, 450, 550]

cut = "( 36500. * weight * xs_weight * sf_total * weight_sherpa22_njets * ( (n_jet>=4) && (jet_pt[0]>50000) && (jet_pt[1]>25000) && (jet_pt[2]>25000) && (jet_pt[3]>25000) && (mt>130000) && (met>230e3) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (dphi_met_lep<2.5) ) )"

ttbar=ROOT.TChain("powheg_ttbar_Nom")
ttbar.Add("/eos/atlas/user/d/dboerner/powheg_ttbar/mc15_13TeV*")
h_ttbar=ROOT.TH2F("h_ttbar","h_ttbar",len(metBinning)-1,array('d',metBinning),len(amt2Binning)-1,array('d',amt2Binning))
ttbar.Draw("amt2:met*0.001>>h_ttbar",cut,"goff")
hist = h_ttbar.Clone()

singletop=ROOT.TChain("powheg_singletop_Nom")
singletop.Add("/eos/atlas/user/d/dboerner/powheg_singletop/mc15_13TeV*")
h_singletop=ROOT.TH2F("h_singletop","h_singletop",len(metBinning)-1,array('d',metBinning),len(amt2Binning)-1,array('d',amt2Binning))
singletop.Draw("amt2:met*0.001>>h_singletop",cut,"goff")
hist.Add(h_singletop)

wjets=ROOT.TChain("sherpa22_Wjets_Nom")
wjets.Add("/eos/atlas/user/d/dboerner/sherpa22_Wjets/mc15_13TeV*")
h_wjets=ROOT.TH2F("h_wjets","h_wjets",len(metBinning)-1,array('d',metBinning),len(amt2Binning)-1,array('d',amt2Binning))
wjets.Draw("amt2:met*0.001>>h_wjets",cut,"goff")
hist.Add(h_wjets)

diboson=ROOT.TChain("sherpa_diboson_Nom")
diboson.Add("/eos/atlas/user/d/dboerner/sherpa_diboson/mc15_13TeV*")
h_diboson=ROOT.TH2F("h_diboson","h_diboson",len(metBinning)-1,array('d',metBinning),len(amt2Binning)-1,array('d',amt2Binning))
diboson.Draw("amt2:met*0.001>>h_diboson",cut,"goff")
hist.Add(h_diboson)

ttV=ROOT.TChain("madgraph_ttV_Nom")
ttV.Add("/eos/atlas/user/d/dboerner/madgraph_ttV/mc15_13TeV*")
h_ttV=ROOT.TH2F("h_ttV","h_ttV",len(metBinning)-1,array('d',metBinning),len(amt2Binning)-1,array('d',amt2Binning))
ttV.Draw("amt2:met*0.001>>h_ttV",cut,"goff")
hist.Add(h_ttV)

bWN=ROOT.TChain("stop_bWN_350_200_m1001L20_Nom")
bWN.Add("/afs/cern.ch/work/d/dhandl/public/Stop1L/default_moriond17/stop_bWN_350_200_m1001L20/mc15_13TeV*")
h_bWN=ROOT.TH2F("h_bWN","h_bWN",len(metBinning)-1,array('d',metBinning),len(amt2Binning)-1,array('d',amt2Binning))
bWN.Draw("amt2:met*0.001>>h_bWN",cut,"goff")

nbinsX = len(metBinning)-1
nbinsY = len(amt2Binning)-1
for x in range(nbinsX):
  hist.SetBinContent(x, nbinsY , hist.GetBinContent(x,nbinsY) + hist.GetBinContent(x, nbinsY + 1))
  hist.SetBinError(x, nbinsY , sqrt(hist.GetBinError(x, nbinsY)**2 + hist.GetBinError(x, nbinsY + 1)**2))
  h_bWN.SetBinContent(x, nbinsY , h_bWN.GetBinContent(x,nbinsY) + h_bWN.GetBinContent(x, nbinsY + 1))
  h_bWN.SetBinError(x, nbinsY , sqrt(h_bWN.GetBinError(x, nbinsY)**2 + h_bWN.GetBinError(x, nbinsY + 1)**2))


for y in range(nbinsY):
  hist.SetBinContent(nbinsX, y , hist.GetBinContent(nbinsX, y) + hist.GetBinContent(nbinsX + 1, y))
  hist.SetBinError(nbinsX, y , sqrt(hist.GetBinError(nbinsX, y)**2 + hist.GetBinError(nbinsX + 1, y)**2))
  h_bWN.SetBinContent(nbinsX, y , h_bWN.GetBinContent(nbinsX, y) + h_bWN.GetBinContent(nbinsX + 1, y))
  h_bWN.SetBinError(nbinsX, y , sqrt(h_bWN.GetBinError(nbinsX, y)**2 + h_bWN.GetBinError(nbinsX + 1, y)**2))


#h=ROOT.TH2F("h","h",len(metBinning)-1,array('d',metBinning),len(amt2Binning)-1,array('d',amt2Binning))
#c.Draw("mt*0.001:met*0.001>>h",cut,"goff")

c0 = ROOT.TCanvas("c0","c0",600,500)
c0.SetFillColor(10)
c0.SetBorderSize(1)
#c0.SetLogz()
c0.SetRightMargin(0.15)
#c0.SetGridy()
#c0.SetGridx()

hist.SetMarkerSize(1.6)
h_bWN.SetMarkerSize(1.6)
h_bWN.SetMarkerColor(2)
hist.SetBarOffset(0.2)
hist.Draw("same TEXT")
hist.GetYaxis().SetTitle("am_{T2}")
hist.GetXaxis().SetTitle("E_{T}^{miss}")
h_bWN.SetBarOffset(-0.2)
h_bWN.Draw("same TEXT")
#h.GetYaxis().SetTitle("am_{T2}")

#for x in range(nbinsX):
l = ROOT.TLine(metBinning[1], amt2Binning[0], metBinning[1], amt2Binning[nbinsY])
l.SetLineStyle(ROOT.kDashed)
l.Draw()
l1 = ROOT.TLine(metBinning[2], amt2Binning[0], metBinning[2], amt2Binning[nbinsY])
l1.SetLineStyle(ROOT.kDashed)
l1.Draw()

#for y in range(nbinsY):
l2 = ROOT.TLine(metBinning[0], amt2Binning[1], metBinning[nbinsX], amt2Binning[1])
l2.SetLineStyle(ROOT.kDashed)
l2.Draw()
l3 = ROOT.TLine(metBinning[0], amt2Binning[2], metBinning[nbinsX], amt2Binning[2])
l3.SetLineStyle(ROOT.kDashed)
l3.Draw()
l4 = ROOT.TLine(metBinning[0], amt2Binning[3], metBinning[nbinsX], amt2Binning[3])
l4.SetLineStyle(ROOT.kDashed)
l4.Draw()
l5 = ROOT.TLine(metBinning[0], amt2Binning[4], metBinning[nbinsX], amt2Binning[4])
l5.SetLineStyle(ROOT.kDashed)
l5.Draw()

#corr = h.GetCorrelationFactor()

ATLASLabel(0.18,0.9,"Work in progress")
ATLASLumiLabel(0.18,0.89,"35")

#text = ROOT.TLatex()
#text.SetNDC()
#text.SetTextSize(0.045)
#text.SetTextAlign(11) 
#text.DrawLatex(0.1,0.04,"r = %.3f"%corr)
##text.DrawLatex(0.5,0.8,"m(#tilde{t},#tilde{#chi}_{1}^{0})_{3-body}=(%i,%i) GeV"%(sig[0],sig[1]))
#ROOT.myText(0.15,0.335,1,"Data 16, RN 297041")
#ROOT.myText(0.15,0.285,1,"#sqrt{s} = 13TeV")
#ROOT.myText(0.15,0.235,1,"Elec. Noise [MeV], EM1")

c0.SaveAs(wwwDir+fileName+".pdf")
c0.SaveAs(wwwDir+fileName+".root")
c0.SaveAs(wwwDir+fileName+".png")

