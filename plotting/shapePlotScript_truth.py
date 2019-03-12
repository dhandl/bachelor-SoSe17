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

wwwDir = "/project/etp5/dhandl/plots/Stop1L/FullRun2/ttbarSystematics/plots/HadFrag/bWN_SR/"

fileName = "bWN_SR"
#fileName = "bWN_SR_shapeComparison_HardScatter"
#fileName = "mt130_met230_shapeComparison_HadFrag_oldPtag"

# setup input directories for TChains
#bkgDir_old = "/eos/atlas/user/j/jkuechle/public/ntuples/" 
#bkgDir = "/eos/atlas/unpledged/group-tokyo/users/toyamaza/stop1L/ntuples/21.2.60/20190124/" 
bkgDir = "/project/etp3/dhandl/samples/SUSY/Stop1L/21.2.60_ML/" 
#sigDir = "/afs/cern.ch/work/d/dhandl/public/Stop1L/syst_truth/" 
#truthDir = "/afs/cern.ch/work/d/dhandl/SUSY/SimpleAnalysis/"
truthDir = "/project/etp3/dhandl/samples/SUSY/Stop1L/TRUTH/"
#truthDir = "/eos/user/d/dhandl/public/ntuples/TRUTH/ttbar_SimpleAnalysis/"
#truthDir = "/afs/cern.ch/work/d/dhandl/SUSY/stop1l-xaod/export/syst_truth/" 
sigDir = "/eos/user/d/dhandl/public/ntuples/20180919/default/"

lumi = 140500.
reco_weight = str(lumi)+" * weight * xs_weight * lumi_weight * sf_total" 
truth_weight = str(lumi)+" * eventWeight * xs_weight" 

reco_cut = "(dphi_jet0_ptmiss>0.4) && (dphi_jet1_ptmiss>0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (n_lep==1) && (lep_pt[0]>=25e3) && (n_bjet>=1)  && (n_jet>=4) && (jet_pt[0]>50e3) && (jet_pt[1]>50e3) && (jet_pt[2]>50e3) && (jet_pt[3]>50e3) && (mt>150e3) && (met>230e3)"

truth_cut = "(dphi_jet0_ptmiss>0.4) && (dphi_jet1_ptmiss>0.4) && !((mt2_tau > -0.5) && (mt2_tau < 80)) && (n_lep==1) && (lep_pt[0]>25) && (n_bjet>=1) && (n_jet>=4) && (jet_pt[0]>25) && (jet_pt[1]>25) && (jet_pt[2]>25) && (jet_pt[3]>25) && (mt>110) && (met>230) && (outputScore_RNN>=0.9) && (outputScore_RNN<1.00)"
#truth_cut = "(n_lep==1) && (n_lep_soft==1) && (n_jet>=2) && (jet0_pt>25) && (jet1_pt>25)"
#cut = "(bWN)"


#----------------------------#
applyFilter = False
if applyFilter:
  truth_cut = truth_cut + " && " + metFilter

#----------------------------#
normalized = False 
if normalized:
  #wwwDir = wwwDir + "normalization/"
  normString = "_norm"
else:
  normString = ""
#----------------------------#
setLogY = False 
if setLogY:
  logString = "_logScale"
  #wwwDir = wwwDir + "logScale/"
else:
  logString = ""
#----------------------------#
setRatioPlot = True 

if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

