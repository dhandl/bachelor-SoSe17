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
ROOT.TH1D().SetDefaultSumw2()

def doRatio(hist1,hist2,Ytitle='1/Default'):
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
  #h1.GetXaxis().SetTitle(Xtitle)
  #h1.GetYaxis().SetTitle(Ytitle)
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

def getYieldFromChain(c, cutString = "(1)", lumi = "36500.", weight = "weight * xs_weight * sf_total * weight_sherpa22_njets", returnError=True):
  h = ROOT.TH1D('h_tmp', 'h_tmp', 1,0,2)
  h.Sumw2()
  c.Draw("1>>h_tmp", "("+lumi+"*"+weight+")*("+cutString+")", 'goff')
  res = h.GetBinContent(1)
  resErr = h.GetBinError(1)
  del h
  if returnError:
   return res, resErr
  return res
                
wwwDir = "/afs/cern.ch/user/d/dhandl/www/Run2/SUSY/Stop1l/ttbarSyst/"
if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

fileName = "SystComparisonSherpa_5bin"

# setup input directories for TChains
bkgDir = "/eos/atlas/user/d/dboerner/SUSY/" 
#bkgDir = "/eos/atlas/user/j/jkuechle/public/ntuples_p2949/" 
#sigDir = "/afs/cern.ch/work/d/dhandl/public/Stop1L/syst_truth/" 
truthDir = "/afs/cern.ch/user/t/therwig/workspace/public/STOP_MORIOND17/syst/" 
sigDir = "/afs/cern.ch/work//j/jmitrevs/public/bWN_syst/" 

lumi = 36100.
weight = " weight * xs_weight * sf_total * weight_sherpa22_njets" 
truth_weight = " weight * xs_weight "

TIGHTE = "( (n_el>0) || Alt$(mu_idMedium,0) )"

bWN_PRESEL = "(stxe_trigger) && (n_jet>=4) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>130e3) && (met>230e3) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (dphi_met_lep<2.5) && " + TIGHTE
truth_bWN_PRESEL = "(n_lep==1) && (lep_pt[0]>25e3) && (n_jet>=4) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>130e3) && (met>230e3) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && (dphi_met_lep<2.5)"

bWN_CR_PRESEL = "(stxe_trigger) && (n_jet>=4) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>130e3) && (met>230e3) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && " + TIGHTE
truth_bWN_CR_PRESEL = "(n_lep==1) && (lep_pt[0]>25e3) && (n_jet>=4) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>130e3) && (met>230e3) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) "

SignalRegions = [
  #{"name":"TCR",  "cut":bWN_CR_PRESEL + "&&  dphi_met_lep>2.5 && amt2>=130 && amt2<170"},
  #{"name":"TVR",  "cut":bWN_CR_PRESEL + "&&  dphi_met_lep>2.5 && amt2>=110 && amt2<130 && met>300e3 "},
  {"name":"bWN",  "cut":bWN_PRESEL + "&& amt2<110 && met>300e3"},
  {"name":"bWN1", "cut":bWN_PRESEL + "&& amt2<91 && met>300e3"},
  {"name":"bWN2", "cut":bWN_PRESEL + "&& amt2>=91 && amt2<97 && met>300e3"},
  {"name":"bWN3", "cut":bWN_PRESEL + "&& amt2>=97 && amt2<106 && met>300e3"},
  {"name":"bWN4", "cut":bWN_PRESEL + "&& amt2>=106 && amt2<118 && met>300e3"},
  {"name":"bWN5", "cut":bWN_PRESEL + "&& amt2>=118 && amt2<130 && met>300e3"}
  #{"name":"bWN6", "cut":bWN_PRESEL + "&& amt2>=116.6 && amt2<123.3 && met>300e3"},
  #{"name":"bWN7", "cut":bWN_PRESEL + "&& amt2>=123.3 && amt2<130 && met>300e3"}
]

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
setRatioPlot = True

