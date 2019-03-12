#!usr/bin/env python

import ROOT
import copy, os, sys
import helpers

from AtlasStyle import * 
from math import *
from array import array

import PlotStyle as PS
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.TGaxis().SetMaxDigits(3)
ROOT.TH1F().SetDefaultSumw2()

def doRatio(hist1,hist2,ymin=-1.2,ymax=4.2,Xtitle='',Ytitle='1/Default'):
  h1=hist1.Clone()
  h2=hist2.Clone()
  h1.Sumw2()
  h2.Sumw2()
  #h1.Scale(1./h1.Integral())
  #h2.Scale(1./h2.Integral())
  h1.Divide(h2)

  h1.SetMinimum(ymin)
  h1.SetMaximum(ymax)
  h1.SetStats(0)
  #h1.SetLineColor(hist1.GetLineColor())
  #h1.SetLineStyle(1)
  #h1.SetLineWidth(1)
  h1.GetXaxis().SetTitle(Xtitle)
  h1.GetYaxis().SetTitle(Ytitle)
  h1.GetYaxis().SetNdivisions(505)
  h1.GetYaxis().SetTitleSize(16)
  h1.GetYaxis().SetTitleFont(43)
  h1.GetYaxis().SetTitleOffset(2.2)
  h1.GetYaxis().SetLabelFont(43)
  h1.GetYaxis().SetLabelSize(16)
  #h1.GetYaxis().SetLabelOffset(0.015)
  h1.GetXaxis().SetNdivisions(510)
  h1.GetXaxis().SetTitleSize(16)
  h1.GetXaxis().SetTitleFont(43)
  h1.GetXaxis().SetTitleOffset(3.4)
  h1.GetXaxis().SetLabelFont(43)
  h1.GetXaxis().SetLabelSize(16)
  #h1.GetXaxis().SetLabelOffset(0.03)
  return h1


wwwDir = "/project/etp5/dhandl/plots/Stop1L/FullRun2/shapeComparison/ttbar2L/bWN_SR/"
if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

fileName = "bWN_SR"
#fileName = "mt130_met230_shapeComparison_HardScatter_oldPtag"
#fileName = "mt130_met230_shapeComparison_HadFrag_oldPtag"

# setup input directories for TChains
#bkgDir = "/eos/atlas/user/d/dboerner/" 
bkgDir = "/project/etp3/dhandl/samples/SUSY/Stop1L/21.2.60_ML/" 
#sigDir = "/afs/cern.ch/work/d/dhandl/public/Stop1L/syst_truth/" 
#truthDir = "/afs/cern.ch/user/t/therwig/workspace/public/STOP_MORIOND17/syst/"
truthDir = "/project/etp3/dhandl/samples/SUSY/Stop1L/TRUTH/" 
#truthDir = "/afs/cern.ch/work/d/dhandl/SUSY/stop1l-xaod/export/syst_truth/" 
sigDir = "/afs/cern.ch/work/j/jmitrevs/public/bWN_syst/"

lumi = 140500.
reco_weight = "weight * xs_weight * sf_total * lumi_weight" 
truth_weight = str(lumi) + " * eventWeight" 

reco_cut = "(stxe_trigger) && (n_lep==1) && (lep_pt[0]>25e3) && (n_bjet>0) && (mt>110e3) && (met>230e3) && (n_jet>=4) && (jet_pt[0]>25e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (outputScore_RNN>=0.9) && (outputScore_RNN<1.0)"
truth_cut = "(n_lep==1) && (n_lep_hard==1) && (lep_pt[0]>25) && (n_jet>=4) && (jet_pt[0]>25) && (jet_pt[1]>25) && (jet_pt[2]>25) && (jet_pt[3]>25) && (mt>110) && (met>230) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mt2_tau > -0.5) && (mt2_tau < 80))"

