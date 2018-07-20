import ROOT
import math
import os, sys

from AtlasStyle import *
SetAtlasStyle()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

ROOT.TGaxis().SetMaxDigits(4)

wwwDir = "/project/etp5/dbuchin/plots/corrVariables/"
if not os.path.exists(wwwDir):
  os.makedirs(wwwDir)
 
 
normalized = False
setLogY = False
setRatioPlot = False

fileName =  "" 
cutInfo = ""

#Set this true to produce a plot adding up all BKG's in addition to the defined signal plots (single BKG's won't be produced while this is true to avoid memory leaks | you need to enable all BKG's in the dictionary)
BKGADD = True

normString = ""
logString = ""
if normalized:
    y_title = 'Normierte Events'
else:
    y_title = 'Events'


# setup input directories for TChains
bkgDir = "/project/etp5/dbuchin/samples/SUSY/Stop1L/softLepton/" 
sigDir = bkgDir



#Which Variable(take respective dictionary):
myvar = {'name':'myLdPhi', "fileName":fileName+"_Ldphi"+normString+logString, 'varStr':"Ldphi", 'Xtitle':'#Delta#phi_{Lepton}', 'Ytitle':'Events', 'binning':[20,0,4], "binningIsExplicit":False}



lumi = 140e3

cut = "( "+str(lumi)+" * weight * xs_weight * sf_total * weight_sherpa22_njets * ((stxe_trigger) &&       (n_bjet>=0)       && (met>230e3) && (n_jet>=2) && (jet_pt[0]>25e3) && (jet_pt[1]>25e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) &&(n_lep==1)&&(n_mu==1?lep_pt[0]>4e3:1)&&(n_el==1?lep_pt[0]>5e3:1)&&(n_jet>=2) && (jet_bjet77[0]==0) && (n_hadtop_cand == 0 || Alt$(hadtop_cand_m[0],0) < 150e3)     ))"


truth_cut = "( 36500. * weight * xs_weight * ( (n_lep==1) && (lep_pt[0]>25e3) && (n_jet>=4) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>130e3) && (met>230e3) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4)))"