allBkg = [
#  {"name":"ttv", "legendName":"t#bar{t}+V", "target":bkgDir+"amcnlo_ttV/*", "color": ROOT.TColor.GetColor("#E67067"), "chain_name":"amcnlo_ttV_Nom"}, 
#  {"name":"diboson", "legendName":"Diboson", "target":bkgDir+"sherpa221_diboson/*", "color": ROOT.TColor.GetColor("#54C571"), "chain_name":"sherpa221_diboson_Nom"}, 
#  {"name":"singletop", "legendName":"Single top", "target":bkgDir+"powheg_singletop/*", "color": ROOT.TColor.GetColor("#82DE68"), "chain_name":"powheg_singletop_Nom"}, 
#  {"name":"wjets", "legendName":"W+jets", "target":bkgDir+"sherpa22_Wjets/*", "color": ROOT.TColor.GetColor("#FCDD5D"), "chain_name":"sherpa22_Wjets_Nom"}, 
#  {"name":"ttbar1L", "legendName":"t#bar{t} 1L", "target":bkgDir+"powheg_ttbar/*", "color":ROOT.TColor.GetColor("#0F75DB"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==1 || tt_cat==4 || tt_cat==7 )" },
#  {"name":"ttbar2L", "legendName":"t#bar{t} 2L", "target":bkgDir+"powheg_ttbar/*", "color":ROOT.TColor.GetColor("#A5C6E8"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==0 || tt_cat==3 || tt_cat==6 )" },
#  {"name":"ttbar1L1tau", "legendName":"t#bar{t} 1L1#tau", "target":bkgDir+"powheg_ttbar/*", "color": ROOT.TColor.GetColor("#5E9AD6"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==2 || tt_cat == 5 ) "},
  {"name":"ttbar",              "legendName":"t#bar{t}",           "target":bkgDir+"powheg_ttbar/*",     "chain_name":"powheg_ttbar_Nom", "color":ROOT.kBlack       },
  {"name":"sherpa_ttbar",              "legendName":"t#bar{t} sherpa",           "target":bkgDir+"sherpa_ttbar/*",     "chain_name":"sherpa_ttbar_Nom", "color":ROOT.kRed       },
#  {"name":"ttbar_radHi",        "legendName":"t#bar{t} radHi",     "target":bkgDir+"ttbar_radHi/*",      "chain_name":"ttbar_radHi_Nom" , "color":ROOT.kRed       },
#  {"name":"ttbar_radLo",        "legendName":"t#bar{t} radLo",     "target":bkgDir+"ttbar_radLo/*",      "chain_name":"ttbar_radLo_Nom" , "color":ROOT.kBlue       },
#  {"name":"hpp_ttbar",          "legendName":"t#bar{t} PwgHpp",    "target":bkgDir+"powheg_hpp_ttbar/*", "chain_name":"powheg_hpp_ttbar_Nom", "color":ROOT.kGreen+2   },
  {"name":"amcnlo_ttbar", "legendName":"t#bar{t} aMCNloHpp", "target":bkgDir+"amcnlo_ttbar/*",     "chain_name":"amcnlo_ttbar_Nom", "color":ROOT.kBlue       },
#  {"name":"ttbar",              "legendName":"t#bar{t}",           "target":truthDir+"syst_tt_PhPy/*",             "chain_name":"syst_tt_PhPy_Nom",     "isTruth":True,   "color":ROOT.kBlack       },
#  {"name":"ttbar_radHi",        "legendName":"t#bar{t} radHi",     "target":truthDir+"syst_tt_PhPy_rHi/*",       "chain_name":"syst_tt_PhPy_rHi_Nom",   "isTruth":True,   "color":ROOT.kRed       },
#  {"name":"ttbar_radLo",        "legendName":"t#bar{t} radLo",     "target":truthDir+"syst_tt_PhPy_rLo/*",       "chain_name":"syst_tt_PhPy_rLo_Nom",   "isTruth":True,   "color":ROOT.kBlue       },
#  {"name":"hpp_ttbar",          "legendName":"t#bar{t} PwgHpp",    "target":truthDir+"syst_tt_PhHpp/*",            "chain_name":"syst_tt_PhHpp_Nom",   "isTruth":True,   "color":ROOT.kGreen+2       },
#  {"name":"amcatnlo_hpp_ttbar", "legendName":"t#bar{t} aMCNloHpp", "target":truthDir+"syst_tt_aMCHpp/*",           "chain_name":"syst_tt_aMCHpp_Nom",  "isTruth":True,   "color":ROOT.kMagenta       },
#  {"name":"ttbar_PhPy8",        "legendName":"t#bar{t} PhPy8",     "target":truthDir+"syst_tt_PhPy8/*",             "chain_name":"syst_tt_PhPy8_Nom",  "isTruth":True,   "color":ROOT.k       },
#  {"name":"Wt",              "legendName":"Single top",           "target":truthDir+"syst_wt_PhPy/*",            "chain_name":"syst_wt_PhPy_Nom"           ,"isTruth":True, "color":ROOT.kBlack       },
#  {"name":"Wt_radHi",        "legendName":"Single top radHi",     "target":truthDir+"syst_wt_PhPy_rHi/*",        "chain_name":"syst_wt_PhPy_rHi_Nom"       ,"isTruth":True, "color":ROOT.kRed     },
#  {"name":"Wt_radLo",        "legendName":"Single top radLo",     "target":truthDir+"syst_wt_PhPy_rLo/*",        "chain_name":"syst_wt_PhPy_rLo_Nom"       ,"isTruth":True, "color":ROOT.kBlue     },
#  {"name":"hpp_Wt",          "legendName":"Single top PwgHpp",    "target":truthDir+"syst_wt_PhHpp/*",           "chain_name":"syst_wt_PhHpp_Nom"          ,"isTruth":True, "color":ROOT.kGreen+2       },
#  {"name":"amcatnlo_hpp_Wt", "legendName":"Single top aMCNloHpp", "target":truthDir+"syst_wt_aMCHpp/*",          "chain_name":"syst_wt_aMCHpp_Nom"         ,"isTruth":True, "color":ROOT.kMagenta       },
#  {"name":"mg5_ttbar",       "legendName":"ttbar MG5",            "target":truthDir+"mg5_ttbar_truth_MET200/*",  "chain_name":"mg5_ttbar_truth_MET200_Nom","isTruth":True, "color":ROOT.kBlack,  "addCut":"n_bjet>=2"         },
#  {"name":"mg5_WWbb",        "legendName":"WWbb MG5",             "target":truthDir+"mg5_WWbb_truth_MET200/*",   "chain_name":"mg5_WWbb_truth_MET200_Nom", "isTruth":True, "color":ROOT.kRed,  "addCut":"n_bjet>=2"         },
#  {"name":"mg5_Wtb",         "legendName":"Wtb MG5",              "target":truthDir+"mg5_Wtb_truth_MET200/*",    "chain_name":"mg5_Wtb_truth_MET200_Nom",  "isTruth":True, "color":ROOT.kBlue,  "addCut":"n_bjet>=2"         },

]