#----------------------------#
normalized = True
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
#  {"name":"ttv", "legendName":"t#bar{t}+V", "target":bkgDir+"madgraph_ttV/*", "color": ROOT.TColor.GetColor("#E67067"), "chain_name":"madgraph_ttV_Nom"}, 
#  {"name":"diboson", "legendName":"Diboson", "target":bkgDir+"sherpa_diboson/*", "color": ROOT.TColor.GetColor("#54C571"), "chain_name":"sherpa_diboson_Nom"}, 
#  {"name":"singletop1L", "legendName":"Single top 1L", "target":stDir+"mc16d_singletop/*.root", "color": ROOT.TColor.GetColor("#82DE68"), "chain_name":"mc16d_singletop_Nom", "isTruth":False, "addCut":"( st_cat==1 || st_cat==4 || st_cat==7 )"}, 
#  {"name":"singletop2L", "legendName":"Single top 2L", "target":stDir+"mc16d_singletop/*.root", "color": ROOT.TColor.GetColor("#82DE68"), "chain_name":"mc16d_singletop_Nom", "isTruth":False, "addCut":"( st_cat==0 || st_cat==2 || st_cat==3 || st_cat==5 || st_cat==6 )"}, 
#  {"name":"wjets", "legendName":"W+jets", "target":bkgDir+"mc16d_wjets/*.root", "color": ROOT.TColor.GetColor("#FCDD5D"), "chain_name":"mc16d_wjets_Nom"}, 
#  {"name":"ttbar1L", "legendName":"t#bar{t} 1L", "target":bkgDir+"mc16d_ttbar/*.root", "color":ROOT.TColor.GetColor("#0F75DB"), "chain_name":"mc16d_ttbar_Nom", "addCut":"( tt_cat==1 || tt_cat==4 || tt_cat==7 )" },
#  {"name":"ttbar2L", "legendName":"t#bar{t} 2L", "target":bkgDir+"mc16d_ttbar/*.root", "color":ROOT.TColor.GetColor("#A5C6E8"), "chain_name":"mc16d_ttbar_Nom", "addCut":"( tt_cat==0 || tt_cat==2 || tt_cat==3 || tt_cat == 5 || tt_cat==6 )", "isTruth":False },
#  {"name":"ttbar1L1tau", "legendName":"t#bar{t} 1L1#tau", "target":bkgDir+"powheg_ttbar/*", "color": ROOT.TColor.GetColor("#5E9AD6"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==2 || tt_cat == 5 )", "isTruth":False}, 
  {"name":"ttbar2L",       "legendName":"t#bar{t} 2L",       "target":[bkgDir+"mc16a_ttbar/*.root",bkgDir+"mc16d_ttbar/*.root",bkgDir+"mc16e_ttbar/*.root"], "chain_name":"ttbar_Nom", 'color':ROOT.TColor.GetColor("#A5C6E8"), 'addCut':'( tt_cat==0 || tt_cat==3 || tt_cat==6 )'},
  {"name":"ttbar1L1tau",       "legendName":"t#bar{t} 1L1#tau",       "target":[bkgDir+"mc16a_ttbar/*.root",bkgDir+"mc16d_ttbar/*.root",bkgDir+"mc16e_ttbar/*.root"], "chain_name":"ttbar_Nom", 'color':ROOT.TColor.GetColor("#5E9AD6"), 'addCut':'(tt_cat==2 || tt_cat==5)'},
  #{"name":"ttbar_radLo", "legendName":"t#bar{t} radLo", "target":[bkgDir+"mc16a_ttbar/*.root",bkgDir+"mc16d_ttbar/*.root",bkgDir+"mc16e_ttbar/*.root"], "chain_name":"ttbar_Nom", "addWeight":"1.15 * weight_ttbar_radLo * 1./weight", 'color':ROOT.kBlue},
  #{"name":"ttbar_radHi", "legendName":"t#bar{t} radHi", "target":[bkgDir+"mc16a_ttbar/*.root",bkgDir+"mc16d_ttbar/*.root",bkgDir+"mc16e_ttbar/*.root"], "chain_name":"ttbar_Nom", "addWeight":"0.8858 * weight_ttbar_radHi * 1./weight", 'color':ROOT.kRed+2},
  #{"name":"ttbar_radHiHdamp", "legendName":"t#bar{t} radHi (+hdamp)", "target":[bkgDir+"mc16a_ttbar_radHi/*.root",bkgDir+"mc16d_ttbar_radHi/*.root",bkgDir+"mc16e_ttbar_radHi/*.root"], "chain_name":"ttbar_radHi", "addWeight":"0.8858 * weight_ttbar_radHi * 1./weight", 'color':ROOT.kRed},
  #{"name":"ttbar",              "legendName":"t#bar{t}",           "target":bkgDir+"powheg_ttbar/*",     "chain_name":"powheg_ttbar_Nom", "color":ROOT.kBlack, "isTruth":False       },
  #{"name":"ttbar_radHi",        "legendName":"t#bar{t} radHi",     "target":bkgDir+"ttbar_radHi/*",      "chain_name":"ttbar_radHi_Nom" , "color":ROOT.kRed       },
#  {"name":"ttbar_radLo",        "legendName":"t#bar{t} radLo",     "target":bkgDir+"ttbar_radLo/*",      "chain_name":"ttbar_radLo_Nom" , "color":ROOT.kBlue       },
#  {"name":"hpp_ttbar",          "legendName":"t#bar{t} PwgHpp",    "target":bkgDir+"powheg_hpp_ttbar/*", "chain_name":"powheg_hpp_ttbar_Nom", "color":ROOT.kGreen+2   },
#  {"name":"amcnlo_ttbar", "legendName":"t#bar{t} aMCNloHpp", "target":bkgDir+"amcatnlo_hpp_ttbar/*",     "chain_name":"amcatnlo_hpp_ttbar_Nom", "color":ROOT.kMagenta       },
#  {"name":"ttbar1L",              "legendName":"t#bar{t} 1L",           "target":bkgDir+"powheg_ttbar/*", "chain_name":"powheg_ttbar_Nom",             "addCut":"( tt_cat==1 || tt_cat==4 || tt_cat==7 )"},
#  {"name":"ttbar1L_radHi",        "legendName":"t#bar{t} 1L radHi",     "target":bkgDir+"ttbar_radHi/*", "chain_name":"ttbar_radHi_Nom",              "addCut":"( tt_cat==1 || tt_cat==4 || tt_cat==7 )"},
#  {"name":"ttbar1L_radLo",        "legendName":"t#bar{t} 1L radLo",     "target":bkgDir+"ttbar_radLo/*", "chain_name":"ttbar_radLo_Nom",              "addCut":"( tt_cat==1 || tt_cat==4 || tt_cat==7 )"},
#  {"name":"hpp_ttbar1L",          "legendName":"t#bar{t} 1L PwgHpp",    "target":bkgDir+"powheg_hpp_ttbar/*", "chain_name":"powheg_hpp_ttbar_Nom",     "addCut":"( tt_cat==1 || tt_cat==4 || tt_cat==7 )"},
#  {"name":"amcatnlo_hpp_ttbar1L", "legendName":"t#bar{t} 1L aMCNloHpp", "target":bkgDir+"amcatnlo_hpp_ttbar/*", "chain_name":"amcatnlo_hpp_ttbar_Nom", "addCut":"( tt_cat==1 || tt_cat==4 || tt_cat==7 )"},
#  {"name":"ttbar2L",              "legendName":"t#bar{t} 2L",           "target":bkgDir+"powheg_ttbar/*", "chain_name":"powheg_ttbar_Nom",             "addCut":"( tt_cat==0 || tt_cat==3 || tt_cat==6 || tt_cat==2 || tt_cat == 5 )"},
#  {"name":"ttbar2L_radHi",        "legendName":"t#bar{t} 2L radHi",     "target":bkgDir+"ttbar_radHi/*", "chain_name":"ttbar_radHi_Nom",              "addCut":"( tt_cat==0 || tt_cat==3 || tt_cat==6 || tt_cat==2 || tt_cat == 5 )"},
#  {"name":"ttbar2L_radLo",        "legendName":"t#bar{t} 2L radLo",     "target":bkgDir+"ttbar_radLo/*", "chain_name":"ttbar_radLo_Nom",              "addCut":"( tt_cat==0 || tt_cat==3 || tt_cat==6 || tt_cat==2 || tt_cat == 5 )"},
#  {"name":"hpp_ttbar2L",          "legendName":"t#bar{t} 2L PwgHpp",    "target":bkgDir+"powheg_hpp_ttbar/*", "chain_name":"powheg_hpp_ttbar_Nom",     "addCut":"( tt_cat==0 || tt_cat==3 || tt_cat==6 || tt_cat==2 || tt_cat == 5 )"},
#  {"name":"amcatnlo_hpp_ttbar2L", "legendName":"t#bar{t} 2L aMCNloHpp", "target":bkgDir+"amcatnlo_hpp_ttbar/*", "chain_name":"amcatnlo_hpp_ttbar_Nom", "addCut":"( tt_cat==0 || tt_cat==3 || tt_cat==6 || tt_cat==2 || tt_cat == 5 )"},

