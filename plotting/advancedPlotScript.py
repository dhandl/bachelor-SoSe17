#!usr/bin/python2

import ROOT
import copy, os, sys

from AtlasStyle import * 
from math import *
from array import array

import PlotStyle as PS
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

def getYieldFromChain(c, cutString = "(1)", lumi = "140500.", weight = "weight * xs_weight * sf_total * lumi_weight", returnError=True):
  h = ROOT.TH1D('h_tmp', 'h_tmp', 1,0,2)
  h.Sumw2()
  c.Draw("1>>h_tmp", "("+lumi+"*"+weight+")*("+cutString+")", 'goff')
  res = h.GetBinContent(1)
  resErr = h.GetBinError(1)
  del h
  if returnError:
   return res, resErr
  return res
                
wwwDir = "/project/etp5/dhandl/plots/Stop1L/FullRun2/CR_VR_SR/"
if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

fileName = "yields"

# setup input directories for TChains
bkgDir = "/project/etp3/dhandl/samples/SUSY/Stop1L/21.2.60_ML/" 
sigDir = "/project/etp3/dhandl/samples/SUSY/Stop1L/21.2.60_ML/" 

lumi = 140500.
weight = " weight * xs_weight * sf_total * lumi_weight" 
truth_weight = " weight * xs_weight "


#bWN_PRESEL = "(stxe_trigger) && (n_jet>=4) && (jet_pt[0]>25e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>110e3) && (met>230e3) && (n_bjet>=1) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80))"
truth_bWN_PRESEL = "(n_lep==1) && (lep_pt[0]>25e3) && (n_jet>=4) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>130e3) && (met>230e3) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && (dphi_met_lep<2.5)"
bWN_PRESEL = "(stxe_trigger) && (mt>110e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && n_jet >= 4 && jet_pt[0]>25e3 && jet_pt[1]>25e3 && jet_pt[2]>25e3 && jet_pt[3]>25e3 && n_bjet >= 1 && n_lep == 1 && lep_pt[0] > 25e3 && met > 230e3 && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80))"

SignalRegions = [
  {"name":"TCR",  "cut":bWN_PRESEL + "&& mt>150e3 && outputScore_RNN>=0.4 && outputScore_RNN<0.6"},
  {"name":"TVR",  "cut":bWN_PRESEL + "&& mt>150e3 && outputScore_RNN>=0.6 && outputScore_RNN<0.65"},
  {"name":"bWN1", "cut":bWN_PRESEL + "&& mt>150e3 && outputScore_RNN>=0.65 && outputScore_RNN<0.70"},
  {"name":"bWN2", "cut":bWN_PRESEL + "&& mt>150e3 && outputScore_RNN>=0.70 && outputScore_RNN<0.75"},
  {"name":"bWN3", "cut":bWN_PRESEL + "&& mt>150e3 && outputScore_RNN>=0.75 && outputScore_RNN<0.80"},
  {"name":"bWN4", "cut":bWN_PRESEL + "&& outputScore_RNN>=0.80 && outputScore_RNN<0.82"},
  {"name":"bWN5", "cut":bWN_PRESEL + "&& outputScore_RNN>=0.82 && outputScore_RNN<0.84"},
  {"name":"bWN6", "cut":bWN_PRESEL + "&& outputScore_RNN>=0.84 && outputScore_RNN<0.86"},
  {"name":"bWN7", "cut":bWN_PRESEL + "&& outputScore_RNN>=0.86 && outputScore_RNN<0.88"},
  {"name":"bWN8", "cut":bWN_PRESEL + "&& outputScore_RNN>=0.88 && outputScore_RNN<0.90"},
  {"name":"bWN9", "cut":bWN_PRESEL + "&& outputScore_RNN>=0.90 && outputScore_RNN<0.92"},
  {"name":"bWN10", "cut":bWN_PRESEL + "&& outputScore_RNN>=0.92 && outputScore_RNN<1.0"},
  {"name":"bWN",  "cut":bWN_PRESEL + " && outputScore_RNN>=0.90 && outputScore_RNN<1.0"}
]

#----------------------------#
normalized = False
if normalized:
  normString = "_norm"
else:
  normString = ""
#----------------------------#
#setLogY = False
setLogY = True
if setLogY:
  logString = "_logScale"
else:
  logString = ""
#----------------------------#
setRatioPlot = False