allSignal = [
#  {"name":"stop_bWN_350_200_Daniela", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(350,200)", "target":bkgDir+"stop_bWN_350_200_MadSpin_m1001L20/*", "color": ROOT.TColor.GetColor(ROOT.kBlue+2), "chain_name":"stop_bWN_350_200_MadSpin_m1001L20_Nom"},
  #{"name":"stop_bWN_350_200_Javier", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(350,200)", "target":sigDir+"stop_bWN_350_200/*", "color": ROOT.TColor.GetColor(ROOT.kRed), "chain_name":"stop_bWN_350_200_Nom"},
  {"name":"stop_bWN_350_200", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(350,200)", "target":bkgDir+"stop_bWN_350_200/*", "color":ROOT.kRed, "chain_name":"stop_bWN_350_200_Nom"},
#  {"name":"stop_bWN_350_230_nom", "legendName":"nominal", "target":sigDir+"Nominal_350_230/*", "color": ROOT.kBlack, "chain_name":"Nominal_350_230_Nom", "isTruth":True},
#  {"name":"stop_bWN_350_230_PS_dw", "legendName":"PS down", "target":sigDir+"py3cdw_350_230/*", "color": ROOT.kRed, "chain_name":"py3cdw_350_230_Nom", "isTruth":True},
#  {"name":"stop_bWN_350_230_PS_up", "legendName":"PS up", "target":sigDir+"py3cup_350_230/*", "color": ROOT.kBlue, "chain_name":"py3cup_350_230_Nom", "isTruth":True},
#  {"name":"stop_bWN_350_230_MERGE_dw", "legendName":"merging down", "target":sigDir+"qcdw_350_230/*", "color": ROOT.kGreen+2, "chain_name":"qcdw_350_230_Nom", "isTruth":True},
#  {"name":"stop_bWN_350_230_MERGE_up", "legendName":"merging up", "target":sigDir+"qcup_350_230/*", "color": ROOT.kOrange+7, "chain_name":"qcup_350_230_Nom", "isTruth":True},
#  {"name":"stop_bWN_350_230_FACT_dw", "legendName":"fact./ren. down", "target":sigDir+"scdw_350_230/*", "color": ROOT.kMagenta, "chain_name":"scdw_350_230_Nom", "isTruth":True},
#  {"name":"stop_bWN_350_230_FACT_up", "legendName":"fact./ren. up", "target":sigDir+"scup_350_230/*", "color": ROOT.kAzure+6, "chain_name":"scup_350_230_Nom", "isTruth":True},
]

for i, sample in enumerate(allBkg+allSignal):
  sample["chain"] = ROOT.TChain(sample["chain_name"])
  sample["chain"].Add(sample["target"])

histos = {}

for sample in allBkg:
#for sample in allBkg+allSignal:
  print sample["name"]
  histos[sample["name"]] = ROOT.TH1D(sample["name"], sample["name"], len(SignalRegions), 0, len(SignalRegions))
  for i,reg in enumerate(SignalRegions):
    if sample.has_key("addCut"):
      cutString = reg["cut"]+" && "+sample["addCut"]
    else:
      cutString = reg["cut"]
    #print cutString
    sample["yield"], sample["error"] = getYieldFromChain(sample["chain"], cutString, weight = weight)
    histos[sample["name"]].SetBinContent(i+1,sample["yield"])
    histos[sample["name"]].SetBinError(i+1,sample["error"])
    histos[sample["name"]].GetXaxis().SetBinLabel(i+1, reg["name"])

canv = ROOT.TCanvas('canv','canv',600,500)
if setRatioPlot:
  pad1 = ROOT.TPad('pad1','pad1',0.,0.3,1.,1.)
  pad1.SetBottomMargin(0.018)
else:
  pad1 = ROOT.TPad('pad1','pad1',0.,0.,1.,1.)
if setLogY:
  pad1.SetLogy()
pad1.Draw()
pad1.cd()
legend = ROOT.TLegend(0.65,0.7,0.9,0.9)
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetShadowColor(ROOT.kWhite)
stack = ROOT.THStack('stack','Stacked Histograms')

first = True

#for sample in allBkg:
#  histos[sample['name']].SetLineColor(ROOT.kBlack)
#  histos[sample['name']].SetLineWidth(1)
#  histos[sample['name']].SetFillColor(sample['color'])
#  histos[sample['name']].SetMarkerStyle(0)
#  #histos[sample['name']].GetXaxis().SetTitle(var['Xtitle'])
#  histos[sample['name']].GetYaxis().SetTitle("Events")# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
#  stack.Add(histos[sample['name']])
#  legend.AddEntry(histos[sample['name']], sample['legendName'],'f')
#       
#stack.Draw('hist')
##stack.GetXaxis().SetTitle(var['Xtitle'])
#stack.GetYaxis().SetTitle("Events")# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
#if setLogY:
#  stack.SetMinimum(10**(-1))
#  stack.SetMaximum(100*stack.GetMaximum())
#else:
#  stack.SetMinimum(0.)
#  stack.SetMaximum(1.25*stack.GetMaximum())

#for sig in allSignal:
for sig in allBkg:
  histos[sig['name']].SetLineColor(sig['color'])
  histos[sig['name']].SetLineWidth(2)
  #histos[sig['name']].SetLineStyle(ROOT.kDashed)
  histos[sig['name']].SetFillColor(0)
  histos[sig['name']].SetMarkerStyle(0)
  histos[sig['name']].SetMarkerColor(sig['color'])
  histos[sig['name']].GetXaxis().SetLabelSize(0.)
  if first:
    histos[sig['name']].Draw('hist e')
    first = False
  else:
    histos[sig['name']].Draw('hist e same')
  histos[sig['name']].SetMinimum(0)
  histos[sig['name']].SetMaximum(1.25*histos[sig['name']].GetMaximum())
  legend.AddEntry(histos[sig['name']], sig['legendName'])
                      
legend.Draw()

#l = ROOT.TLine(1, 0, 1, 1.25*stack.GetMaximum())
#l.SetLineStyle(ROOT.kDashed)
#l.Draw()
#l1 = ROOT.TLine(2, 0, 2, 1.25*stack.GetMaximum())
#l1.SetLineStyle(ROOT.kDashed)
#l1.Draw()

canv.cd()

if setRatioPlot:
  #helpers.ATLASLabelRatioPad(0.18,0.88,"Work in progress")
  #helpers.ATLASLumiLabelRatioPad(0.18,0.6, str(lumi*0.001))
  pad2 = ROOT.TPad("pad2","pad2",0.,0.,1.,0.3)
  pad2.SetTopMargin(0.01)
  pad2.SetBottomMargin(0.3)
  pad2.SetGrid()
  pad2.Draw()
  pad2.cd()

  ratio1 = doRatio(histos['sherpa_ttbar'],histos['ttbar'],"1./PwgPy6")
  ratio1.Draw("hist e")
  ratio2 = doRatio(histos['amcnlo_ttbar'],histos['ttbar'],"1./PwgPy6")
  ratio2.Draw("hist e same")
#else:
pad1.cd()
ATLASLabel(0.18,0.88,"Work in progress")
ATLASLumiLabel(0.18,0.86, str(lumi*0.001))

canv.cd()
canv.Print(wwwDir+fileName+".pdf")
canv.Print(wwwDir+fileName+".root")
canv.Print(wwwDir+fileName+".png")
