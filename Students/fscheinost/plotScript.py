#!usr/bin/python2

import ROOT
import copy, os, sys
import helpers

from AtlasStyle import * 
from math import *
from array import array

SetAtlasStyle()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.TGaxis().SetMaxDigits(3)

def doRatio(hist1,hist2,Xtitle='',Ytitle='1/Default'):
  h1=hist1.Clone()
  h2=hist2.Clone()
  h1.Sumw2()
  h2.Sumw2()
  #h1.Scale(1./h1.Integral())
  #h2.Scale(1./h2.Integral())
  h1.Divide(h2)

  h1.SetMinimum(0.0)
  h1.SetMaximum(5.5)
  h1.SetStats(0)
  #h1.SetLineColor(hist1.GetLineColor())
  #h1.SetLineStyle(1)
  #h1.SetLineWidth(1)
  h1.GetXaxis().SetTitle(Xtitle)
  h1.GetYaxis().SetTitle(Ytitle)
  h1.GetYaxis().SetNdivisions(505)
  h1.GetYaxis().SetTitleSize(23)
  h1.GetYaxis().SetTitleFont(43)
  h1.GetYaxis().SetTitleOffset(1.8)
  h1.GetYaxis().SetLabelFont(43)
  h1.GetYaxis().SetLabelSize(20)
  h1.GetYaxis().SetLabelOffset(0.015)
  h1.GetXaxis().SetNdivisions(510)
  h1.GetXaxis().SetTitleSize(23)
  h1.GetXaxis().SetTitleFont(43)
  h1.GetXaxis().SetTitleOffset(3.4)
  h1.GetXaxis().SetLabelFont(43)
  h1.GetXaxis().SetLabelSize(20)
  h1.GetXaxis().SetLabelOffset(0.04)
  return h1


wwwDir = "/afs/cern.ch/user/d/dhandl/www/Run2/SUSY/Stop1l/shapeFit/"
if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

fileName = "bWN_multiBin_stack"

# setup input directories for TChains
bkgDir = "/eos/atlas/user/d/dboerner/" 
sigDir = "/afs/cern.ch/work/d/dhandl/public/Stop1L/default_moriond17/" 

TIGHTE = "( (n_el>0) || Alt$(mu_idMedium,0) )"

lumi = 36500.
weight = str(lumi)+" * weight * xs_weight * sf_total * weight_sherpa22_njets" 
cut = "(stxe_trigger) && (n_jet>=4) && (jet_pt[0]>50000) && (jet_pt[1]>25000) && (jet_pt[2]>25000) && (jet_pt[3]>25000) && (mt>130000) && (met>300e3) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (dphi_met_lep<2.5) && " + TIGHTE

#----------------------------#
normalized = False
if normalized:
  normString = "_norm"
else:
  normString = ""
#----------------------------#
setLogY = False
#setLogY = True
if setLogY:
  logString = "_logScale"
else:
  logString = ""
#----------------------------#
setRatioPlot = False 