allBkg = [
#  {"name":"ttv", "legendName":"t#bar{t}+V", "target":bkgDir+"madgraph_ttV/*", "color": ROOT.TColor.GetColor("#E67067"), "chain_name":"madgraph_ttV_Nom"}, 
#  {"name":"diboson", "legendName":"Diboson", "target":bkgDir+"sherpa_diboson/*", "color": ROOT.TColor.GetColor("#54C571"), "chain_name":"sherpa_diboson_Nom"}, 
#  {"name":"singletop", "legendName":"Single top SUSY5", "target":bkgDir+"powheg_singletop/*", "color": ROOT.TColor.GetColor("#82DE68"), "chain_name":"powheg_singletop_Nom", "isTruth":False}, 
#  {"name":"wjets", "legendName":"W+jets", "target":bkgDir+"sherpa22_Wjets/*", "color": ROOT.TColor.GetColor("#FCDD5D"), "chain_name":"sherpa22_Wjets_Nom"}, 
#  {"name":"ttbar1L", "legendName":"t#bar{t} 1L", "target":bkgDir+"powheg_ttbar/*", "color":ROOT.TColor.GetColor("#0F75DB"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==1 || tt_cat==4 || tt_cat==7 )" },
#  {"name":"ttbar2L", "legendName":"t#bar{t} 2L", "target":bkgDir+"powheg_ttbar/*", "color":ROOT.TColor.GetColor("#A5C6E8"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==0 || tt_cat==3 || tt_cat==6 )", "isTruth":False },
#  {"name":"ttbar1L1tau", "legendName":"t#bar{t} 1L1#tau", "target":bkgDir+"powheg_ttbar/*", "color": ROOT.TColor.GetColor("#5E9AD6"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==2 || tt_cat == 5 )", "isTruth":False}, 
#  {"name":"ttbar",              "legendName":"t#bar{t}",           "target":bkgDir+"powheg_ttbar_TRUTH3/*",     "chain_name":"powheg_ttbar_TRUTH3_Nom", "color":ROOT.kBlack, "isTruth":True, "Signal":False},
#  {"name":"ttbar",      "legendName":"t#bar{t}", "target":bkgDir+"powheg_ttbar_TRUTH3/*",     "chain_name":"powheg_ttbar_TRUTH3_Nom", "color":ROOT.kBlack, "isTruth":True, "Signal":False},
#  {"name":"ttbar_radHi",        "legendName":"t#bar{t} radHi",     "target":bkgDir+"ttbar_radHi_TRUTH3/*",      "chain_name":"ttbar_radHi_TRUTH3_Nom", "color":ROOT.kRed, "isTruth":True, "Signal":True},
#  {"name":"ttbar_radLo",        "legendName":"t#bar{t} radLo",     "target":bkgDir+"ttbar_radLo_TRUTH3/*",      "chain_name":"ttbar_radLo_TRUTH3_Nom", "color":ROOT.kBlue, "isTruth":True, "Signal":True},
#  {"name":"ttbar_hpp",          "legendName":"t#bar{t} PwgHpp",    "target":bkgDir+"powheg_hpp_ttbar_TRUTH3/*", "chain_name":"powheg_hpp_ttbar_TRUTH3_Nom", "color":ROOT.kGreen+2, "isTruth":True},
#  {"name":"amcnlo_ttbar",       "legendName":"t#bar{t} aMCNloHpp", "target":bkgDir+"amcnlo_ttbar/*",     "chain_name":"amcnlo_ttbar_Nom", "color":ROOT.kMagenta},
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

  #{"name":"stop_bWN_450_300_nom",    'color':ROOT.kBlack,   "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (nominal)", "target":[truthDir+"stop_bWN_450_300_Systematics/stop_bWN_450_300_truth_nom2/*.root"], "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"2.4926739e-6"},
  #{"name":"stop_bWN_450_300_py3cdw", 'color':ROOT.kBlue,     "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (PS down)", "target":[truthDir+"stop_bWN_450_300_Systematics/stop_bWN_450_300_truth_py3cdw2/*.root"], "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"2.5580223e-6"},
  #{"name":"stop_bWN_450_300_py3cup", 'color':ROOT.kRed,    "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (PS up)", "target":[truthDir+"stop_bWN_450_300_Systematics/stop_bWN_450_300_truth_py3cup2/*.root"], "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"3.0288650e-6"},
  #{"name":"stop_bWN_450_300_qcdw",   'color':ROOT.kGreen+2,"legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (Merging down)", "target":[truthDir+"stop_bWN_450_300_Systematics/stop_bWN_450_300_truth_qcdw2/*.root"], "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"2.2612986e-6"},
  #{"name":"stop_bWN_450_300_qcup",   'color':ROOT.kOrange+7, "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (Merging up)", "target":[truthDir+"stop_bWN_450_300_Systematics/stop_bWN_450_300_truth_qcup2/*.root"], "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"3.2773017e-6"},
  #{"name":"stop_bWN_450_300_scdw",   'color':ROOT.kAzure+6, "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (Fact. down)", "target":[truthDir+"stop_bWN_450_300_Systematics/stop_bWN_450_300_truth_scdw2/*.root"], "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"2.6069763e-6"},
  #{"name":"stop_bWN_450_300_scup",   'color':ROOT.kMagenta, "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300) (Fact. up)", "target":[truthDir+"stop_bWN_450_300_Systematics/stop_bWN_450_300_truth_scup2/*.root"], "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"2.3937855e-6"},

  #{"name":"stop_bWN_500_410_nom", 'color':ROOT.kBlack, "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,410) (nominal)", "target":[truthDir+"stop_bWN_500_410_Systematics/stop_bWN_500_410_truth_nom2/*.root"], "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"1.1721006e-6"},
  #{"name":"stop_bWN_500_410_py3cdw", 'color':ROOT.kBlue, "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,410) (PS down)", "target":[truthDir+"stop_bWN_500_410_Systematics/stop_bWN_500_410_truth_py3cdw2/*.root"], "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"1.1923293e-6"},
  #{"name":"stop_bWN_500_410_py3cup", 'color':ROOT.kRed, "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,410) (PS up)", "target":[truthDir+"stop_bWN_500_410_Systematics/stop_bWN_500_410_truth_py3cup2/*.root"], "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"1.4348189e-6"},
  #{"name":"stop_bWN_500_410_qcdw", 'color':ROOT.kGreen+2, "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,410) (Merging down)", "target":[truthDir+"stop_bWN_500_410_Systematics/stop_bWN_500_410_truth_qcdw2/*.root"], "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"1.0595916e-6"},
  #{"name":"stop_bWN_500_410_qcup", 'color':ROOT.kOrange+7, "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,410) (Merging up)", "target":[truthDir+"stop_bWN_500_410_Systematics/stop_bWN_500_410_truth_qcup2/*.root"], "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"1.2350749e-6"},
  #{"name":"stop_bWN_500_410_scdw", 'color':ROOT.kAzure+6, "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,410) (Fact. down)", "target":[truthDir+"stop_bWN_500_410_Systematics/stop_bWN_500_410_truth_scdw2/*.root"], "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"1.2263233e-6"},
  #{"name":"stop_bWN_500_410_scup", 'color':ROOT.kMagenta, "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,410) (Fact. up)", "target":[truthDir+"stop_bWN_500_410_Systematics/stop_bWN_500_410_truth_scup2/*.root"], "chain_name":"StopOneLepton2016__ntuple", "isTruth":True, "addWeight":"1.1214690e-6"},


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

{"name":"ttbar", "legendName":"t#bar{t} nominal (Truth)", "target":[truthDir+"/ttbar_nom/*.root"], "color": ROOT.kBlack, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True},
{"name":"ttbar_phh7", "legendName":"t#bar{t} Pow+H7 (Truth)", "target":[truthDir+"/ttbar_PhH7/*.root"], "color": ROOT.kRed, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True},
#{"name":"ttbar_amcpy8", "legendName":"t#bar{t} aMC@NLO+Py8 (Truth)", "target":[truthDir+"/ttbar_aMCPy8/*.root"], "color": ROOT.kRed, "chain_name":"StopOneLepton2016__ntuple", "isTruth":True},
#{"name":"ttbar", "legendName":"t#bar{t} 1L (Reco mc16d)", "target":bkgDir+"mc16d_ttbar/*.root", "color": ROOT.kBlue, "chain_name":"ttbar_Nom", "isTruth":False, "addCut":"( tt_cat==1 || tt_cat==4 || tt_cat>=7 )"},
#{"name":"ttbar", "legendName":"t#bar{t} (Reco)", "target":[bkgDir+"mc16a_ttbar/*.root",bkgDir+"mc16d_ttbar/*.root",bkgDir+"mc16e_ttbar/*.root"], "color": ROOT.kBlue, "chain_name":"ttbar_Nom", "isTruth":False},
#{"name":"ttbar_old", "legendName":"t#bar{t} (Reco mc15)", "target":bkgDir_old+"powheg_ttbar/*", "chain_name":"powheg_ttbar_Nom", "color":ROOT.kRed, "isTruth":False, "addCut":"( tt_cat==1 || tt_cat==4 || tt_cat==7 )"},
]

