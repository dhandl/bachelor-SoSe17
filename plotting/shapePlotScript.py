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
  h1.GetYaxis().SetTitleSize(23)
  h1.GetYaxis().SetTitleFont(43)
  h1.GetYaxis().SetTitleOffset(1.5)
  h1.GetYaxis().SetLabelFont(43)
  h1.GetYaxis().SetLabelSize(18)
  h1.GetYaxis().SetLabelOffset(0.015)
  h1.GetXaxis().SetNdivisions(510)
  h1.GetXaxis().SetTitleSize(20)
  h1.GetXaxis().SetTitleFont(43)
  h1.GetXaxis().SetTitleOffset(3.4)
  h1.GetXaxis().SetLabelFont(43)
  h1.GetXaxis().SetLabelSize(18)
  h1.GetXaxis().SetLabelOffset(0.03)
  return h1


wwwDir = "/afs/cern.ch/user/d/dhandl/www/Run2/SUSY/Stop1l/ttbarSyst/"
if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)

fileName = "shapeTTbar2L_"
#fileName = "mt130_met230_shapeComparison_HardScatter_oldPtag"
#fileName = "mt130_met230_shapeComparison_HadFrag_oldPtag"

# setup input directories for TChains
#bkgDir = "/eos/atlas/user/d/dboerner/" 
bkgDir = "/eos/atlas/user/j/jkuechle/public/ntuples/" 
#sigDir = "/afs/cern.ch/work/d/dhandl/public/Stop1L/syst_truth/" 
truthDir = "/afs/cern.ch/user/t/therwig/workspace/public/STOP_MORIOND17/syst/"
#truthDir = "/afs/cern.ch/work/d/dhandl/SUSY/stop1l-xaod/export/syst_truth/" 
sigDir = "/afs/cern.ch/work/j/jmitrevs/public/bWN_syst/"

lumi = 36100.
weight = str(lumi)+" * weight * xs_weight * sf_total * weight_sherpa22_njets" 
truth_weight = str(lumi)+" * weight * xs_weight " 