#  {"name":"stop_bWN_450_300_nom", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (TRUTH)", "target":truthDir+"stop_bWN_450_300_truth_highStat_v4/*.root", "color": ROOT.kBlack, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True},
#  {"name":"stop_bWN_450_300_mc16", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (mc16d)", "target":bkgDir+"stop_bWN_450_300_mc16d/*.root", "color": ROOT.kBlue, "chain_name":"stop_bWN_450_300_mc16d_Nom", "isTruth":False},

#  {"name":"stop_bWN_450_300_nom", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (nominal)", "target":truthDir+"stop_bWN_450_300_Systematics/stop_bWN_450_300_truth_nom2/*.root", "color": ROOT.kBlack, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"2.4926739e-6"},
#  {"name":"stop_bWN_450_300_py3cdw", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (PS down)", "target":truthDir+"stop_bWN_450_300_Systematics/stop_bWN_450_300_truth_py3cdw2/*.root", "color": ROOT.kRed, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"2.5580223e-6"},
#  {"name":"stop_bWN_450_300_py3cup", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (PS up)", "target":truthDir+"stop_bWN_450_300_Systematics/stop_bWN_450_300_truth_py3cup2/*.root", "color": ROOT.kBlue, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"3.0288650e-6"},
#  {"name":"stop_bWN_450_300_qcdw", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (Merging down)", "target":truthDir+"stop_bWN_450_300_Systematics/stop_bWN_450_300_truth_qcdw2/*.root", "color": ROOT.kGreen+2, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"2.2612986e-6"},
#  {"name":"stop_bWN_450_300_qcup", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (Merging up)", "target":truthDir+"stop_bWN_450_300_Systematics/stop_bWN_450_300_truth_qcup2/*.root", "color": ROOT.kOrange+7, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"3.2773017e-6"},
#  {"name":"stop_bWN_450_300_scdw", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (Fact. down)", "target":truthDir+"stop_bWN_450_300_Systematics/stop_bWN_450_300_truth_scdw2/*.root", "color": ROOT.kMagenta, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"2.6069763e-6"},
#  {"name":"stop_bWN_450_300_scup", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (Fact. up)", "target":truthDir+"stop_bWN_450_300_Systematics/stop_bWN_450_300_truth_scup2/*.root", "color": ROOT.kAzure+6, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"2.3937855e-6"},

#  {"name":"stop_bWN_500_410_nom", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,410) (nominal)", "target":truthDir+"stop_bWN_500_410_Systematics/stop_bWN_500_410_truth_nom2/*.root", "color": ROOT.kBlack, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"1.1721006e-6"},
#  {"name":"stop_bWN_500_410_py3cdw", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,410) (PS down)", "target":truthDir+"stop_bWN_500_410_Systematics/stop_bWN_500_410_truth_py3cdw2/*.root", "color": ROOT.kRed, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"1.1923293e-6"},
#  {"name":"stop_bWN_500_410_py3cup", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,410) (PS up)", "target":truthDir+"stop_bWN_500_410_Systematics/stop_bWN_500_410_truth_py3cup2/*.root", "color": ROOT.kBlue, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"1.4348189e-6"},
#  {"name":"stop_bWN_500_410_qcdw", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,410) (Merging down)", "target":truthDir+"stop_bWN_500_410_Systematics/stop_bWN_500_410_truth_qcdw2/*.root", "color": ROOT.kGreen+2, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"1.0595916e-6"},
#  {"name":"stop_bWN_500_410_qcup", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,410) (Merging up)", "target":truthDir+"stop_bWN_500_410_Systematics/stop_bWN_500_410_truth_qcup2/*.root", "color": ROOT.kOrange+7, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"1.2350749e-6"},
#  {"name":"stop_bWN_500_410_scdw", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,410) (Fact. down)", "target":truthDir+"stop_bWN_500_410_Systematics/stop_bWN_500_410_truth_scdw2/*.root", "color": ROOT.kMagenta, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"1.2263233e-6"},
#  {"name":"stop_bWN_500_410_scup", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,410) (Fact. up)", "target":truthDir+"stop_bWN_500_410_Systematics/stop_bWN_500_410_truth_scup2/*.root", "color": ROOT.kAzure+6, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"1.1214690e-6"},

#  {"name":"ttbar_truth",              "legendName":"t#bar{t}",           "target":truthDir+"syst_tt_PhPy/*",             "chain_name":"syst_tt_PhPy_Nom",     "isTruth":True,   "color":ROOT.kRed       },
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
#  {"name":"mg5_ttbar",       "legendName":"ttbar MG5",            "target":truthDir+"mg5_ttbar_truth_MET200/*",  "chain_name":"mg5_ttbar_truth_MET200_Nom","isTruth":True, "color":ROOT.k,  "addCut":"n_bjet>=2"         },
#  {"name":"mg5_WWbb",        "legendName":"WWbb MG5",             "target":truthDir+"mg5_WWbb_truth_MET200/*",   "chain_name":"mg5_WWbb_truth_MET200_Nom", "isTruth":True, "color":ROOT.k,  "addCut":"n_bjet>=2"         },
#  {"name":"mg5_Wtb",         "legendName":"Wtb MG5",              "target":truthDir+"mg5_Wtb_truth_MET200/*",    "chain_name":"mg5_Wtb_truth_MET200_Nom",  "isTruth":True, "color":ROOT.k,  "addCut":"n_bjet>=2"         },

]