allBkg = [
  {"name":"ttv", "legendName":"t#bar{t}+V", "target":bkgDir+"madgraph_ttV/*", "color": ROOT.TColor.GetColor("#E67067"), "chain_name":"madgraph_ttV_Nom"}, 
  {"name":"diboson", "legendName":"Diboson", "target":bkgDir+"sherpa_diboson/*", "color": ROOT.TColor.GetColor("#54C571"), "chain_name":"sherpa_diboson_Nom"}, 
  {"name":"singletop", "legendName":"Single top", "target":bkgDir+"powheg_singletop/*", "color": ROOT.TColor.GetColor("#82DE68"), "chain_name":"powheg_singletop_Nom"}, 
  {"name":"wjets", "legendName":"W+jets", "target":bkgDir+"sherpa22_Wjets/*", "color": ROOT.TColor.GetColor("#FCDD5D"), "chain_name":"sherpa22_Wjets_Nom"}, 
  {"name":"ttbar1L", "legendName":"t#bar{t} 1L", "target":bkgDir+"powheg_ttbar/*", "color":ROOT.TColor.GetColor("#0F75DB"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==1 || tt_cat==4 || tt_cat==7 )" },
  {"name":"ttbar2L", "legendName":"t#bar{t} 2L", "target":bkgDir+"powheg_ttbar/*", "color":ROOT.TColor.GetColor("#A5C6E8"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==0 || tt_cat==3 || tt_cat==6 )" },
  {"name":"ttbar1L1tau", "legendName":"t#bar{t} 1L1#tau", "target":bkgDir+"powheg_ttbar/*", "color": ROOT.TColor.GetColor("#5E9AD6"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==2 || tt_cat == 5 ) "}, 
]

allSignal = [
  {"name":"stop_bWN_350_200", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(350,200)", "target":sigDir+"stop_bWN_350_200_m1001L20/*", "color": ROOT.TColor.GetColor(ROOT.kBlue+2), "chain_name":"stop_bWN_350_200_m1001L20_Nom"},
]

for i, sample in enumerate(allBkg+allSignal):
  sample["chain"] = ROOT.TChain(sample["chain_name"])
  sample["chain"].Add(sample["target"])

allVariables = []
amt2 = {'name':'myAmt2', "fileName":fileName+"_amt2"+normString+logString, 'varStr':"amt2", 'Xtitle':'am_{T2}', 'Ytitle':'Events', 'binning':[50,80,90,100,110,130,150,170,250,350,600], "binningIsExplicit":True}
#amt2 = {'name':'myAmt2', "fileName":fileName+"_amt2"+normString+logString, 'varStr':"amt2", 'Xtitle':'am_{T2}', 'Ytitle':'Events', 'binning':[30,0,600], "binningIsExplicit":False}

allVariables.append(amt2)

histos = {}

for sample in allBkg+allSignal:
  histos[sample['name']] = {}
  for var in allVariables:
    if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
      histos[sample["name"]][var["name"]] = ROOT.TH1F(sample["name"]+"_"+var["name"], sample["name"]+"_"+var["name"], len(var['binning'])-1, array('d', var['binning']))
    else:
      histos[sample["name"]][var["name"]] = ROOT.TH1F(sample["name"]+"_"+var["name"], sample["name"]+"_"+var["name"],*var["binning"])
    if sample.has_key("addCut"):
      cutString = cut+" && "+sample["addCut"]
    else:
      cutString = cut
    sample["chain"].Draw(var["varStr"]+">>"+histos[sample["name"]][var["name"]].GetName(), "("+weight+") * ("+cutString+")","goff")
      
for var in allVariables:
  canv = ROOT.TCanvas(var['name']+'_Window',var['name']+'_Window',600,500)
  if setRatioPlot:
    pad1 = ROOT.TPad('pad1','pad1',0.,0.3,1.,1.)
    pad1.SetBottomMargin(0.018)
  else:
    pad1 = ROOT.TPad('pad1','pad1',0.,0.,1.,1.)
  if setLogY:
    pad1.SetLogy()
  pad1.Draw()
  pad1.cd()
  legend = ROOT.TLegend(0.7,0.5,0.9,0.9)
  legend.SetFillColor(0)
  legend.SetBorderSize(0)
  legend.SetShadowColor(ROOT.kWhite)
  stack = ROOT.THStack('stack','Stacked Histograms')

  first = True

  for sample in allBkg:
    histos[sample['name']][var['name']].SetLineColor(ROOT.kBlack)
    histos[sample['name']][var['name']].SetLineWidth(1)
    histos[sample['name']][var['name']].SetFillColor(sample['color'])
    histos[sample['name']][var['name']].SetMarkerStyle(0)
    histos[sample['name']][var['name']].GetXaxis().SetTitle(var['Xtitle'])
    histos[sample['name']][var['name']].GetYaxis().SetTitle(var['Ytitle'])# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
    #histos[sample['name']][var['name']].GetXaxis().SetLabelSize(0.04)
    #histos[sample['name']][var['name']].GetYaxis().SetLabelSize(0.04)
    stack.Add(histos[sample['name']][var['name']])
    legend.AddEntry(histos[sample['name']][var['name']], sample['legendName'],'f')
         
  stack.Draw('hist')
  stack.GetXaxis().SetTitle(var['Xtitle'])
  stack.GetYaxis().SetTitle(var['Ytitle'])# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
  if setLogY:
    stack.SetMinimum(10**(-1))
    stack.SetMaximum(100*stack.GetMaximum())
  else:
    stack.SetMinimum(0.)
    stack.SetMaximum(1.5*stack.GetMaximum())

  for sig in allSignal:
    histos[sig['name']][var['name']].SetLineColor(sig['color'])
    histos[sig['name']][var['name']].SetLineWidth(2)
    histos[sig['name']][var['name']].SetLineStyle(ROOT.kDashed)
    histos[sig['name']][var['name']].SetFillColor(0)
    histos[sig['name']][var['name']].SetMarkerStyle(0)
    histos[sig['name']][var['name']].Draw('hist same')
    legend.AddEntry(histos[sig['name']][var['name']], sig['legendName'])
                        
  legend.Draw()

  canv.cd()

  if setRatioPlot:
    helpers.ATLASLabelRatioPad(0.18,0.88,"Work in progress")
    helpers.ATLASLumiLabelRatioPad(0.18,0.6, str(lumi*0.001))
    pad2 = ROOT.TPad("pad2","pad2",0.,0.,1.,0.3)
    pad2.SetTopMargin(0.01)
    pad2.SetBottomMargin(0.3)
    pad2.SetGrid()
    pad2.Draw()
    pad2.cd()
  
    ratio1 = doRatio(histos['ttbar2L'][var['name']],histos['ttbar1L'][var['name']],var['Xtitle'])
    ratio1.Draw("hist")
  else:
    pad1.cd()
    ATLASLabel(0.18,0.88,"Work in progress")
    ATLASLumiLabel(0.18,0.86, str(lumi*0.001))

  canv.cd()
  canv.Print(wwwDir+var["fileName"]+".pdf")
  canv.Print(wwwDir+var["fileName"]+".root")
  canv.Print(wwwDir+var["fileName"]+".png")