allBkg = [
  #Am Besten nur relevante Bkgs benutzen
  {"name":"ttv", "legendName":"t#bar{t}+V", "target":bkgDir+"amcnlo_ttV/*", "color": ROOT.TColor.GetColor("#E67067"), "chain_name":"amcnlo_ttV_Nom"}, 
  {"name":"diboson", "legendName":"Diboson", "target":bkgDir+"sherpa221_diboson/*", "color": ROOT.TColor.GetColor("#54C571"), "chain_name":"sherpa221_diboson_Nom"}, 
  {"name":"singletop", "legendName":"Single top", "target":bkgDir+"powheg_singletop/*", "color": ROOT.TColor.GetColor("#82DE68"), "chain_name":"powheg_singletop_Nom", "isTruth":False}, 
  {"name":"wjets", "legendName":"W+jets", "target":bkgDir+"sherpa22_Wjets/*", "color": ROOT.TColor.GetColor("#FCDD5D"), "chain_name":"sherpa22_Wjets_Nom"}, 
  {"name":"zjets", "legendName":"Z+jets", "target":bkgDir+"sherpa22_Zjets/*", "color": ROOT.kViolet, "chain_name":"sherpa22_Zjets_Nom"},
  {"name":"ttbar",              "legendName":"t#bar{t}",           "target":bkgDir+"powheg_ttbar/*",     "chain_name":"powheg_ttbar_Nom", "color":ROOT.kBlue, "isTruth":False       },
  {"name":"ttbar1L", "legendName":"t#bar{t} 1L", "target":bkgDir+"powheg_ttbar/*", "color":ROOT.TColor.GetColor("#0F75DB"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==1 || tt_cat==4 || tt_cat==7 )" },
  {"name":"ttbar2L", "legendName":"t#bar{t} 2L", "target":bkgDir+"powheg_ttbar/*", "color":ROOT.TColor.GetColor("#A5C6E8"), "chain_name":"powheg_ttbar_Nom", "addCut":"( tt_cat==2 || tt_cat == 5 || tt_cat==0 || tt_cat==3 || tt_cat==6 )", "isTruth":False },
]

allSignal = [
  {"name":"stop_bffN_400_380", "legendName":"m(#tilde{t}_{1},#tilde{#chi}_{1}^{0})=400,380 *10", "target":sigDir+"TT_bffN_400_380/*", "color": ROOT.kBlack, "chain_name":"TT_bffN_400_380_Nom", "isTruth":False, "scale":10},
  {"name":"stop_bffN_400_350", "legendName":"m(#tilde{t}_{1},#tilde{#chi}_{1}^{0})=400,350 *10", "target":sigDir+"TT_bffN_400_350/*", "color": ROOT.kBlue, "chain_name":"TT_bffN_400_350_Nom", "isTruth":False, "scale":10},
  {"name":"stop_bffN_400_320", "legendName":"m(#tilde{t}_{1},#tilde{#chi}_{1}^{0})=400,320 *10", "target":sigDir+"TT_bffN_400_320/*", "color": ROOT.kPink, "chain_name":"TT_bffN_400_320_Nom", "isTruth":False, "scale":10}
]


for i, sample in enumerate(allBkg+allSignal):
  sample["chain"] = ROOT.TChain(sample["chain_name"])
  sample["chain"].Add(sample["target"])


allVariables = []
amt2 = {'name':'myAmt2', "fileName":fileName+"_amt2"+normString+logString, 'varStr':"amt2", 'Xtitle':'am_{T2}', 'Ytitle':'Events', 'binning':[30,0,600], "binningIsExplicit":False}
met = {'name':'myMET', "fileName":fileName+"_met"+normString+logString, 'varStr':"(met*0.001)", 'Xtitle':'E_{T}^{miss} [GeV]', 'Ytitle':'Events', 'binning':[40,200,900], "binningIsExplicit":False}
dphi = {'name':'mydPhi', "fileName":fileName+"_dphi"+normString+logString, 'varStr':"dphi_met_lep", 'Xtitle':'#Delta#phi(l, E_{T}^{miss})', 'Ytitle':'Events', 'binning':[20,0,4], "binningIsExplicit":False}
lep_pt = {'name':'myLepPt', "fileName":fileName+"_lepPt"+normString+logString, 'varStr':"lep_pt *0.001", 'Xtitle':'Lepton p_{T} [GeV]', 'Ytitle':'Events', 'binning':[40,0,100], "binningIsExplicit":False}
lep_pt_over_met = {'name':'myLepPtOverMet', "fileName":fileName+"_lepPt_over_met"+normString+logString, 'varStr':"lepPt_over_met", 'Xtitle':'Lepton p_{T} over E_{T}^{miss}', 'Ytitle':'Events / 0.01', 'binning':[40,0,0.9], "binningIsExplicit":False}
mt = {'name':'myMt', "fileName":fileName+"_mt"+normString+logString, 'varStr':"(mt*0.001)", 'Xtitle':'m_{T} [GeV]', 'Ytitle':'Events', 'binning':[40,0,300], "binningIsExplicit":False}
ht = {'name':'myHt', "fileName":fileName+"_ht"+normString+logString, 'varStr':"(HT*0.001)", 'Xtitle':'H_{T} [TeV]', 'Ytitle':'Events', 'binning':[40,0.1,1.5], "binningIsExplicit":False}
nbjet = {'name':'myNbjet', "fileName":fileName+"_nbjet"+normString+logString, 'varStr':"n_bjet", 'Xtitle':'b-jet multiplicity', 'Ytitle':'Events', 'binning':[5,-0.5,4.5], "binningIsExplicit":False}
njet = {'name':'myNjet', "fileName":fileName+"_njet"+normString+logString, 'varStr':"n_jet", 'Xtitle':'Jet multiplicity', 'Ytitle':'%s' % (y_title), 'binning':[11,-0.5,10.5], "binningIsExplicit":False}
jet1 = {'name':'myJet1', "fileName":fileName+"_jetPt1"+normString+logString, 'varStr':"(jet_pt[0]*0.001)", 'Xtitle':'first jet p_{T} [GeV]', 'Ytitle':'%s' % (y_title), 'binning':[20,25,800], "binningIsExplicit":False}
jet2 = {'name':'myJet2', "fileName":fileName+"_jetPt2"+normString+logString, 'varStr':"(jet_pt[1]*0.001)", 'Xtitle':'second jet p_{T} [GeV]', 'Ytitle':'%s' % (y_title), 'binning':[20,25,600], "binningIsExplicit":False}
CT1 = {'name':'myCT1', "fileName":fileName+"_CT1"+normString+logString, 'varStr':'CT1_alt', 'Xtitle':'C_{T1} [GeV]', 'Ytitle':'Events', 'binning':[30,200,900], "binningIsExplicit":False}
CT2 = {'name':'myCT2', "fileName":fileName+"_CT2"+normString+logString, 'varStr':'CT2', 'Xtitle':'C_{T2} [GeV]', 'Ytitle':'Events', 'binning':[30,200,900], "binningIsExplicit":False}
metoverLepPtHt = {'name':'myMetoverLepPtHt', "fileName":fileName+"_met_over_lepPt_ht"+normString+logString, 'varStr':'met_over_lepPt_softjetPt', 'Xtitle':'E_{T}^{miss} over Lepton P_{T} and Softjet P_{T}', 'Ytitle':'Events', 'binning':[40,0,10], "binningIsExplicit":False}
metoversqrtlepPtHt = {'name':'myMetoverSqrtLepPtHt', "fileName":fileName+"_met_over_squareroot_lepPt_softjetPt"+normString+logString, 'varStr':'met_over_sqrt_lepPt_softjetPt', 'Xtitle':'E_{T}^{miss} over Squareroot Lepton P_{T} and Softjet P_{T}', 'Ytitle':'Events', 'binning':[25,0,80], "binningIsExplicit":False}
dphijet12 = {'name':'myDphiJet12', "fileName":fileName+"_dphi_jet12"+normString+logString, 'varStr':'dphi_jet12', 'Xtitle':'dphi Jet_{1} Jet_{2}', 'Ytitle':'Events', 'binning':[20,0,3.2], "binningIsExplicit":False}
dphiLepJet1 = {'name':'myDphiLepJet1', "fileName":fileName+"_dphi_lep_jet1"+normString+logString, 'varStr':'dphi_lep_jet1', 'Xtitle':'dphi Lepton Jet_{1}', 'Ytitle':'Events', 'binning':[20,0,6], "binningIsExplicit":False}
sqrtlepPtHtoverMet = {'name':'mySqrtLepPtHtoverMet', "fileName":fileName+"_squareroot_lepPt_softjetPt_over_met"+normString+logString, 'varStr':'squareroot_lepPt_softjetPt_over_met', 'Xtitle':'Squareroot Lepton P_{T} and Softjet P_{T} over E_{T}^{miss}', 'Ytitle':'Events', 'binning':[20,0,0.15], "binningIsExplicit":False}
dphiMinMet = {'name':'mydPhiMinMet', "fileName":fileName+"_dphi_min_ptmiss"+normString+logString, 'varStr':"dphi_min_ptmiss", 'Xtitle':'Min(#Delta#phi(Jet, E_{T}^{miss}))', 'Ytitle':'Events', 'binning':[20,0,4], "binningIsExplicit":False}
lepEta = {'name':'myLepEta', "fileName":fileName+"_lep_eta"+normString+logString, 'varStr':"abs(lep_eta[0])", 'Xtitle':'|#eta(l)|', 'Ytitle':'Events', 'binning':[20,0,4], "binningIsExplicit":False}
jetM1 = {'name':'myJetM1', "fileName":fileName+"_jet_m1"+normString+logString, 'varStr':"jet_m[0]*0.001", 'Xtitle':'Jet_{1} Mass', 'Ytitle':'Events', 'binning':[30,0,100], "binningIsExplicit":False}
jet1Eta = {'name':'myJet1Eta', "fileName":fileName+"_jet1_eta"+normString+logString, 'varStr':"abs(jet_eta[0])", 'Xtitle':'|#eta(Jet_{1})|', 'Ytitle':'Events', 'binning':[20,0,4], "binningIsExplicit":False}
jet2Eta = {'name':'myJet2Eta', "fileName":fileName+"_jet2_eta"+normString+logString, 'varStr':"abs(jet_eta[1])", 'Xtitle':'|#eta(Jet_{2})|', 'Ytitle':'Events', 'binning':[20,0,4], "binningIsExplicit":False}
jet3Eta = {'name':'myJet3Eta', "fileName":fileName+"_jet3_eta"+normString+logString, 'varStr':"abs(jet_eta[2])", 'Xtitle':'|#eta(Jet_{3})|', 'Ytitle':'Events', 'binning':[20,0,4], "binningIsExplicit":False}
jetM2 = {'name':'myJetM2', "fileName":fileName+"_jet_m2"+normString+logString, 'varStr':"jet_m[1]*0.001", 'Xtitle':'Jet_{2} Mass', 'Ytitle':'Events', 'binning':[30,0,80], "binningIsExplicit":False}
jetM3 = {'name':'myJetM3', "fileName":fileName+"_jet_m3"+normString+logString, 'varStr':"jet_m[2]*0.001", 'Xtitle':'Jet_{3} Mass', 'Ytitle':'Events', 'binning':[30,0,80], "binningIsExplicit":False}
lepJet1_energy_ratio = {'name':'myELepoverEJet1', "fileName":fileName+"_lepJet1_energy_ratio"+normString+logString, 'varStr':"lepJet1_energy_ratio", 'Xtitle':'E_{Lepton} over E_{Jet1}', 'Ytitle':'Events', 'binning':[30,0,0.9], "binningIsExplicit":False}
mt_over_dphiMetLep = {'name':'myMtoverDPhiMetLep', "fileName":fileName+"_mt_over_dphiMetLep"+normString+logString, 'varStr':"mt_over_dphiMetLep", 'Xtitle':'M_{T} over #Delta#phi(l, E_{T}^{miss})', 'Ytitle':'Events', 'binning':[30,0,310], "binningIsExplicit":False}
sqrtLepPt_over_met = {'name':'mySqrtLepPtoverMet', "fileName":fileName+"_sqrtLepPt_over_met"+normString+logString, 'varStr':"(sqrtLepPt_over_met *100)", 'Xtitle':'Squareroot of Lepton P_{T} over E^{miss}_{T} (in %)', 'Ytitle':'Events', 'binning':[30,0,10], "binningIsExplicit":False}
lepCharge = {'name':'myLepCharge', "fileName":fileName+"_lep_charge"+normString+logString, 'varStr':"lep_charge", 'Xtitle':'Lepton Charge', 'Ytitle':'Events', 'binning':[30,-2,5], "binningIsExplicit":False}
wPt = {'name':'myWPt', "fileName":fileName+"_wPt"+normString+logString, 'varStr':"pt_W *0.001", 'Xtitle':'W p_{T} [GeV]', 'Ytitle':'Events', 'binning':[30,0.2,1.3], "binningIsExplicit":False}
metx_abs = {'name':'myMetXAbs', "fileName":fileName+"_met_x_abs"+normString+logString, 'varStr':"met_x *0.000001", 'Xtitle':'E^{miss}_{T,x} [TeV]', 'Ytitle':'Events', 'binning':[30,0,2.0], "binningIsExplicit":False}
mety_abs = {'name':'myMetYAbs', "fileName":fileName+"_met_y_abs"+normString+logString, 'varStr':"met_y *0.000001", 'Xtitle':'E^{miss}_{T,y} [TeV]', 'Ytitle':'Events', 'binning':[30,0,2.0], "binningIsExplicit":False}
dphi_b_ptmiss_min = {'name':'myDphiBMetMin', "fileName":fileName+"_dphi_B_Met_Min"+normString+logString, 'varStr':'dphi_b_ptmiss_min', 'Xtitle':'Min(#Delta#phi(B-Jet, E^{miss}_{T}))', 'Ytitle':'Events', 'binning':[25,0,4], "binningIsExplicit":False}
dr_bjet_lep = {'name':'myDRBlep', "fileName":fileName+"_dR_B_Lep"+normString+logString, 'varStr':'dr_bjet_lep', 'Xtitle':'dR B-Jet Lepton', 'Ytitle':'Events', 'binning':[30,0,6], "binningIsExplicit":False}
bjet1 = {'name':'myBJet1', "fileName":fileName+"_bjetPt1"+normString+logString, 'varStr':"(bjet_pt[0]*0.001)", 'Xtitle':'first B-Jet p_{T} [GeV]', 'Ytitle':'%s' % (y_title), 'binning':[30,25,600], "binningIsExplicit":False}
wPt_over_met = {'name':'myWPtoverMet', "fileName":fileName+"_wPt_over_met"+normString+logString, 'varStr':"wPt_over_met", 'Xtitle':'W P_{T} over E^{miss}_{T}', 'Ytitle':'Events', 'binning':[40,0,2], "binningIsExplicit":False}
Lp = {'name':'myLp', "fileName":fileName+"_Lp"+normString+logString, 'varStr':"Lp", 'Xtitle':'L_{P}', 'Ytitle':'Events', 'binning':[40,-0.2,0.2], "binningIsExplicit":False}
WEnergy1 = {'name':'myWEnergy1', "fileName":fileName+"_W_Energy1"+normString+logString, 'varStr':"WEnergy1", 'Xtitle':'W Energy 1 [GeV]', 'Ytitle':'Events', 'binning':[50,0,950], "binningIsExplicit":False}
WRapidity1 = {'name':'myWRapidity1', "fileName":fileName+"_W_Rapidity1"+normString+logString, 'varStr':"WRapidity1", 'Xtitle':'|Rapidity(W)| 1', 'Ytitle':'Events', 'binning':[40,0,3], "binningIsExplicit":False}
W_Lepton_angle_Wrestingframe1 = {'name':'myWLeptonAngleWResting1', "fileName":fileName+"_W_lepton_Angle_Wresting1"+normString+logString, 'varStr':"W_Lepton_angle_Wrestingframe1", 'Xtitle':'Angle(W, Lepton) in W resting frame 1', 'Ytitle':'Events', 'binning':[40,1.5,4], "binningIsExplicit":False}
WJet2_angle_jet1boost1 = {'name':'myWJet2BoostJet1Angle1', "fileName":fileName+"_WJet2_jet1boost_angle1"+normString+logString, 'varStr':"WJet2_angle_jet1boost1", 'Xtitle':'Angle(W, Jet_{2}) boosted in Jet_{1} frame 1', 'Ytitle':'Events', 'binning':[40,0,1], "binningIsExplicit":False}
HT = {'name':'myHTmine', "fileName":fileName+"_HT_mine"+normString+logString, 'varStr':"(HT*0.001)", 'Xtitle':'my H_{T} [TeV]', 'Ytitle':'Events', 'binning':[40,0.1,1.5], "binningIsExplicit":False}
Cos_W_resting_Lepton_angle1 = {'name':'myCosWRestingLeptonAngle1', "fileName":fileName+"_Cos_W_resting_lepton_Angle1"+normString+logString, 'varStr':"(Cos_W_resting_Lepton_angle1)", 'Xtitle':'Cos(Angle(W, Lepton)) in W resting frame 1', 'Ytitle':'%s' % (y_title), 'binning':[40,-1,-0.5], "binningIsExplicit":False}
n_hadtop_cand = {'name':'myNhadtop', "fileName":fileName+"_n_hadtop"+normString+logString, 'varStr':"n_hadtop_cand", 'Xtitle':'hadronic top multiplicity', 'Ytitle':'Events', 'binning':[5,-0.5,4.5], "binningIsExplicit":False}
hadtop_cand_m = {'name':'myHadtopM', "fileName":fileName+"_hadtop_m"+normString+logString, 'varStr':"hadtop_cand_m[0]*0.001", 'Xtitle':'Hadronic Top Mass [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], "binningIsExplicit":False}
mT2tau = {'name':'myMT2tau', "fileName":fileName+"_mT2_tau"+normString+logString, 'varStr':"mT2tauLooseTau_GeV", 'Xtitle':'m_{T2} tau [GeV]', 'Ytitle':'Events', 'binning':[30,-2,2], "binningIsExplicit":False}
Ldphi = {'name':'myLdPhi', "fileName":fileName+"_Ldphi"+normString+logString, 'varStr':"Ldphi", 'Xtitle':'#Delta#phi_{Lepton}', 'Ytitle':'Events', 'binning':[20,0,4], "binningIsExplicit":False}


#allVariables.append(amt2)
#allVariables.append(met)
#allVariables.append(dphi)
#allVariables.append(lep_pt)
#allVariables.append(lep_pt_over_met)
#allVariables.append(mt)
#allVariables.append(ht)
#allVariables.append(nbjet)
#allVariables.append(njet)
allVariables.append(jet1)
#allVariables.append(jet2)
allVariables.append(CT1) 
allVariables.append(CT2)
#allVariables.append(metoverLepPtHt)
#allVariables.append(metoversqrtlepPtHt)
#allVariables.append(dphijet12)
#allVariables.append(dphiLepJet1)
#allVariables.append(sqrtlepPtHtoverMet)
#allVariables.append(dphiMinMet)
#allVariables.append(lepEta)
#allVariables.append(jetM1)
#allVariables.append(jet1Eta)
#allVariables.append(jet2Eta)
#allVariables.append(jet3Eta)
#allVariables.append(jetM2)
#allVariables.append(jetM3)
#allVariables.append(lepJet1_energy_ratio)
#allVariables.append(mt_over_dphiMetLep)
#allVariables.append(sqrtLepPt_over_met)
#allVariables.append(lepCharge)
#allVariables.append(wPt)
#allVariables.append(metx_abs)
#allVariables.append(mety_abs)
#allVariables.append(dphi_b_ptmiss_min)
#allVariables.append(dr_bjet_lep)
#allVariables.append(bjet1)
#allVariables.append(wPt_over_met)
#allVariables.append(Lp)
#allVariables.append(WEnergy1)
#allVariables.append(WRapidity1)
#allVariables.append(W_Lepton_angle_Wrestingframe1)
#allVariables.append(WJet2_angle_jet1boost1)
#allVariables.append(HT)
#allVariables.append(Cos_W_resting_Lepton_angle1)
#allVariables.append(n_hadtop_cand)
#allVariables.append(hadtop_cand_m)
#allVariables.append(mT2tau)
#allVariables.append(Ldphi)


histos = {}
histSums = {}

for var in allVariables:
    histSums[var['name']] = ROOT.TH2F("allBkg_"+var["name"], "allBkg_"+var["name"],myvar['binning'][0],myvar['binning'][1],myvar['binning'][2],var['binning'][0],var['binning'][1],var['binning'][2])

for sample in allBkg+allSignal:
  histos[sample['name']] = {}
  for var in allVariables:
    if var['name'] != myvar:
        if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
            histos[sample["name"]][var["name"]] = ROOT.TH1F(sample["name"]+"_"+var["name"], sample["name"]+"_"+var["name"], len(var['binning'])-1, array('d', var['binning']))
        else:
            histos[sample["name"]][var["name"]] = ROOT.TH2F(sample["name"]+"_"+var["name"], sample["name"]+"_"+var["name"],myvar['binning'][0],myvar['binning'][1],myvar['binning'][2],var['binning'][0],var['binning'][1],var['binning'][2])
        if sample.has_key("addCut"):
            cutString = cut+" && "+sample["addCut"]
        else:
            cutString = cut
        sample["chain"].Draw(var['varStr']+":"+myvar['varStr']+">>"+ histos[sample["name"]][var["name"]].GetName(),cutString,"goff")

for var in allVariables:
    if var['name'] != myvar:
        if BKGADD:
            for sample in allBkg:
                c0 = ROOT.TCanvas("c0","c0",1500,1250)
                c0.SetFillColor(10)
                c0.SetBorderSize(1)
                c0.SetLogz()
                c0.SetRightMargin(0.15)

                histos[sample["name"]][var["name"]].GetYaxis().SetTitle(var['Xtitle'])
                
                histos[sample["name"]][var["name"]].GetXaxis().SetTitle(myvar['Xtitle'])
                
                histSums[var['name']].Add(histos[sample['name']][var['name']])
                
            histSums[var['name']].Draw("colz")
            histSums[var['name']].GetYaxis().SetTitle(var['Xtitle'])
                
            histSums[var['name']].GetXaxis().SetTitle(myvar['Xtitle'])
                
            corr = histSums[var['name']].GetCorrelationFactor()

            ATLASLabel(0.18,0.9,"Work in progress")
            ATLASLumiLabel(0.18,0.89,"140")

            text = ROOT.TLatex()
            text.SetNDC()
            text.SetTextSize(0.045)
            text.SetTextAlign(11) 
            text.DrawLatex(0.1,0.04,"r = %.3f"%corr)
                
            fileName = 'ALLBKG_' + myvar['name'] + 'VS' + var['name'] + cutInfo
                    
            c0.SaveAs(wwwDir+fileName+".pdf")
            c0.SaveAs(wwwDir+fileName+".root")
            c0.SaveAs(wwwDir+fileName+".png")
            
            for sample in allSignal:
                c0 = ROOT.TCanvas("c0","c0",1500,1250)
                c0.SetFillColor(10)
                c0.SetBorderSize(1)
                c0.SetLogz()
                c0.SetRightMargin(0.15)
                #c0.SetGridy()
                #c0.SetGridx()
                    
                histos[sample["name"]][var["name"]].Draw("colz")
                histos[sample["name"]][var["name"]].GetYaxis().SetTitle(var['Xtitle'])
                #h.GetYaxis().SetTitle("#Delta#Phi(E_{T}^{miss},l)")
                histos[sample["name"]][var["name"]].GetXaxis().SetTitle(myvar['Xtitle'])
                
                corr = histos[sample["name"]][var["name"]].GetCorrelationFactor()

                ATLASLabel(0.18,0.9,"Work in progress")
                ATLASLumiLabel(0.18,0.89,"140")

                text = ROOT.TLatex()
                text.SetNDC()
                text.SetTextSize(0.045)
                text.SetTextAlign(11) 
                text.DrawLatex(0.1,0.04,"r = %.3f"%corr)
                #text.DrawLatex(0.5,0.8,"m(#tilde{t},#tilde{#chi}_{1}^{0})_{3-body}=(%i,%i) GeV"%(sig[0],sig[1]))
                #ROOT.myText(0.15,0.335,1,"Data 16, RN 297041")
                #ROOT.myText(0.15,0.285,1,"#sqrt{s} = 13TeV")
                #ROOT.myText(0.15,0.235,1,"Elec. Noise [MeV], EM1")
                    
                fileName = sample['name'] + '_' + myvar['name'] + 'VS' + var['name'] + cutInfo
                    
                c0.SaveAs(wwwDir+fileName+".pdf")
                c0.SaveAs(wwwDir+fileName+".root")
                c0.SaveAs(wwwDir+fileName+".png")
            
          
        else:  
            for sample in allBkg+allSignal:
                c0 = ROOT.TCanvas("c0","c0",1500,1250)
                c0.SetFillColor(10)
                c0.SetBorderSize(1)
                c0.SetLogz()
                c0.SetRightMargin(0.15)
                #c0.SetGridy()
                #c0.SetGridx()
                    
                histos[sample["name"]][var["name"]].Draw("colz")
                histos[sample["name"]][var["name"]].GetYaxis().SetTitle(var['Xtitle'])
                #h.GetYaxis().SetTitle("#Delta#Phi(E_{T}^{miss},l)")
                histos[sample["name"]][var["name"]].GetXaxis().SetTitle(myvar['Xtitle'])
                
                corr = histos[sample["name"]][var["name"]].GetCorrelationFactor()

                ATLASLabel(0.18,0.9,"Work in progress")
                ATLASLumiLabel(0.18,0.89,"140")

                text = ROOT.TLatex()
                text.SetNDC()
                text.SetTextSize(0.045)
                text.SetTextAlign(11) 
                text.DrawLatex(0.1,0.04,"r = %.3f"%corr)
                #text.DrawLatex(0.5,0.8,"m(#tilde{t},#tilde{#chi}_{1}^{0})_{3-body}=(%i,%i) GeV"%(sig[0],sig[1]))
                #ROOT.myText(0.15,0.335,1,"Data 16, RN 297041")
                #ROOT.myText(0.15,0.285,1,"#sqrt{s} = 13TeV")
                #ROOT.myText(0.15,0.235,1,"Elec. Noise [MeV], EM1")
                    
                fileName = sample['name'] + '_' + myvar['name'] + 'VS' + var['name'] + cutInfo
                    
                c0.SaveAs(wwwDir+fileName+".pdf")
                c0.SaveAs(wwwDir+fileName+".root")
                c0.SaveAs(wwwDir+fileName+".png")