allBkg = [
  {"name":"ttv", "legendName":"t#bar{t}+V", "target":[bkgDir+"mc16a_ttV/*.root",bkgDir+"mc16d_ttV/*.root",bkgDir+"mc16e_ttV/*.root"], "color": ROOT.TColor.GetColor("#E67067"), "chain_name":"ttV_Nom"}, 
  {"name":"multiboson", "legendName":"Multiboson", "target":[bkgDir+"mc16a_multiboson/*.root",bkgDir+"mc16d_multiboson/*.root",bkgDir+"mc16e_multiboson/*.root"], "color": ROOT.TColor.GetColor("#54C571"), "chain_name":"multiboson_Nom"}, 
  {"name":"singletop", "legendName":"Single top", "target":[bkgDir+"mc16a_singletop/*.root",bkgDir+"mc16d_singletop/*.root",bkgDir+"mc16e_singletop/*.root"], "color": ROOT.TColor.GetColor("#82DE68"), "chain_name":"singletop_Nom"}, 
  {"name":"wjets", "legendName":"W+jets", "target":[bkgDir+"mc16a_wjets/*.root",bkgDir+"mc16d_wjets/*.root",bkgDir+"mc16e_wjets/*.root"], "color": ROOT.TColor.GetColor("#FCDD5D"), "chain_name":"wjets_Nom"}, 
#  {"name":"ttbar1L", "legendName":"t#bar{t} 1L", "target":bkgDir+"powheg_ttbar/*", "color":ROOT.TColor.GetColor("#0F75DB"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==1 || tt_cat==4 || tt_cat==7 )" },
#  {"name":"ttbar2L", "legendName":"t#bar{t} 2L", "target":bkgDir+"powheg_ttbar/*", "color":ROOT.TColor.GetColor("#A5C6E8"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==0 || tt_cat==3 || tt_cat==6 )" },
#  {"name":"ttbar1L1tau", "legendName":"t#bar{t} 1L1#tau", "target":bkgDir+"powheg_ttbar/*", "color": ROOT.TColor.GetColor("#5E9AD6"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==2 || tt_cat == 5 ) "},
  {"name":"ttbar",              "legendName":"t#bar{t}",           "target":[bkgDir+"mc16a_ttbar/*.root",bkgDir+"mc16d_ttbar/*.root",bkgDir+"mc16e_ttbar/*.root"],     "chain_name":"ttbar_Nom", "color":ROOT.TColor.GetColor("#A5C6E8")       },
#  {"name":"sherpa_ttbar",              "legendName":"t#bar{t} sherpa",           "target":bkgDir+"sherpa_ttbar/*",     "chain_name":"sherpa_ttbar_Nom", "color":ROOT.kRed       },
#  {"name":"ttbar_radHi",        "legendName":"t#bar{t} radHi",     "target":bkgDir+"ttbar_radHi/*",      "chain_name":"ttbar_radHi_Nom" , "color":ROOT.kRed       },
#  {"name":"ttbar_radLo",        "legendName":"t#bar{t} radLo",     "target":bkgDir+"ttbar_radLo/*",      "chain_name":"ttbar_radLo_Nom" , "color":ROOT.kBlue       },
#  {"name":"hpp_ttbar",          "legendName":"t#bar{t} PwgHpp",    "target":bkgDir+"powheg_hpp_ttbar/*", "chain_name":"powheg_hpp_ttbar_Nom", "color":ROOT.kGreen+2   },
#  {"name":"amcnlo_ttbar", "legendName":"t#bar{t} aMCNloHpp", "target":bkgDir+"amcnlo_ttbar/*",     "chain_name":"amcnlo_ttbar_Nom", "color":ROOT.kBlue       },
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
  {"name":"bWN_500_350", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,350)", "target":[bkgDir+"mc16a_bWN_500_350/*.root",bkgDir+"mc16d_bWN_500_350/*.root",bkgDir+"mc16e_bWN_500_350/*.root",], "color":ROOT.kRed, "chain_name":"bWN_500_350_Nom"},
  {"name":"bWN_500_380", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,380)", "target":[bkgDir+"mc16a_bWN_500_380/*.root",bkgDir+"mc16d_bWN_500_380/*.root",bkgDir+"mc16e_bWN_500_380/*.root",], "color":ROOT.kBlue+2, "chain_name":"bWN_500_380_Nom"},
  {"name":"bWN_500_410", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,410)", "target":[bkgDir+"mc16a_bWN_500_410/*.root",bkgDir+"mc16d_bWN_500_410/*.root",bkgDir+"mc16e_bWN_500_410/*.root",], "color":ROOT.kGreen+2, "chain_name":"bWN_500_410_Nom"},
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
  for target in sample['target']:
    sample["chain"].Add(target)

histos = {}

for sample in allBkg+allSignal:
#for sample in allBkg+allSignal:
  print sample["name"]
  histos[sample["name"]] = ROOT.TH1D(sample["name"], sample["name"], len(SignalRegions), 0, len(SignalRegions))
  for i,reg in enumerate(SignalRegions):
    if sample.has_key("addCut"):
      cutString = reg["cut"]+" && "+sample["addCut"]
    else:
      cutString = reg["cut"]
    #print cutString
    sample["yield"], sample["error"] = getYieldFromChain(sample["chain"], cutString, lumi=str(lumi), weight = weight)
    print reg['name'] 
    print "%.2f$\pm$%.2f"%(round(sample["yield"],2),round(sample["error"],2))
    histos[sample["name"]].SetBinContent(i+1,sample["yield"])
    histos[sample["name"]].SetBinError(i+1,sample["error"])
    histos[sample["name"]].GetXaxis().SetBinLabel(i+1, reg["name"])

canv = ROOT.TCanvas('canv','canv',800,500)
if setRatioPlot:
  pad1 = ROOT.TPad('pad1','pad1',0.,0.3,1.,1.)
  pad1.SetBottomMargin(0.018)
else:
  pad1 = ROOT.TPad('pad1','pad1',0.,0.,1.,1.)
if setLogY:
  pad1.SetLogy()
pad1.Draw()
pad1.cd()
legend = ROOT.TLegend(0.65,0.55,0.9,0.9)
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetShadowColor(ROOT.kWhite)
stack = ROOT.THStack('stack','Stacked Histograms')

first = True

for sample in allBkg:
  histos[sample['name']].SetLineColor(ROOT.kBlack)
  histos[sample['name']].SetLineWidth(1)
  histos[sample['name']].SetFillColor(sample['color'])
  histos[sample['name']].SetMarkerStyle(0)
  #histos[sample['name']].GetXaxis().SetTitle(var['Xtitle'])
  histos[sample['name']].GetYaxis().SetTitle("Events")# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
  stack.Add(histos[sample['name']])
  legend.AddEntry(histos[sample['name']], sample['legendName'],'f')
       
stack.Draw('hist')
#stack.GetXaxis().SetTitle(var['Xtitle'])
stack.GetYaxis().SetTitle("Events")# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
if setLogY:
  stack.SetMinimum(0.1)
  stack.SetMaximum(500*stack.GetMaximum())
else:
  stack.SetMinimum(0.)
  stack.SetMaximum(1.5*stack.GetMaximum())

#for sig in allSignal:
for sig in allSignal:
  histos[sig['name']].SetLineColor(sig['color'])
  histos[sig['name']].SetLineWidth(2)
  histos[sig['name']].SetLineStyle(ROOT.kDashed)
  histos[sig['name']].SetFillColor(0)
  histos[sig['name']].SetMarkerStyle(0)
  histos[sig['name']].SetMarkerColor(sig['color'])
  histos[sig['name']].GetXaxis().SetLabelSize(0.)
  #if first:
  #  histos[sig['name']].Draw('hist e')
  #3  first = False
  #else:
  #  histos[sig['name']].Draw('hist e same')
  histos[sig['name']].Draw('hist same')
  #histos[sig['name']].SetMinimum(0)
  #histos[sig['name']].SetMaximum(1.25*histos[sig['name']].GetMaximum())
  legend.AddEntry(histos[sig['name']], sig['legendName'])
                      
legend.Draw()

#l = ROOT.TLine(1, ROOT.gPad.GetUymin(), 1, ROOT.gPad.GetUymax())
#l.SetLineStyle(ROOT.kDashed)
#l.SetLineColor(ROOT.kBlack)
#l.SetLineWidth(3)
#l.Draw("same")
#l1 = ROOT.TLine(2, ROOT.gPad.GetUymin(), 2, ROOT.gPad.GetUymax())
#l1.SetLineStyle(ROOT.kDashed)
#l1.SetLineColor(ROOT.kBlack)
#l1.SetLineWidth(3)
#l1.Draw('same')
#l2 = ROOT.TLine(12, ROOT.gPad.GetUymin(), 12, ROOT.gPad.GetUymax())
#l2.SetLineStyle(ROOT.kDashed)
#l2.SetLineColor(ROOT.kBlack)
#l2.SetLineWidth(3)
#l2.Draw('same')


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

pad1.cd()
PS.atlas('Work in progress')
if not normalized:
  PS.sqrts_lumi(13, 140.5, x=0.18)
PS.string(x=0.18, y=PS.ThirdLine, text="Simulation")

canv.cd()
canv.Print(wwwDir+fileName+".pdf")
canv.Print(wwwDir+fileName+".root")
canv.Print(wwwDir+fileName+".png")