for i, sample in enumerate(allBkg):
  sample["chain"] = ROOT.TChain(sample["chain_name"])
  for target in sample['target']:
    sample["chain"].Add(target)

allVariables = []
#amt2 = {'name':'myAmt2', "fileName":fileName+"_amt2"+normString+logString, 'varStr':"amt2", 'Xtitle':'am_{T2}', 'Ytitle':'Events', 'binning':[80,90,100,110,120,170,250,350,600], "binningIsExplicit":True}
amt2 = {'name':'myAmt2', "fileName":fileName+"_amt2"+normString+logString, 'varStr':"amt2", 'Xtitle':'am_{T2} [GeV]', 'Ytitle':'Events / 20 Gev', 'binning':[30,0,600], "binningIsExplicit":False}
dphi = {'name':'mydphi', "fileName":fileName+"_dphi"+normString+logString, 'varStr':"dphi_met_lep", 'Xtitle':'#Delta#Phi(E_{T}^{miss},l)', 'Ytitle':'Events / 0.2', 'binning':[16,0,3.2], "binningIsExplicit":False}
met = {'name':'myMet', "fileName":fileName+"_met"+normString+logString, 'varStr':"(met*0.001)", 'Xtitle':'E_{T}^{miss} [GeV]', 'Ytitle':'Events / 20 GeV', 'binning':[40,200,1200], "binningIsExplicit":False}
metphi = {'name':'mymetPhi', "fileName":fileName+"_metPhi"+normString+logString, 'varStr':"met_phi", 'Xtitle':' #phi(#vec{p}_{T}^{miss})', 'Ytitle':'Events / 0.4', 'binning':[16,-pi,pi], "binningIsExplicit":False}
njet = {'name':'myNjet', "fileName":fileName+"_njet"+normString+logString, 'varStr':"n_jet", 'Xtitle':'Jet multiplicity', 'Ytitle':'Events', 'binning':[11,-0.5,10.5], "binningIsExplicit":False}
leppt = {'name':'myLepton', "fileName":fileName+"_lepPt"+normString+logString, 'varStr':"(lep_pt[0]*0.001)", 'Xtitle':'lepton p_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[20,0,500], "binningIsExplicit":False}
jet1 = {'name':'myJet1', "fileName":fileName+"_jetPt1"+normString+logString, 'varStr':"(jet_pt[0]*0.001)", 'Xtitle':'first jet p_{T} [GeV]', 'Ytitle':'Events / 40 GeV', 'binning':[20,0,800], "binningIsExplicit":False}
jet2 = {'name':'myJet2', "fileName":fileName+"_jetPt2"+normString+logString, 'varStr':"(jet_pt[1]*0.001)", 'Xtitle':'second jet p_{T} [GeV]', 'Ytitle':'Events / 40 GeV', 'binning':[15,0,600], "binningIsExplicit":False}
jet3 = {'name':'myJet3', "fileName":fileName+"_jetPt3"+normString+logString, 'varStr':"(jet_pt[2]*0.001)", 'Xtitle':'third jet p_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[14,0,350], "binningIsExplicit":False}
jet4 = {'name':'myJet4', "fileName":fileName+"_jetPt4"+normString+logString, 'varStr':"(jet_pt[3]*0.001)", 'Xtitle':'fourth jet p_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[10,0,250], "binningIsExplicit":False}
nbjet = {'name':'myNbjet', "fileName":fileName+"_nbjet"+normString+logString, 'varStr':"n_bjet", 'Xtitle':'b-jet multiplicity', 'Ytitle':'Events', 'binning':[5,-0.5,4.5], "binningIsExplicit":False}
mt = {'name':'myMT','fileName':fileName+'_mt'+normString+logString, 'varStr':'mt*0.001', 'Xtitle':'m_{T} [GeV]', 'Ytitle':'Events', 'binning':[24,100,700], 'binningIsExplicit':False}
ntop = {'name':'myntop','fileName':fileName+'_n_hadtop'+normString+logString, 'varStr':'n_hadtop_cand', 'Xtitle':'n_{had. top}', 'Ytitle':'Events', 'binning':[4,-0.5,3.5], 'binningIsExplicit':False}
ht = {'name':'myht','fileName':fileName+'_hT'+normString+logString, 'varStr':'ht*0.001', 'Xtitle':'h_{T} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
dphi_jet0_ptmiss = {'name':'mydPhi_jet0ptmiss', 'fileName':fileName+'_dphi_jet0_ptmiss'+normString+logString, 'varStr':'dphi_jet0_ptmiss', 'Xtitle':'#Delta#phi(jet0, p_{T}^{miss})', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
dphi_jet1_ptmiss = {'name':'mydPhi_jet1ptmiss', 'fileName':fileName+'_dphi_jet1_ptmiss'+normString+logString, 'varStr':'dphi_jet1_ptmiss', 'Xtitle':'#Delta#phi(jet1, p_{T}^{miss})', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
mbl = {'name':'mymbl','fileName':fileName+'_m_bl'+normString+logString, 'varStr':'m_bl*0.001', 'Xtitle':'m_{b,l} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
lep_phi = {'name':'mylphi', 'fileName':fileName+'_lep_phi'+normString+logString, 'varStr':'lep_phi', 'Xtitle':'#phi(l)', 'Ytitle':'Events', 'binning':[16,0,3.2], 'binningIsExplicit':False}
lep_eta = {'name':'myleta', 'fileName':fileName+'_lep_eta'+normString+logString, 'varStr':'lep_eta', 'Xtitle':'#eta(l)', 'Ytitle':'Events', 'binning':[32,-3.2,3.2], 'binningIsExplicit':False}
metsig = {'name':'myMET_sig', 'fileName':fileName+'_met_sig'+normString+logString, 'varStr':'met_sig', 'Xtitle':'E_{T}^{miss, sig}', 'Ytitle':'Events', 'binning':[30,0,50], 'binningIsExplicit':False}
htsig ={'name':'myhT_sig', 'fileName':fileName+'_hT_sig'+normString+logString, 'varStr':'ht_sig', 'Xtitle':'h_{T}^{sig}', 'Ytitle':'Events', 'binning':[30,0,50], 'binningIsExplicit':False}
dphi_b_lep_max = {'name':'mydPhi_blepmax', 'fileName':fileName+'_dphi_b_lep_max'+normString+logString, 'varStr':'dphi_b_lep_max', 'Xtitle':'max(#Delta#phi(b, l))', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
dphi_b_ptmiss_max = {'name':'mydPhi_bptmissmax', 'fileName':fileName+'_dphi_b_ptmiss_max'+normString+logString, 'varStr':'dphi_b_ptmiss_max', 'Xtitle':'max(#Delta#phi(b, p_{T}^{miss}))', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
metprojlep = {'name':'myMETprojLEP', 'fileName':fileName+'_met_proj_lep'+normString+logString, 'varStr':'met_proj_lep*0.001', 'Xtitle':'E_{T,l}^{miss} [GeV]', 'Ytitle':'Events', 'binning':[30,0,600], 'binningIsExplicit':False}
dRbjetlep = {'name':'mydRbjetlep', 'fileName':fileName+'_dr_bjet_lep'+normString+logString, 'varStr':'dr_bjet_lep', 'Xtitle':'#DeltaR(b,l)', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
bjetpt0 = {'name':'myBjetpT0','fileName':fileName+'_bjet_pt0'+normString+logString, 'varStr':'bjet_pt[0]*0.001', 'Xtitle':'p_{T}^{bjet0} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[24,0,600], 'binningIsExplicit':False}
bjetpt1 = {'name':'myBjetpT1','fileName':fileName+'_bjet_pt1'+normString+logString, 'varStr':'bjet_pt[1]*0.001', 'Xtitle':'p_{T}^{bjet1} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
mTblMET = {'name':'myMtblMet','fileName':fileName+'_mT_blMET'+normString+logString, 'varStr':'mT_blMET*0.001', 'Xtitle':'m_{T}^{blMET} [GeV]', 'Ytitle':'Events', 'binning':[50,100,700], 'binningIsExplicit':False}
mtopX2 = {'name':'mymtopX2','fileName':fileName+'_m_top_chi2'+normString+logString, 'varStr':'m_top_chi2', 'Xtitle':'m_{top}^{#chi 2} [GeV]', 'Ytitle':'Events', 'binning':[20,0,400], 'binningIsExplicit':False}
mtop = {'name':'mymtop','fileName':fileName+'_m_top_reclustered'+normString+logString, 'varStr':'hadtop_cand_m[0]*0.001', 'Xtitle':'m_{top}^{reclustered} [GeV]', 'Ytitle':'Events', 'binning':[20,0,400], 'binningIsExplicit':False}
output = {'name':'myoutput','fileName':fileName+'_RNN'+normString+logString, 'varStr':'outputScore_RNN', 'Xtitle':'RNN', 'Ytitle':'Events / 0.1', 'binning':[10,0,1], 'binningIsExplicit':False}

## For TRUTH RECO comparison
#dphi = {'name':'mydphi', "fileName":fileName+"_dphi"+normString+logString, 'varStr':"dphi_met_lep", 'Xtitle':'#Delta#Phi(E_{T}^{miss},l)', 'Ytitle':'Events / 0.2', 'binning':[16,0,pi], "binningIsExplicit":False}
#met = {'name':'myMet', "fileName":fileName+"_met"+normString+logString, 'varStr':"met", 'Xtitle':'E_{T}^{miss} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[40,0,1000], "binningIsExplicit":False, "isMeV":True}
#metphi = {'name':'mymetPhi', "fileName":fileName+"_MetPhi"+normString+logString, 'varStr':"met_phi", 'Xtitle':' #phi(#vec{p}_{T}^{miss})', 'Ytitle':'Events / 0.4', 'binning':[16,-pi,pi], "binningIsExplicit":False}
#metx = {'name':'myMetx', "fileName":fileName+"_metX"+normString+logString, 'varStr':"met_x", 'Xtitle':'E_{x}^{miss} [GeV]', 'Ytitle':'Events / 50 GeV', 'binning':[32,-800,800], "binningIsExplicit":False,"isMeV":True}
#mety = {'name':'myMety', "fileName":fileName+"_metY"+normString+logString, 'varStr':"met_y", 'Xtitle':'E_{y}^{miss} [GeV]', 'Ytitle':'Events / 50 GeV', 'binning':[32,-800,800], "binningIsExplicit":False, "isMeV":True}
#mt = {'name':'myMt', "fileName":fileName+"_mt"+normString+logString, 'varStr':"mt", 'Xtitle':'m_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[24,0,600], "binningIsExplicit":False, "isMeV":True}
#ht = {'name':'myHt', "fileName":fileName+"_ht"+normString+logString, 'varStr':"ht", 'Xtitle':'H_{T} [GeV]', 'Ytitle':'Events / 50 GeV', 'binning':[32,0,1600], "binningIsExplicit":False, "isMeV":True}
##met_sig = {'name':'myMetsig', "fileName":fileName+"_met_sig"+normString+logString, 'varStr':"(met_sig)", 'Xtitle':'E_{T}^{miss} sig.', 'Ytitle':'Events', 'binning':[25,0,25], "binningIsExplicit":False, "addCut":" (amt2<110) && (dphi_met_lep<2.5) "}
#ht_sig = {'name':'myHtsig', "fileName":fileName+"_ht_sig"+normString+logString, 'varStr':"(ht_sig)", 'Xtitle':'H_{T} sig.', 'Ytitle':'Events', 'binning':[30,-20,40], "binningIsExplicit":False}
##
##mettruth = {'name':'myMetTruth', "fileName":fileName+"_truthMet"+normString+logString, 'varStr':"(met_truth*0.001)", 'Xtitle':'truth E_{T}^{miss} [GeV]', 'Ytitle':'Events', 'binning':[32,0,800], "binningIsExplicit":False}
#leppt = {'name':'myLepPt', "fileName":fileName+"_lepPt"+normString+logString, 'varStr':"lep_pt[0]", 'Xtitle':'lepton p_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[20,0,500], "binningIsExplicit":False, "isMeV":True}
#lepphi = {'name':'myLepPhi', "fileName":fileName+"_lepPhi"+normString+logString, 'varStr':"lep_phi[0]", 'Xtitle':'lepton #phi', 'Ytitle':'Events / 0.4', 'binning':[16,-pi,pi], "binningIsExplicit":False}
#lepeta = {'name':'myLepEta', "fileName":fileName+"_lepEta"+normString+logString, 'varStr':"lep_eta[0]", 'Xtitle':'lepton #eta', 'Ytitle':'Events / 0.2', 'binning':[25,-2.5,2.5], "binningIsExplicit":False}
#lepe = {'name':'myLepPt', "fileName":fileName+"_lepE"+normString+logString, 'varStr':"lep_e[0]", 'Xtitle':'lepton E [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[32,0,800], "binningIsExplicit":False, "isMeV":True}
#nbjet = {'name':'myNbjet', "fileName":fileName+"_nbjet"+normString+logString, 'varStr':"n_bjet", 'Xtitle':'n_{b-tag}', 'Ytitle':'Events', 'binning':[6,-0.5,5.5], "binningIsExplicit":False}
#njet = {'name':'myNjet', "fileName":fileName+"_njet"+normString+logString, 'varStr':"n_jet", 'Xtitle':'n_{jet}', 'Ytitle':'Events', 'binning':[13,-0.5,12.5], "binningIsExplicit":False}
#truthjet1 = {'name':'myJet1', "fileName":fileName+"_Jetpt0"+normString+logString, 'varStr':"jet_pt[0]", 'Xtitle':'1^{st} jet p_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[40,0,1000], "binningIsExplicit":False, "isMeV":True}
#truthjet2 = {'name':'myJet2', "fileName":fileName+"_Jetpt1"+normString+logString, 'varStr':"jet_pt[1]", 'Xtitle':'2^{nd} jet p_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[32,0,800], "binningIsExplicit":False, "isMeV":True}
#truthjet3 = {'name':'myJet3', "fileName":fileName+"_Jetpt2"+normString+logString, 'varStr':"jet_pt[2]", 'Xtitle':'3^{rd} jet p_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[24,0,600], "binningIsExplicit":False, "isMeV":True}
#
#truthjet4 = {'name':'myJet4', "fileName":fileName+"_Jetpt3"+normString+logString, 'varStr':"jet_pt[3]", 'Xtitle':'4^{th} jet p_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[16,0,400], "binningIsExplicit":False, "isMeV":True}
#truthjete1 = {'name':'myJete1', "fileName":fileName+"_JetE0"+normString+logString, 'varStr':"jet_e[0]", 'Xtitle':'1^{st} jet E [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[40,0,1000], "binningIsExplicit":False, "isMeV":True}
#truthjete2 = {'name':'myJete2', "fileName":fileName+"_JetE1"+normString+logString, 'varStr':"jet_e[1]", 'Xtitle':'2^{nd} jet E [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[32,0,800], "binningIsExplicit":False, "isMeV":True}
#truthjete3 = {'name':'myJete3', "fileName":fileName+"_JetE2"+normString+logString, 'varStr':"jet_e[2]", 'Xtitle':'3^{rd} jet E [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[24,0,600], "binningIsExplicit":False, "isMeV":True}
#
#truthjete4 = {'name':'myJete4', "fileName":fileName+"_JetE3"+normString+logString, 'varStr':"jet_e[3]", 'Xtitle':'4^{th} jet E [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[16,0,400], "binningIsExplicit":False, "isMeV":True}
#truthjeteta1 = {'name':'myJetEta1', "fileName":fileName+"_JetEta0"+normString+logString, 'varStr':"jet_eta[0]", 'Xtitle':'1^{st} jet #eta', 'Ytitle':'Events / 0.2', 'binning':[25,-2.5,2.5], "binningIsExplicit":False}
#truthjeteta2 = {'name':'myJetEta2', "fileName":fileName+"_JetEta1"+normString+logString, 'varStr':"jet_eta[1]", 'Xtitle':'2^{nd} jet #eta', 'Ytitle':'Events / 0.2', 'binning':[25,-2.5,2.5], "binningIsExplicit":False}
#truthjeteta3 = {'name':'myJetEta3', "fileName":fileName+"_JetEta2"+normString+logString, 'varStr':"jet_eta[2]", 'Xtitle':'3^{rd} jet #eta', 'Ytitle':'Events / 0.2', 'binning':[25,-2.5,2.5], "binningIsExplicit":False}
#truthjeteta4 = {'name':'myJetEta4', "fileName":fileName+"_JetEta3"+normString+logString, 'varStr':"jet_eta[3]", 'Xtitle':'4^{th} jet #eta', 'Ytitle':'Events / 0.2', 'binning':[25,-2.5,2.5], "binningIsExplicit":False}
#truthjetphi1 = {'name':'myJetPhi1', "fileName":fileName+"_JetPhi0"+normString+logString, 'varStr':"jet_phi[0]", 'Xtitle':'1^{st} jet #phi', 'Ytitle':'Events / 0.4', 'binning':[16,-pi,pi], "binningIsExplicit":False}
#truthjetphi2 = {'name':'myJetPhi2', "fileName":fileName+"_JetPhi1"+normString+logString, 'varStr':"jet_phi[1]", 'Xtitle':'2^{nd} jet #phi', 'Ytitle':'Events / 0.4', 'binning':[16,-pi,pi], "binningIsExplicit":False}
#truthjetphi3 = {'name':'myJetPhi3', "fileName":fileName+"_JetPhi2"+normString+logString, 'varStr':"jet_phi[2]", 'Xtitle':'3^{rd} jet #phi', 'Ytitle':'Events / 0.4', 'binning':[16,-pi,pi], "binningIsExplicit":False}
#truthjetphi4 = {'name':'myJetPhi4', "fileName":fileName+"_JetPhi3"+normString+logString, 'varStr':"jet_phi[3]", 'Xtitle':'4^{th} jet #phi', 'Ytitle':'Events / 0.4', 'binning':[16,-pi,pi], "binningIsExplicit":False}
#bjet1 = {'name':'myBJet1', "fileName":fileName+"_bJetpt1"+normString+logString, 'varStr':"bjet_pt0", 'Xtitle':'1^{st} b_{jet} p_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[32,0,800], "binningIsExplicit":False}
#bjeteta1 = {'name':'myBJetEta1', "fileName":fileName+"_bJetEta1"+normString+logString, 'varStr':"bjet_eta0", 'Xtitle':'1^{st} b_{jet} #eta', 'Ytitle':'Events / 0.2', 'binning':[25,-2.5,2.5], "binningIsExplicit":False}
#bjetphi1 = {'name':'myBJetPhi1', "fileName":fileName+"_bJetPhi1"+normString+logString, 'varStr':"bjet_phi0", 'Xtitle':'1^{st} b_{jet} #phi', 'Ytitle':'Events / 0.4', 'binning':[16,-pi,pi], "binningIsExplicit":False}
#bjete1 = {'name':'myBJete1', "fileName":fileName+"_bJetE1"+normString+logString, 'varStr':"bjet_e0", 'Xtitle':'1^{st} b_{jet} E [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[32,0,800], "binningIsExplicit":False}
#bjet2 = {'name':'myBJet2', "fileName":fileName+"_bJetpt2"+normString+logString, 'varStr':"bjet_pt1", 'Xtitle':'2^{nd} b_{jet} p_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[16,0,400], "binningIsExplicit":False}
#mbl = {'name':'myMbl', "fileName":fileName+"_m_bl"+normString+logString, 'varStr':"m_bl", 'Xtitle':'m_{bl} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[24,0,600], "binningIsExplicit":False, "isMeV":True}
#output = {'name':'myoutput','fileName':fileName+'_RNN'+normString+logString, 'varStr':'outputScore_RNN', 'Xtitle':'RNN', 'Ytitle':'Events / 0.05', 'binning':[20,0,1], 'binningIsExplicit':False}

#allVariables.append(amt2)
allVariables.append(met)
allVariables.append(metphi)
allVariables.append(mt)
allVariables.append(dphi)
allVariables.append(mbl)
allVariables.append(njet)
allVariables.append(nbjet)
allVariables.append(jet1)
allVariables.append(jet2)
allVariables.append(jet3)
allVariables.append(jet4)
#allVariables.append(truthjete1)
#allVariables.append(truthjete2)
#allVariables.append(truthjete3)
#allVariables.append(truthjete4)
#allVariables.append(truthjeteta1)
#allVariables.append(truthjeteta2)
#allVariables.append(truthjeteta3)
#allVariables.append(truthjeteta4)
#allVariables.append(truthjetphi1)
#allVariables.append(truthjetphi2)
#allVariables.append(truthjetphi3)
#allVariables.append(truthjetphi4)
allVariables.append(output)
#allVariables.append(ntop)
#allVariables.append(metprojlep)
#allVariables.append(htsig)
#allVariables.append(mtopX2)
#allVariables.append(mtop)
allVariables.append(leppt)
#allVariables.append(lepeta)
#allVariables.append(lepphi)
#allVariables.append(lepe)
allVariables.append(bjetpt0)
#allVariables.append(bjeteta1)
#allVariables.append(bjetphi1)
#allVariables.append(bjete1)

histos = {}

for sample in allBkg:
  print sample['name']
  histos[sample['name']] = {}
  for var in allVariables:
    if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
      histos[sample["name"]][var["name"]] = ROOT.TH1F(sample["name"]+"_"+var["name"], sample["name"]+"_"+var["name"], len(var['binning'])-1, array('d', var['binning']))
    else:
      histos[sample["name"]][var["name"]] = ROOT.TH1F(sample["name"]+"_"+var["name"], sample["name"]+"_"+var["name"],*var["binning"])

    if sample.has_key('isTruth') and sample["isTruth"]:
      cut = truth_cut
      weight = truth_weight
    else: 
      cut = reco_cut
      weight = reco_weight
      if var.has_key("isMeV") and var["isMeV"]:
        var["varStr"] = var["varStr"]+"*0.001"
      else:
        var["varStr"] = var["varStr"]
        #var["varStr"] = var["varStr"]+"[0]"
        #var["varStr"] = "bjet_phi[0]"

    if sample.has_key("addCut"):
      cutString = cut+" && "+sample["addCut"]
    else:
      cutString = cut

    if sample.has_key("addWeight"):
      weightString = weight+" * "+sample["addWeight"]
    else:
      weightString = weight

    sample["chain"].Draw(var["varStr"]+">>"+histos[sample["name"]][var["name"]].GetName(), "("+weightString+") * ("+cutString+")","goff")
      
for var in allVariables:
  canv = ROOT.TCanvas(var['name']+'_Window',var['name']+'_Window',600,500)
  if setRatioPlot:
    pad1 = ROOT.TPad('pad1','pad1',0.,0.3,1.,1.)
    pad1.SetBottomMargin(0.018)
    pad1.SetRightMargin(0.08)
  else:
    pad1 = ROOT.TPad('pad1','pad1',0.,0.,1.,1.)
  if setLogY:
    pad1.SetLogy()
  pad1.Draw()
  pad1.cd()
  legend = ROOT.TLegend(0.6,0.9-len(allBkg)*0.06,0.88,0.9)
  PS.legend(legend)

  first = True
  nMax = 0.
  for sample in allBkg:
    print sample['name']
    histos[sample['name']][var['name']].SetLineColor(sample['color'])
    histos[sample['name']][var['name']].SetLineWidth(2)
    #histos[sample['name']][var['name']].SetFillColor(sample['color'])
    histos[sample['name']][var['name']].SetMarkerStyle(20)
    histos[sample['name']][var['name']].SetMarkerColor(sample['color'])
    histos[sample['name']][var['name']].SetMarkerSize(0.85)
    histos[sample['name']][var['name']].GetXaxis().SetTitle(var['Xtitle'])
    histos[sample['name']][var['name']].GetYaxis().SetTitle(var['Ytitle'])# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
    if setRatioPlot:
      histos[sample['name']][var['name']].GetXaxis().SetLabelSize(0.0)
    #histos[sample['name']][var['name']].GetYaxis().SetLabelSize(0.04)
    legend.AddEntry(histos[sample['name']][var['name']], sample['legendName'])
    if normalized:
      histos[sample['name']][var['name']].Scale(1./histos[sample['name']][var['name']].Integral())

    max_tmp = histos[sample['name']][var['name']].GetMaximum()
    if max_tmp > nMax:
      nMax = max_tmp
    if first:
      histos[sample['name']][var['name']].Draw('hist e')
      first = False
    else:
      histos[sample['name']][var['name']].Draw('hist e same')
  for sample in allBkg:
    histos[sample['name']][var['name']].SetMaximum(2*nMax)
    
  legend.Draw()

  canv.cd()

  if setRatioPlot:
    #helpers.ATLASLabelRatioPad(0.18,0.88,"Work in progress")
    #helpers.ATLASLumiLabelRatioPad(0.18,0.84, str(lumi*0.001))
    #ATLASLabel(0.18,0.90,"Work in progress")
    #if not normalized:
    #  ATLASLumiLabel(0.18,0.895, str(lumi*0.001))
    pad2 = ROOT.TPad("pad2","pad2",0.,0.,1.,0.3)
    pad2.SetTopMargin(0.01)
    pad2.SetBottomMargin(0.32)
    pad2.SetRightMargin(0.08)
    pad2.SetGrid()
    pad2.Draw()
    pad2.cd()
  
    ratio1 = doRatio(histos['ttbar1L1tau'][var['name']],histos['ttbar2L'][var['name']], ymin=0.5, ymax=1.6, Xtitle=var['Xtitle'],Ytitle="1/t#bar{t} 2L")
    #ratio2 = doRatio(histos['ttbar_radHi'][var['name']],histos['ttbar'][var['name']], ymin=0.5, ymax=1.6, Xtitle=var['Xtitle'],Ytitle="1/nominal")
    #ratio3 = doRatio(histos['ttbar_radLo'][var['name']],histos['ttbar'][var['name']], ymin=0.5, ymax=1.6, Xtitle=var['Xtitle'],Ytitle="1/nominal")
    #ratio2 = doRatio(histos['stop_bWN_450_300_scup'][var['name']],histos['stop_bWN_450_300_nom'][var['name']], ymin=0.2, ymax=1.8, Xtitle=var['Xtitle'],Ytitle="1/nominal")
    #ratio1 = doRatio(histos['stop_bWN_500_410_scdw'][var['name']],histos['stop_bWN_500_410_nom'][var['name']], ymin=0.2, ymax=1.8, Xtitle=var['Xtitle'],Ytitle="1/nominal")
    #ratio2 = doRatio(histos['stop_bWN_500_410_scup'][var['name']],histos['stop_bWN_500_410_nom'][var['name']], ymin=0.2, ymax=1.8, Xtitle=var['Xtitle'],Ytitle="1/nominal")
    #ratio2 = doRatio(histos['singletop1L'][var['name']],histos['ttbar2L'][var['name']], ymin=-0.5, ymax=2.5, Xtitle=var['Xtitle'],Ytitle="1/t#bar{t} 2L")
    #ratio3 = doRatio(histos['wjets'][var['name']],histos['ttbar2L'][var['name']], ymin=-0.5, ymax=2.5, Xtitle=var['Xtitle'],Ytitle="1/t#bar{t} 2L")
    ratio1.SetMarkerStyle(20)
    ratio1.SetMarkerColor(ratio1.GetLineColor())
    ratio1.SetMarkerSize(0.85)
    #ratio2.SetMarkerStyle(20)
    #ratio2.SetMarkerColor(ratio2.GetLineColor())
    #ratio2.SetMarkerSize(0.85)
    #ratio3.SetMarkerStyle(20)
    #ratio3.SetMarkerColor(ratio3.GetLineColor())
    #ratio3.SetMarkerSize(0.85)
    ratio1.Draw("ep")
    #ratio2.Draw("ep same") 
    #ratio3.Draw("ep same") 
    ROOT.gPad.Modified()
    ROOT.gPad.Update()
    line = ROOT.TLine(ROOT.gPad.GetUxmin(), 1, ROOT.gPad.GetUxmax(), 1)
    line.SetLineStyle(ROOT.kDashed)
    line.SetLineWidth(2)
    line.Draw()

  #else:
  #  pad1.cd()
  #  ATLASLabel(0.18,0.88,"Work in progress")
  #  if not normalized:
  #    ATLASLumiLabel(0.18,0.86, str(lumi*0.001))
  pad1.cd()
  PS.atlas('Work in progress')
  if not normalized:
    PS.sqrts_lumi(13, 140.5, x=0.18)
  PS.string(x=0.18, y=PS.ThirdLine, text="Simulation")

  canv.cd()
  canv.Print(wwwDir+var["fileName"]+".pdf")
  canv.Print(wwwDir+var["fileName"]+".root")
  canv.Print(wwwDir+var["fileName"]+".png")
  canv.Close()