for i, sample in enumerate(allBkg):
  sample["chain"] = ROOT.TChain(sample["chain_name"])
  for target in sample['target']:
    sample["chain"].Add(target)
  #if sample.has_key("isTruth") and sample["isTruth"]:
  #  sample["chain"].SetAlias("Met", "met*1000.")
  #  sample["chain"].SetAlias("Met_x", "met_x*1000.")
  #  sample["chain"].SetAlias("Met_y", "met_y*1000.")
  #  sample["chain"].SetAlias("Mt", "mt*1000.")
  #  sample["chain"].SetAlias("Ht", "ht*1000.")
  #  sample["chain"].SetAlias("lep_pt[0]", "lep_pt*1000.")
  #  sample["chain"].SetAlias("lep_eta[0]", "lep_eta")
  #  sample["chain"].SetAlias("lep_phi[0]", "lep_phi")
  #  sample["chain"].SetAlias("jet_pt[0]", "jet0_pt*1000.")
  #  sample["chain"].SetAlias("jet_eta[0]", "jet0_eta")
  #  sample["chain"].SetAlias("jet_phi[0]", "jet0_phi")
  #  sample["chain"].SetAlias("jet_pt[1]", "jet1_pt*1000.")
  #  sample["chain"].SetAlias("jet_eta[1]", "jet1_eta")
  #  sample["chain"].SetAlias("jet_phi[1]", "jet1_phi")
  #  sample["chain"].SetAlias("jet_pt[2]", "jet2_pt*1000.")
  #  sample["chain"].SetAlias("jet_eta[2]", "jet2_eta")
  #  sample["chain"].SetAlias("jet_phi[2]", "jet2_phi")
  #  sample["chain"].SetAlias("jet_pt[3]", "jet3_pt*1000.")
  #  sample["chain"].SetAlias("jet_eta[3]", "jet3_eta")
  #  sample["chain"].SetAlias("jet_phi[3]", "jet3_phi")
  #  sample["chain"].SetAlias("bjet_pt[0]", "bjet_pt0*1000.")
  #  sample["chain"].SetAlias("bjet_eta[0]", "bjet_eta0")
  #  sample["chain"].SetAlias("bjet_phi[0]", "bjet_phi0")
  #  sample["chain"].SetAlias("bjet_pt[1]", "bjet_pt1*1000.")
  #else:
  #  sample["chain"].SetAlias("Met", "met")
  #  sample["chain"].SetAlias("Met_x", "met_x")
  #  sample["chain"].SetAlias("Met_y", "met_y")
  #  sample["chain"].SetAlias("Mt", "mt")
  #  sample["chain"].SetAlias("Ht", "ht")