cut = "(stxe_trigger) && (n_bjet>0) && (mt>130e3) && (met>230e3) && (n_jet>=4) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80))"
truth_cut = "(n_lep==1) && (lep_pt[0]>25e3) && (n_jet>=4) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>130e3) && (met>230e3) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) "#&& !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80))"

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
#  {"name":"singletop", "legendName":"Single top SUSY5", "target":bkgDir+"powheg_singletop/*", "color": ROOT.TColor.GetColor("#82DE68"), "chain_name":"powheg_singletop_Nom", "isTruth":False}, 
#  {"name":"wjets", "legendName":"W+jets", "target":bkgDir+"sherpa22_Wjets/*", "color": ROOT.TColor.GetColor("#FCDD5D"), "chain_name":"sherpa22_Wjets_Nom"}, 
#  {"name":"ttbar1L", "legendName":"t#bar{t} 1L", "target":bkgDir+"powheg_ttbar/*", "color":ROOT.TColor.GetColor("#0F75DB"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==1 || tt_cat==4 || tt_cat==7 )" },
  {"name":"ttbar2L", "legendName":"t#bar{t} 2L", "target":bkgDir+"powheg_ttbar/*", "color":ROOT.TColor.GetColor("#A5C6E8"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==0 || tt_cat==3 || tt_cat==6 )", "isTruth":False },
  {"name":"ttbar1L1tau", "legendName":"t#bar{t} 1L1#tau", "target":bkgDir+"powheg_ttbar/*", "color": ROOT.TColor.GetColor("#5E9AD6"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==2 || tt_cat == 5 )", "isTruth":False}, 
#  {"name":"ttbar",              "legendName":"t#bar{t}",           "target":bkgDir+"powheg_ttbar/*",     "chain_name":"powheg_ttbar_Nom", "color":ROOT.kBlack, "isTruth":False       },
#  {"name":"ttbar_radHi",        "legendName":"t#bar{t} radHi",     "target":bkgDir+"ttbar_radHi/*",      "chain_name":"ttbar_radHi_Nom" , "color":ROOT.kRed       },
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

#  {"name":"stop_bWN_350_230", "legendName":"stop_bWN_350_230 SUSY5", "target":bkgDir+"stop_bWN_350_230/*", "color": ROOT.kBlack, "chain_name":"stop_bWN_350_230_Nom", "isTruth":False},
#  {"name":"stop_bWN_350_230_nom", "legendName":"stop_bWN_350_230 TRUTH", "target":sigDir+"stop_bWN_350_230_MadSin_m1001L20_truth/*", "color": ROOT.kBlue, "chain_name":"stop_bWN_350_230_MadSin_m1001L20_truth_Nom", "isTruth":True},
#  {"name":"stop_bWN_350_230_nom", "legendName":"nominal", "target":sigDir+"Nominal_350_230/*", "color": ROOT.kBlack, "chain_name":"Nominal_350_230_Nom", "isTruth":True},
#  {"name":"stop_bWN_350_230_PS_dw", "legendName":"PS down", "target":sigDir+"py3cdw_350_230/*", "color": ROOT.kRed, "chain_name":"py3cdw_350_230_Nom", "isTruth":True},
#  {"name":"stop_bWN_350_230_PS_up", "legendName":"PS up", "target":sigDir+"py3cup_350_230/*", "color": ROOT.kBlue, "chain_name":"py3cup_350_230_Nom", "isTruth":True},
#  {"name":"stop_bWN_350_230_MERGE_dw", "legendName":"merging down", "target":sigDir+"qcdw_350_230/*", "color": ROOT.kGreen+2, "chain_name":"qcdw_350_230_Nom", "isTruth":True},
#  {"name":"stop_bWN_350_230_MERGE_up", "legendName":"merging up", "target":sigDir+"qcup_350_230/*", "color": ROOT.kOrange+7, "chain_name":"qcup_350_230_Nom", "isTruth":True},
#  {"name":"stop_bWN_350_230_FACT_dw", "legendName":"fact./ren. down", "target":sigDir+"scdw_350_230/*", "color": ROOT.kMagenta, "chain_name":"scdw_350_230_Nom", "isTruth":True},
#  {"name":"stop_bWN_350_230_FACT_up", "legendName":"fact./ren. up", "target":sigDir+"scup_350_230/*", "color": ROOT.kAzure+6, "chain_name":"scup_350_230_Nom", "isTruth":True},
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

allSignal = [
  {"name":"stop_bWN_350_200", "legendName":"m(#tilde{t},#tilde{#chi}_{1}^{0})=(350,200)", "target":bkgDir+"stop_bWN_350_200_MadSpin_m1001L20/*", "color": ROOT.TColor.GetColor(ROOT.kBlue+2), "chain_name":"stop_bWN_350_200_MadSpin_m1001L20_Nom"},
]

for i, sample in enumerate(allBkg):
  sample["chain"] = ROOT.TChain(sample["chain_name"])
  sample["chain"].Add(sample["target"])

allVariables = []
#amt2 = {'name':'myAmt2', "fileName":fileName+"_amt2"+normString+logString, 'varStr':"amt2", 'Xtitle':'am_{T2}', 'Ytitle':'Events', 'binning':[80,90,100,110,120,170,250,350,600], "binningIsExplicit":True}
amt2 = {'name':'myAmt2', "fileName":fileName+"_amt2"+normString+logString, 'varStr':"amt2", 'Xtitle':'am_{T2} [GeV]', 'Ytitle':'Events / 20 GeV', 'binning':[30,0,600], "binningIsExplicit":False, "addCut":" (met>300e3) && (dphi_met_lep<2.5) "}
dphi = {'name':'mydphi', "fileName":fileName+"_dphi"+normString+logString, 'varStr':"dphi_met_lep", 'Xtitle':'#Delta#Phi(E_{T}^{miss},l)', 'Ytitle':'Events / 0.2', 'binning':[16,0,3.2], "binningIsExplicit":False, "addCut":" (met>300e3) && (amt2<110)"}
met = {'name':'myMet', "fileName":fileName+"_met"+normString+logString, 'varStr':"(met*0.001)", 'Xtitle':'E_{T}^{miss} [GeV]', 'Ytitle':'Events / 20 GeV', 'binning':[20,200,600], "binningIsExplicit":False, "addCut":" (amt2<110) && (dphi_met_lep<2.5) "}
njet = {'name':'myNjet', "fileName":fileName+"_njet"+normString+logString, 'varStr':"n_jet", 'Xtitle':'Jet multiplicity', 'Ytitle':'Events', 'binning':[11,-0.5,10.5], "binningIsExplicit":False, "addCut":" (met>300e3) && (dphi_met_lep<2.5) && (amt2<110) "}
jet1 = {'name':'myJet1', "fileName":fileName+"_jetPt1"+normString+logString, 'varStr':"(jet_pt[0]*0.001)", 'Xtitle':'first jet p_{T} [GeV]', 'Ytitle':'Events / 40 GeV', 'binning':[20,0,800], "binningIsExplicit":False, "addCut":" (met>300e3) && (dphi_met_lep<2.5) && (amt2<110) "}
jet2 = {'name':'myJet2', "fileName":fileName+"_jetPt2"+normString+logString, 'varStr':"(jet_pt[1]*0.001)", 'Xtitle':'second jet p_{T} [GeV]', 'Ytitle':'Events / 40 GeV', 'binning':[15,0,600], "binningIsExplicit":False, "addCut":" (met>300e3) && (dphi_met_lep<2.5) && (amt2<110) "}
jet3 = {'name':'myJet3', "fileName":fileName+"_jetPt3"+normString+logString, 'varStr':"(jet_pt[2]*0.001)", 'Xtitle':'third jet p_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[14,0,350], "binningIsExplicit":False, "addCut":" (met>300e3) && (dphi_met_lep<2.5) && (amt2<110) "}
jet4 = {'name':'myJet4', "fileName":fileName+"_jetPt4"+normString+logString, 'varStr':"(jet_pt[3]*0.001)", 'Xtitle':'fourth jet p_{T} [GeV]', 'Ytitle':'Events / 25 GeV', 'binning':[10,0,250], "binningIsExplicit":False, "addCut":" (met>300e3) && (dphi_met_lep<2.5) && (amt2<110) "}
nbjet = {'name':'myNbjet', "fileName":fileName+"_nbjet"+normString+logString, 'varStr':"n_bjet", 'Xtitle':'b-jet multiplicity', 'Ytitle':'Events', 'binning':[5,-0.5,4.5], "binningIsExplicit":False, "addCut":" (met>300e3) && (dphi_met_lep<2.5) && (amt2<110) "}

allVariables.append(amt2)
allVariables.append(dphi)
allVariables.append(met)
allVariables.append(njet)
allVariables.append(jet1)
allVariables.append(jet2)
allVariables.append(jet3)
allVariables.append(jet4)
allVariables.append(nbjet)

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
      cut = cut
      weight = weight
    if sample.has_key("addCut"):
      cutString = cut+" && "+sample["addCut"]
    else:
      cutString = cut
#    if var.has_key("addCut"):
#      cutString = cutString+" && "+var["addCut"]
#    else:
#      cutString = cutString
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
  legend = ROOT.TLegend(0.7,0.75,0.9,0.9)
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
    histos[sample['name']][var['name']].SetMarkerStyle(0)
    histos[sample['name']][var['name']].GetXaxis().SetTitle(var['Xtitle'])
    histos[sample['name']][var['name']].GetYaxis().SetTitle(var['Ytitle'])# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
    if setRatioPlot:
      histos[sample['name']][var['name']].GetXaxis().SetLabelSize(0.0)
    #histos[sample['name']][var['name']].GetYaxis().SetLabelSize(0.04)
    #stack.Add(histos[sample['name']][var['name']])
    legend.AddEntry(histos[sample['name']][var['name']], sample['legendName'])
    if normalized:
      histos[sample['name']][var['name']].Scale(1./histos[sample['name']][var['name']].Integral())

    max_tmp = histos[sample['name']][var['name']].GetMaximum()
    if max_tmp > nMax:
      nMax = max_tmp
    if first:
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
    ATLASLabel(0.18,0.88,"Work in progress")
    ATLASLumiLabel(0.18,0.86, str(lumi*0.001))
    pad2 = ROOT.TPad("pad2","pad2",0.,0.,1.,0.3)
    pad2.SetTopMargin(0.01)
    pad2.SetBottomMargin(0.3)
    pad2.SetGrid()
    pad2.Draw()
    pad2.cd()
  
    ratio1 = doRatio(histos['ttbar1L1tau'][var['name']],histos['ttbar2L'][var['name']], ymin=-0.5, ymax=2.5, Xtitle=var['Xtitle'],Ytitle="1/t#bar{t} 2L")
    #ratio2 = doRatio(histos['stop_bWN_350_230_FACT_up'][var['name']],histos['stop_bWN_350_230_nom'][var['name']], ymin=-0.5, ymax=2.5, Xtitle=var['Xtitle'],Ytitle="1/nominal")
    ratio1.SetMarkerStyle(20)
    ratio1.SetMarkerColor(ratio1.GetLineColor())
    ratio1.SetMarkerSize(0.85)
    #ratio2.SetMarkerStyle(20)
    #ratio2.SetMarkerColor(ratio2.GetLineColor())
    #ratio2.SetMarkerSize(0.85)
    ratio1.Draw("ep")
    #ratio2.Draw("ep same") 
    ROOT.gPad.Modified()
    ROOT.gPad.Update()
    line = ROOT.TLine(ROOT.gPad.GetUxmin(), 1, ROOT.gPad.GetUxmax(), 1)
    line.SetLineStyle(ROOT.kDashed)
    line.SetLineWidth(2)
    line.Draw()

  else:
    pad1.cd()
    ATLASLabel(0.18,0.88,"Work in progress")
    ATLASLumiLabel(0.18,0.86, str(lumi*0.001))

  canv.cd()
  canv.Print(wwwDir+var["fileName"]+".pdf")
  canv.Print(wwwDir+var["fileName"]+".root")
  canv.Print(wwwDir+var["fileName"]+".png")