allVariables = []
#amt2 = {'name':'myAmt2', "fileName":fileName+"_amt2"+normString+logString, 'varStr':"amt2", 'Xtitle':'am_{T2}', 'Ytitle':'Events', 'binning':[80,90,100,110,120,170,250,350,600], "binningIsExplicit":True}
amt2 = {'name':'myAmt2', "fileName":fileName+"_amt2"+normString+logString, 'varStr':"amt2", 'Xtitle':'am_{T2} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[20,0,500], "binningIsExplicit":False}
dphi = {'name':'mydphi', "fileName":fileName+"_dphi"+normString+logString, 'varStr':"dphi_met_lep", 'Xtitle':'#Delta#Phi(E_{T}^{miss},l)', 'Ytitle':'Events / 0.2', 'binning':[16,0,3.2], "binningIsExplicit":False}
met = {'name':'myMet', "fileName":fileName+"_met"+normString+logString, 'varStr':"met", 'Xtitle':'E_{T}^{miss} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[35,200,1600], "binningIsExplicit":False, "isMeV":True}
genmet = {'name':'myGenMet', "fileName":fileName+"_genmet"+normString+logString, 'varStr':"genMet", 'Xtitle':'Gen. E_{T}^{miss} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[48,400,1600], "binningIsExplicit":False, "isMeV":True}
metphi = {'name':'mymetPhi', "fileName":fileName+"_MetPhi"+normString+logString, 'varStr':"met_phi", 'Xtitle':' #phi(#vec{p}_{T}^{miss})', 'Ytitle':'Events', 'binning':[16,-pi,pi], "binningIsExplicit":False}
metx = {'name':'myMetx', "fileName":fileName+"_metX"+normString+logString, 'varStr':"met_x", 'Xtitle':'E_{x}^{miss} [GeV]', 'Ytitle':'Events / 50 GeV', 'binning':[32,-800,800], "binningIsExplicit":False,"isMeV":True}
mety = {'name':'myMety', "fileName":fileName+"_metY"+normString+logString, 'varStr':"met_y", 'Xtitle':'E_{y}^{miss} [GeV]', 'Ytitle':'Events / 50 GeV', 'binning':[32,-800,800], "binningIsExplicit":False, "isMeV":True}
mt = {'name':'myMt', "fileName":fileName+"_mt"+normString+logString, 'varStr':"mt", 'Xtitle':'m_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[28,0,700], "binningIsExplicit":False, "isMeV":True}
ht = {'name':'myHt', "fileName":fileName+"_ht"+normString+logString, 'varStr':"ht", 'Xtitle':'H_{T} [GeV]', 'Ytitle':'Events / 50 GeV', 'binning':[32,0,1600], "binningIsExplicit":False, "isMeV":True}
#met_sig = {'name':'myMetsig', "fileName":fileName+"_met_sig"+normString+logString, 'varStr':"(met_sig)", 'Xtitle':'E_{T}^{miss} sig.', 'Ytitle':'Events', 'binning':[25,0,25], "binningIsExplicit":False, "addCut":" (amt2<110) && (dphi_met_lep<2.5) "}
ht_sig = {'name':'myHtsig', "fileName":fileName+"_ht_sig"+normString+logString, 'varStr':"(ht_sig)", 'Xtitle':'H_{T} sig.', 'Ytitle':'Events', 'binning':[30,-20,40], "binningIsExplicit":False}
#
#mettruth = {'name':'myMetTruth', "fileName":fileName+"_truthMet"+normString+logString, 'varStr':"(met_truth*0.001)", 'Xtitle':'truth E_{T}^{miss} [GeV]', 'Ytitle':'Events', 'binning':[32,0,800], "binningIsExplicit":False}
leppt = {'name':'myLepPt', "fileName":fileName+"_lepPt"+normString+logString, 'varStr':"lep_pt[0]", 'Xtitle':'lepton p_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[20,0,500], "binningIsExplicit":False, "isMeV":True}
lepphi = {'name':'myLepPhi', "fileName":fileName+"_lepPhi"+normString+logString, 'varStr':"lep_phi[0]", 'Xtitle':'lepton #phi', 'Ytitle':'Events', 'binning':[16,-pi,pi], "binningIsExplicit":False}
lepeta = {'name':'myLepEta', "fileName":fileName+"_lepEta"+normString+logString, 'varStr':"lep_eta[0]", 'Xtitle':'lepton #eta', 'Ytitle':'Events', 'binning':[25,-2.5,2.5], "binningIsExplicit":False}
nbjet = {'name':'myNbjet', "fileName":fileName+"_nbjet"+normString+logString, 'varStr':"n_bjet", 'Xtitle':'b-jet multiplicity', 'Ytitle':'Events', 'binning':[9,-0.5,8.5], "binningIsExplicit":False}

njet = {'name':'myNjet', "fileName":fileName+"_njet"+normString+logString, 'varStr':"n_jet", 'Xtitle':'jet multiplicity', 'Ytitle':'Events', 'binning':[13,-0.5,12.5], "binningIsExplicit":False}
truthjet1 = {'name':'myJet1', "fileName":fileName+"_Jetpt1"+normString+logString, 'varStr':"jet_pt[0]", 'Xtitle':'1^{st} jet p_{T} [GeV]', 'Ytitle':'Events / 40 GeV', 'binning':[25,0,1000], "binningIsExplicit":False, "isMeV":True}
truthjet2 = {'name':'myJet2', "fileName":fileName+"_Jetpt2"+normString+logString, 'varStr':"jet_pt[1]", 'Xtitle':'2^{nd} jet p_{T} [GeV]', 'Ytitle':'Events / 40 GeV', 'binning':[32,0,800], "binningIsExplicit":False, "isMeV":True}

truthjet3 = {'name':'myJet3', "fileName":fileName+"_Jetpt3"+normString+logString, 'varStr':"jet_pt[2]", 'Xtitle':'3^{rd} jet p_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[24,0,600], "binningIsExplicit":False, "isMeV":True}

truthjet4 = {'name':'myJet4', "fileName":fileName+"_Jetpt4"+normString+logString, 'varStr':"jet_pt[3]", 'Xtitle':'4^{th} jet p_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[16,0,400], "binningIsExplicit":False, "isMeV":True}
truthjeteta1 = {'name':'myJetEta1', "fileName":fileName+"_JetEta1"+normString+logString, 'varStr':"jet_eta[0]", 'Xtitle':'1^{st} jet #eta', 'Ytitle':'Events', 'binning':[25,-2.5,2.5], "binningIsExplicit":False}
truthjeteta2 = {'name':'myJetEta2', "fileName":fileName+"_JetEta2"+normString+logString, 'varStr':"jet_eta[1]", 'Xtitle':'2^{nd} jet #eta', 'Ytitle':'Events', 'binning':[25,-2.5,2.5], "binningIsExplicit":False}
truthjeteta3 = {'name':'myJetEta3', "fileName":fileName+"_JetEta3"+normString+logString, 'varStr':"jet_eta[2]", 'Xtitle':'3^{rd} jet #eta', 'Ytitle':'Events', 'binning':[25,-2.5,2.5], "binningIsExplicit":False}
truthjeteta4 = {'name':'myJetEta4', "fileName":fileName+"_JetEta4"+normString+logString, 'varStr':"jet_eta[3]", 'Xtitle':'4^{th} jet #eta', 'Ytitle':'Events', 'binning':[25,-2.5,2.5], "binningIsExplicit":False}
truthjetphi1 = {'name':'myJetPhi1', "fileName":fileName+"_JetPhi1"+normString+logString, 'varStr':"jet_phi[0]", 'Xtitle':'1^{st} jet #phi', 'Ytitle':'Events', 'binning':[16,-pi,pi], "binningIsExplicit":False}
truthjetphi2 = {'name':'myJetPhi2', "fileName":fileName+"_JetPhi2"+normString+logString, 'varStr':"jet_phi[1]", 'Xtitle':'2^{nd} jet #phi', 'Ytitle':'Events', 'binning':[16,-pi,pi], "binningIsExplicit":False}
truthjetphi3 = {'name':'myJetPhi3', "fileName":fileName+"_JetPhi3"+normString+logString, 'varStr':"jet_phi[2]", 'Xtitle':'3^{rd} jet #phi', 'Ytitle':'Events', 'binning':[16,-pi,pi], "binningIsExplicit":False}
truthjetphi4 = {'name':'myJetPhi4', "fileName":fileName+"_JetPhi4"+normString+logString, 'varStr':"jet_phi[3]", 'Xtitle':'4^{th} jet #phi', 'Ytitle':'Events', 'binning':[16,-pi,pi], "binningIsExplicit":False}
#
#truthjetetatotal = {'name':'myJetEtaTotal', "fileName":fileName+"_truthSignalJetEtaTotal"+normString+logString, 'varStr':"(jet_eta)", 'Xtitle':'jet #eta (incl. all truth signal jets)', 'Ytitle':'Events', 'binning':[20,-2.5,2.5], "binningIsExplicit":False}
#truthjetpttotal = {'name':'myJetPtTotal', "fileName":fileName+"_truthSignalJetPtTotal"+normString+logString, 'varStr':"(jet_pt*0.001)", 'Xtitle':'jet p_{T} [GeV] (incl. all truth signal jets)', 'Ytitle':'Events', 'binning':[25,0,600], "binningIsExplicit":False}
#truthjetphitotal = {'name':'myJetPhiTotal', "fileName":fileName+"_truthSignalJetPhiTotal"+normString+logString, 'varStr':"(jet_phi)", 'Xtitle':'jet #phi (incl. all truth signal jets)', 'Ytitle':'Events', 'binning':[15,0,3.2], "binningIsExplicit":False}
#truthjetetotal = {'name':'myJetETotal', "fileName":fileName+"_truthSignalJetETotal"+normString+logString, 'varStr':"(jet_e*0.001)", 'Xtitle':'jet E [GeV] (incl. all truth signal jets)', 'Ytitle':'Events', 'binning':[45,0,1800], "binningIsExplicit":False}
#truthjetmtotal = {'name':'myJetMTotal', "fileName":fileName+"_truthSignalJetMTotal"+normString+logString, 'varStr':"(jet_m*0.001)", 'Xtitle':'jet m [GeV] (incl. all truth signal jets)', 'Ytitle':'Events', 'binning':[14,0,140], "binningIsExplicit":False}
bjet0 = {'name':'myBJet1', "fileName":fileName+"_bJetpt0"+normString+logString, 'varStr':"bjet_pt0", 'Xtitle':'1^{st} b_{jet} p_{T} [GeV]', 'Ytitle':'Events / 40 GeV', 'binning':[20,0,800], "binningIsExplicit":False}
bjeteta0 = {'name':'myBJetEta1', "fileName":fileName+"_bJetEta1"+normString+logString, 'varStr':"bjet_eta0", 'Xtitle':'1^{st} b_{jet} #eta', 'Ytitle':'Events', 'binning':[25,-2.5,2.5], "binningIsExplicit":False}
bjetphi0 = {'name':'myBJetPhi1', "fileName":fileName+"_bJetPhi1"+normString+logString, 'varStr':"bjet_phi0", 'Xtitle':'1^{st} b_{jet} #phi', 'Ytitle':'Events', 'binning':[16,-pi,pi], "binningIsExplicit":False}
bjet1 = {'name':'myBJet2', "fileName":fileName+"_bJetpt2"+normString+logString, 'varStr':"bjet_pt1", 'Xtitle':'2^{nd} b_{jet} p_{T} [GeV]', 'Ytitle':'Events', 'binning':[16,0,400], "binningIsExplicit":False}
mbl = {'name':'myMbl', "fileName":fileName+"_m_bl"+normString+logString, 'varStr':"m_bl", 'Xtitle':'m_{bl} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[24,0,600], "binningIsExplicit":False, "isMeV":True}
#truthjetdrtotal = {'name':'mydrJetTotal', "fileName":fileName+"_truthDrJetTotal"+normString+logString, 'varStr':"(jet_deltaRj)", 'Xtitle':'#Delta R(jet, jet) (incl. all truth signal jets)', 'Ytitle':'Events', 'binning':[25,0,5], "binningIsExplicit":False}
#truthdphilepjettotal = {'name':'mydphiLepJetTotal', "fileName":fileName+"_truthDphiLepJetTotal"+normString+logString, 'varStr':"(truth_signaljet_dphilep)", 'Xtitle':'#Delta #phi (lep,jet) (incl. all truth signal jets)', 'Ytitle':'Events', 'binning':[15,0,3.2], "binningIsExplicit":False}

#closestdrlepjet = {'name':'myclosestdrLepJetTotal', "fileName":fileName+"_closestDrLepJet"+normString+logString, 'varStr':"(dr_lep_jet_min)", 'Xtitle':'min. #Delta R(lep, jet)', 'Ytitle':'Events', 'binning':[25,0,5], "binningIsExplicit":False}
#closestdphilepjet = {'name':'myclosestdphiLepJetTotal', "fileName":fileName+"_closestDphiLepJet"+normString+logString, 'varStr':"(dphi_lep_jet_min)", 'Xtitle':'min. #Delta #phi (lep, jet)', 'Ytitle':'Events', 'binning':[30,-3.2,3.2], "binningIsExplicit":False}
#maxdrlepjet = {'name':'mymaxdrLepJetTotal', "fileName":fileName+"_maxDrLepJetTotal"+normString+logString, 'varStr':"(dr_lep_jet_max)", 'Xtitle':'max. #Delta R(lep, jet)', 'Ytitle':'Events', 'binning':[25,0,5], "binningIsExplicit":False}
#maxdphilepjet = {'name':'mymaxdphiLepJetTotal', "fileName":fileName+"_maxDphiLepJetTotal"+normString+logString, 'varStr':"(dphi_lep_jet_max)", 'Xtitle':'max. #Delta #phi (lep, jet)', 'Ytitle':'Events', 'binning':[30,-3.2,3.2], "binningIsExplicit":False}
#closestdrjj = {'name':'myclosestdrJJTotal', "fileName":fileName+"_closestDrJetJet"+normString+logString, 'varStr':"(dr_jet_jet_min)", 'Xtitle':'min. #Delta R_{jj}', 'Ytitle':'Events', 'binning':[25,0,5], "binningIsExplicit":False}
#closestdphijj = {'name':'myclosestdphiJJTotal', "fileName":fileName+"_closestDphiJetJet"+normString+logString, 'varStr':"(dphi_jet_jet_min)", 'Xtitle':'min. #Delta #phi_{jj}', 'Ytitle':'Events', 'binning':[30,-3.3,3.2], "binningIsExplicit":False}
#maxdrjj = {'name':'mymaxdrJJTotal', "fileName":fileName+"_maxDrJetJetTotal"+normString+logString, 'varStr':"(dr_jet_jet_max)", 'Xtitle':'max. #Delta R_{jj}', 'Ytitle':'Events', 'binning':[25,0,5], "binningIsExplicit":False}
#maxdphijj = {'name':'mymaxdphiJJTotal', "fileName":fileName+"_maxDphiJetJet"+normString+logString, 'varStr':"(dphi_jet_jet_max)", 'Xtitle':'max. #Delta #phi_{jj}', 'Ytitle':'Events', 'binning':[30,-3.2,3.2], "binningIsExplicit":False}
#
#closestdetalepjet = {'name':'myclosestdetaLepJetTotal', "fileName":fileName+"_closestDetaLepJet"+normString+logString, 'varStr':"(deta_lep_jet_min)", 'Xtitle':'min. #Delta #eta (lep, jet)', 'Ytitle':'Events', 'binning':[40,-5,5], "binningIsExplicit":False}
#maxdetalepjet = {'name':'mymaxdetaLepJetTotal', "fileName":fileName+"_maxDetaLepJet"+normString+logString, 'varStr':"(deta_lep_jet_max)", 'Xtitle':'max. #Delta #eta (lep, jet)', 'Ytitle':'Events', 'binning':[40,-5,5], "binningIsExplicit":False}
#closestdetajetjet = {'name':'myclosestdetaJetJetTotal', "fileName":fileName+"_closestDetaJetJet"+normString+logString, 'varStr':"(deta_jet_jet_min)", 'Xtitle':'min. #Delta #eta (jet, jet)', 'Ytitle':'Events', 'binning':[40,-5,5], "binningIsExplicit":False}
#maxdetajetjet = {'name':'mymaxdetaJetJetTotal', "fileName":fileName+"_maxDetaJetJet"+normString+logString, 'varStr':"(deta_jet_jet_max)", 'Xtitle':'max. #Delta #eta (jet, jet)', 'Ytitle':'Events', 'binning':[40,-5,5], "binningIsExplicit":False}
#mjj = {'name':'myMjj', "fileName":fileName+"_M_j1j2"+normString+logString, 'varStr':"(m_jet1_jet2*0.001)", 'Xtitle':'m_{j_{1}j_{2}} [GeV]', 'Ytitle':'Events', 'binning':[30,0,1500], "binningIsExplicit":False}
#maxmjj = {'name':'mymaxMjj', "fileName":fileName+"_maxMjj"+normString+logString, 'varStr':"(m_jet_jet_max*0.001)", 'Xtitle':'max. m_{jj} [GeV]', 'Ytitle':'Events', 'binning':[32,0,1800], "binningIsExplicit":False}
#minmjj = {'name':'myminMjj', "fileName":fileName+"_minMjj"+normString+logString, 'varStr':"(m_jet_jet_min*0.001)", 'Xtitle':'min. m_{jj} [GeV]', 'Ytitle':'Events', 'binning':[20,0,500], "binningIsExplicit":False}
#
#
#mtt = {'name':'myMtt', "fileName":fileName+"_M_ttbar"+normString+logString, 'varStr':"(ttbar_m*0.001)", 'Xtitle':'m_{t#bar{t}} [GeV]', 'Ytitle':'Events', 'binning':[40,0,4000], "binningIsExplicit":False}
#pttt = {'name':'myPttt', "fileName":fileName+"_Pt_ttbar"+normString+logString, 'varStr':"(ttbar_pt*0.001)", 'Xtitle':'p_{T}^{t#bar{t}} [GeV]', 'Ytitle':'Events', 'binning':[30,0,1500], "binningIsExplicit":False}
#dphitt = {'name':'myDphitt', "fileName":fileName+"_dphi_ttbar"+normString+logString, 'varStr':"(ttbar_dphi)", 'Xtitle':'#Delta#Phi_{t#bar{t}} [GeV]', 'Ytitle':'Events', 'binning':[30,-3.15,3.15], "binningIsExplicit":False}
output = {'name':'myoutput','fileName':fileName+'_RNN'+normString+logString, 'varStr':'outputScore_RNN', 'Xtitle':'RNN', 'Ytitle':'Events / 0.1', 'binning':[10,0,1], 'binningIsExplicit':False}

#allVariables.append(amt2)
allVariables.append(met)
allVariables.append(metphi)
allVariables.append(mt)
allVariables.append(dphi)
#allVariables.append(genmet)
#allVariables.append(metx)
#allVariables.append(mety)
#allVariables.append(ht)
#allVariables.append(mtt)
#allVariables.append(pttt)
#allVariables.append(dphitt)
#allVariables.append(ht_sig)
#allVariables.append(met_sig)
allVariables.append(njet)
allVariables.append(leppt)
allVariables.append(lepeta)
allVariables.append(lepphi)
#allVariables.append(mettruth)
allVariables.append(nbjet)
allVariables.append(bjet0)
#allVariables.append(bjeteta1)
#allVariables.append(bjetphi1)
#allVariables.append(bjet2)
#allVariables.append(truthjet1)
#allVariables.append(truthjet2)
#allVariables.append(truthjet3)
#allVariables.append(truthjet4)
#allVariables.append(truthjeteta1)
#allVariables.append(truthjeteta2)
#allVariables.append(truthjeteta3)
#allVariables.append(truthjeteta4)
#allVariables.append(truthjetphi1)
#allVariables.append(truthjetphi2)
#allVariables.append(truthjetphi3)
#allVariables.append(truthjetphi4)
#allVariables.append(mbl)
#allVariables.append(truthjetetatotal)
#allVariables.append(truthjetpttotal)
#allVariables.append(truthjetphitotal)
#allVariables.append(truthjetetotal)
#allVariables.append(truthjetmtotal)
#allVariables.append(closestdrlepjet)
#allVariables.append(closestdphilepjet)
#allVariables.append(maxdrlepjet)
#allVariables.append(maxdphilepjet)
#allVariables.append(closestdrjj)
#allVariables.append(closestdphijj)
#allVariables.append(maxdrjj)
#allVariables.append(maxdphijj)
#allVariables.append(closestdetalepjet)
#allVariables.append(maxdetalepjet)
#allVariables.append(closestdetajetjet)
#allVariables.append(maxdetajetjet)
#allVariables.append(mjj)
#allVariables.append(maxmjj)
#allVariables.append(minmjj)
#allVariables.append(truthjetdrtotal)
#allVariables.append(output)

histos = {}

for sample in allBkg:
  print sample['name']
  histos[sample['name']] = {}
  for var in allVariables:
    if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
      histos[sample["name"]][var["name"]] = ROOT.TH1F(sample["name"]+"_"+var["name"], sample["name"]+"_"+var["name"], len(var['binning'])-1, array('d', var['binning']))
    else:
      histos[sample["name"]][var["name"]] = ROOT.TH1F(sample["name"]+"_"+var["name"], sample["name"]+"_"+var["name"],*var["binning"])

    if sample.has_key("isTruth") and sample["isTruth"]:
      cut = truth_cut
      weight = truth_weight
    else: 
      cut = reco_cut
      weight = reco_weight
      if var.has_key("isMeV") and var["isMeV"]:
        var["varStr"] = var["varStr"]+"*0.001"
        #var["varStr"] = "gen_filter_met*0.001"
      else:
        var["varStr"] = var["varStr"]
      #var["varStr"] = var["varStr"]+"[0]"
      #var["varStr"] = "jet_pt[0]*0.001"

    if sample.has_key("addCut"):
      cutString = cut+" && "+sample["addCut"]
    else:
      cutString = cut

    if sample.has_key("addWeight"):
      weightString = weight+" * "+sample["addWeight"]
    else:
      weightString = weight

    sample["chain"].Draw(var["varStr"]+">>"+histos[sample["name"]][var["name"]].GetName(), "("+weightString+") * ("+cutString+")","goff")
    histos[sample["name"]][var["name"]].SetDirectory(0)
      
for var in allVariables:
  print "Plotting: ",var['name'] 
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
  legend = ROOT.TLegend(0.6, 0.9-len(allBkg)*0.05, 0.9, 0.9)
  PS.legend(legend)
  legend = ROOT.TLegend(0.65,0.7,0.9,0.9)
  legend.SetFillColor(0)
  legend.SetBorderSize(0)
  legend.SetShadowColor(ROOT.kWhite)
  #stack = ROOT.THStack('stack','Stacked Histograms')

  first = True
  nMax = 0.
  for sample in allBkg:
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
    #stack.Add(histos[sample['name']][var['name']])
    if sample.has_key("Signal") and sample["Signal"]:
      sample["sep"] = getSeparation(histos["stop_bWN_450_300_truth"][var["name"]], histos[sample["name"]][var["name"]])
      legend.AddEntry(histos[sample['name']][var['name']], "%s (<S^{2}> = %.3f%%)"%(sample['legendName'],sample["sep"]*100))
    else:
      legend.AddEntry(histos[sample['name']][var['name']], sample['legendName'])
      
    if normalized:
      print sample['name']
      histos[sample['name']][var['name']].Scale(1./histos[sample['name']][var['name']].Integral())
      histos[sample['name']][var['name']].GetYaxis().SetTitle('a. u.')

    max_tmp = histos[sample['name']][var['name']].GetMaximum()
    if max_tmp > nMax:
      nMax = max_tmp
    if first:
      if setLogY:
        histos[sample['name']][var['name']].SetMaximum(100*histos[sample['name']][var['name']].GetMaximum())
        histos[sample['name']][var['name']].SetMinimum(0.1)
        if normalized:
          histos[sample['name']][var['name']].SetMaximum(1.2)
          histos[sample['name']][var['name']].SetMinimum(2e-5)
      else:
        histos[sample['name']][var['name']].SetMaximum(1.7*histos[sample['name']][var['name']].GetMaximum())
      histos[sample['name']][var['name']].Draw('hist e')
      first = False
    else:
      histos[sample['name']][var['name']].Draw('hist e same')
         
  #stack.Draw('hist')
  #stack.GetXaxis().SetTitle(var['Xtitle'])
  #stack.GetYaxis().SetTitle(var['Ytitle'])# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
  #if setLogY:
  #  histos['ttbar2L'][var['name']].SetMinimum(10**(-1))
  #  histos['ttbar2L'][var['name']].SetMaximum(100*nMax)
  #else:
  #  histos['ttbar2L'][var['name']].SetMinimum(0.)
  #  histos['ttbar2L'][var['name']].SetMaximum(40.)

#  for sig in allSignal:
#    histos[sig['name']][var['name']].SetLineColor(sig['color'])
#    histos[sig['name']][var['name']].SetLineWidth(2)
#    histos[sig['name']][var['name']].SetLineStyle(ROOT.kDashed)
#    histos[sig['name']][var['name']].SetFillColor(0)
#    histos[sig['name']][var['name']].SetMarkerStyle(0)
#    histos[sig['name']][var['name']].Draw('hist same')
#    legend.AddEntry(histos[sig['name']][var['name']], sig['legendName'])
                        
  legend.Draw()

  canv.cd()

  if setRatioPlot:
    #helpers.ATLASLabelRatioPad(0.18,0.88,"Work in progress")
    #helpers.ATLASLumiLabelRatioPad(0.18,0.84, str(lumi*0.001))
    #ATLASLabel(0.18,0.90,"Work in progress")
    #if not normalized:
    #  ATLASLumiLabel(0.18,0.895,str(lumi*0.001))
    pad2 = ROOT.TPad("pad2","pad2",0.,0.,1.,0.3)
    pad2.SetTopMargin(0.01)
    pad2.SetBottomMargin(0.32)
    pad2.SetRightMargin(0.08)
    pad2.SetGrid()
    pad2.Draw()
    pad2.cd()
  
    #ratio0 = doRatio(histos['ttbar'][var['name']],histos['ttbar'][var['name']], ymin=0.6, ymax=1.45, Xtitle=var['Xtitle'],Ytitle="1/t#bar{t}")
    ratio1 = doRatio(histos['ttbar_phh7'][var['name']],histos['ttbar'][var['name']], ymin=0.2, ymax=1.85, Xtitle=var['Xtitle'],Ytitle="1/nominal")
    #ratio1 = doRatio(histos['ttbar_amcpy8'][var['name']],histos['ttbar'][var['name']], ymin=0.2, ymax=1.85, Xtitle=var['Xtitle'],Ytitle="1/truth")
    #ratio1 = doRatio(histos['stop_bWN_500_410_py3cdw'][var['name']],histos['stop_bWN_500_410_nom'][var['name']], ymin=0.2, ymax=1.85, Xtitle=var['Xtitle'],Ytitle="1/nominal")
    #ratio2 = doRatio(histos['stop_bWN_500_410_py3cup'][var['name']],histos['stop_bWN_500_410_nom'][var['name']], ymin=0.2, ymax=1.85, Xtitle=var['Xtitle'],Ytitle="1/nominal")
    #ratio3 = doRatio(histos['ttbar400'][var['name']],histos['ttbar'][var['name']], ymin=-0.5, ymax=2.5, Xtitle=var['Xtitle'],Ytitle="1/t#bar{t}")
    #ratio4 = doRatio(histos['amcnlo_ttbar'][var['name']],histos['ttbar'][var['name']], ymin=-0.5, ymax=2.5, Xtitle=var['Xtitle'],Ytitle="1/t#bar{t}")
    ratio1.SetMarkerStyle(20)
    ratio1.SetMarkerColor(ratio1.GetLineColor())
    ratio1.SetMarkerSize(0.85)
    #ratio2.SetMarkerStyle(20)
    #ratio2.SetMarkerColor(ratio2.GetLineColor())
    #ratio2.SetMarkerSize(0.85)
    #ratio3.SetMarkerStyle(20)
    #ratio3.SetMarkerColor(ratio3.GetLineColor())
    #ratio3.SetMarkerSize(0.85)
    #ratio4.SetMarkerStyle(20)
    #ratio4.SetMarkerColor(ratio4.GetLineColor())
    #ratio4.SetMarkerSize(0.85)
    #ratio0.Draw("e2")
    ratio1.Draw("ep")
    #ratio2.Draw("ep same") 
    #ratio3.Draw("ep same") 
    #ratio4.Draw("ep same") 
    ROOT.gPad.Modified()
    ROOT.gPad.Update()
    line = ROOT.TLine(ROOT.gPad.GetUxmin(), 1.0, ROOT.gPad.GetUxmax(), 1.0)
    line.SetLineStyle(ROOT.kDashed)
    line.SetLineWidth(3)
    line.Draw()

  pad1.cd()
  PS.atlas('Work in progress')
  if not normalized:
    PS.sqrts_lumi(13, 140.5, x=0.18)
  PS.string(x=0.18, y=PS.ThirdLine, text="Simulation")

  canv.cd()
  canv.Print(wwwDir+var["fileName"]+".pdf")
  canv.Print(wwwDir+var["fileName"]+".root")
  canv.Print(wwwDir+var["fileName"]+".png")
