#!usr/bin/python2

# import statements
import ROOT
import copy, os, sys
import helpers

from AtlasStyle import * 
from math import *
from array import array
from datetime import datetime


def doRatio(hist1,hist2,Xtitle='',Ytitle='1/Default'):
    """TO DO: find out what this does exactly"""    
    
    # ROOT commands
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


def plot(var, fileName, cut, weight, allSignal, allBkg):
    """ Creates a plot """
    
    # Creates empty list 'allVariables' and appends first passed argument to that list
    # 'allVariables.append(var)' replaces the following append statements at position 1 (~ ll. 76)
    allVariables=[]
    allVariables.append(var)
    

    # Creating dictionaries of different variables with defined keys (But why is it commented out?)

    #amt2 = {'name':'myAmt2', 'fileName':fileName+'_amt2'+normString+logString, 'varStr':'amt2', 'Xtitle':'am_{T2}', 'Ytitle':'Events', 'binning':[30,0,600], 'binningIsExplicit':False}
    #met = {'name':'myMET', 'fileName':fileName+'_met'+normString+logString, 'varStr':'(met*0.001)', 'Xtitle':'E_{T}^{miss} [GeV]', 'Ytitle':'Events', 'binning':[30,0,600], 'binningIsExplicit':False}
    #dphi = {'name':'mydPhi', 'fileName':fileName+'_dphi'+normString+logString, 'varStr':'dphi_met_lep', 'Xtitle':'#Delta#phi(l, E_{T}^{miss})', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
    #mt = {'name':'myMT','fileName':fileName+'_mt'+normString+logString, 'varStr':'mt*0.001', 'Xtitle':'m_{T}', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    #Q = {'name':'myQ','fileName':fileName+'_Q'+normString+logString, 'varStr':'1-mt*mt/(2*met*lep_pt[0])', 'Xtitle':'Q', 'Ytitle':'Events', 'binning':[30,-1,1], 'binningIsExplicit':False}
    #njet = {'name':'mynjet','fileName':fileName+'_njet'+normString+logString, 'varStr':'n_jet', 'Xtitle':'N jets', 'Ytitle':'Events', 'binning':[10,0,10], 'binningIsExplicit':False}
    #nbjet = {'name':'mynbjet','fileName':fileName+'_nbjet'+normString+logString, 'varStr':'n_bjet', 'Xtitle':'N bjets', 'Ytitle':'Events', 'binning':[10,0,10], 'binningIsExplicit':False}
    #jetpt = {'name':'myjetpT','fileName':fileName+'_jetpT'+normString+logString, 'varStr':'jet_pt*0.001', 'Xtitle':'p_{T}^{jet}', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    #ht = {'name':'myht','fileName':fileName+'_hT'+normString+logString, 'varStr':'ht*0.001', 'Xtitle':'h_{T}', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    #dphi_jet0_ptmiss = {'name':'mydPhi_jet0ptmiss', 'fileName':fileName+'_dphi_jet0_ptmiss'+normString+logString, 'varStr':'dphi_jet0_ptmiss', 'Xtitle':'#Delta#phi(jet0, p_{T}^{miss})', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
    #dphi_jet1_ptmiss = {'name':'mydPhi_jet1ptmiss', 'fileName':fileName+'_dphi_jet1_ptmiss'+normString+logString, 'varStr':'dphi_jet1_ptmiss', 'Xtitle':'#Delta#phi(jet1, p_{T}^{miss})', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
    #amm = {'name':'myamm','fileName':fileName+'_amm'+normString+logString, 'varStr':'(met*lep_pt[0])*(0.001*0.001)', 'Xtitle':'amm', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}


    # Here is position 1
    
    #allVariables.append(met)
    #allVariables.append(dphi)
    #allVariables.append(amt2)
    #allVariables.append(mt)
    #allVariables.append(Q)
    #allVariables.append(njet)
    #allVariables.append(nbjet)
    #allVariables.append(jetpt)
    #allVariables.append(ht)
    #allVariables.append(dphi_jet0_ptmiss)
    #allVariables.append(dphi_jet1_ptmiss)
    #allVariables.append(amm)


    # Create empty dictionary of histograms
    histos = {}

    # Final structure of histos will be as following:
    # histos = {sample1_name: {variable 1: actual ROOT histogram, variable 2: actual ROOT histogram, ...}, sample2_name:{variable 1: actual ROOT histogram, ...}, ... }

    # Going through all entries of combined list of background and signal data
    # allBkg & allSignal are lists whose entries are dictionaries, therefore allBkg+allSignal is joined list
    # sample is one item of that joined list and it is a dictionary (see ~ ll. 230)
    for sample in allBkg+allSignal:
        
        # For every item in list do following:
        # Create a new key-value-pair: The key of this new pair is the value of "sample['name']" and its value is an empty dictionary
        histos[sample['name']] = {}
        
        # Now we are going through each variable "var" in list "allVariables"
        # At this point we are going thorugh each variable of each decay        
        for var in allVariables:

            # Adds Key-Pair value with key "var['name']" and as a value it adds the ROOT histogram
            # Upper Key-Pair value is added as value to key sample['name']

            # Check if variable has an explicit binning value set to true
            if var.has_key('binningIsExplicit') and var['binningIsExplicit']:
                # Set explicit binning accoirding to settings, ROOT syntax applies
                histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], len(var['binning'])-1, array('d', var['binning']))
            
            # No explicit binning set
            else:
                histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'],*var['binning'])
            
            # Check if variable has explicit cutt
            if sample.has_key('addCut'):
                cutString = cut+' && '+sample['addCut']
            else:
                cutString = cut
            
            # Draws value of key "chain"
            sample['chain'].Draw(var['varStr']+'>>'+histos[sample['name']][var['name']].GetName(), '('+weight+') * ('+cutString+')','goff')
    
    # Set Style for each variable 
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
    
    # Stacks histograms! Important for adding up background signal    
    stack = ROOT.THStack('stack','Stacked Histograms')

        
    first = True
    
    # Draw each background sample in histogram and stack values!
    for sample in allBkg:
        histos[sample['name']][var['name']].SetLineColor(ROOT.kBlack)
        histos[sample['name']][var['name']].SetLineWidth(2)
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
    
    # Check for logarithmic scale    
    if setLogY:
        stack.SetMinimum(10**(-1))
        stack.SetMaximum(100*stack.GetMaximum())
    else:
        stack.SetMinimum(0.)
        stack.SetMaximum(1.5*stack.GetMaximum())
    
    # Plotting signal in same histogram with set style. Do NOT stack!
    for sig in allSignal:
        histos[sig['name']][var['name']].SetLineColor(sig['color'])
        histos[sig['name']][var['name']].SetLineWidth(2)
        histos[sig['name']][var['name']].SetLineStyle(ROOT.kDashed)
        histos[sig['name']][var['name']].SetFillColor(0)
        histos[sig['name']][var['name']].SetMarkerStyle(0)
        
        # Trick for scaling up signal data and make it more visible, fakes higher luminosity for better visibility
        # Comment out if not needed.        
        if histos['ttbar1L'][var['name']].Integral()>0.:
            histos[sig['name']][var['name']].Scale(histos['ttbar1L'][var['name']].Integral()/histos[sig['name']][var['name']].Integral())
        
        # Draw        
        histos[sig['name']][var['name']].Draw('hist same')
        legend.AddEntry(histos[sig['name']][var['name']], sig['legendName'])
                        
    legend.Draw()

    canv.cd()

    # Check if ratio plot is true. If ratio plot is set, two diagrams will appear
    if setRatioPlot:
        helpers.ATLASLabelRatioPad(0.18,0.88,'Work in progress')
        helpers.ATLASLumiLabelRatioPad(0.18,0.6, str(lumi*0.001))
        pad2 = ROOT.TPad('pad2','pad2',0.,0.,1.,0.3)
        pad2.SetTopMargin(0.01)
        pad2.SetBottomMargin(0.3)
        pad2.SetGrid()
        pad2.Draw()
        pad2.cd()

  
        ratio1 = doRatio(histos['ttbar2L'][var['name']],histos['ttbar1L'][var['name']],var['Xtitle'])
        ratio1.Draw('hist')
    else:
        pad1.cd()
        ATLASLabel(0.18,0.88,'Work in progress')
        ATLASLumiLabel(0.18,0.86, str(lumi*0.001))

    # Creating files
    canv.cd()
    canv.Print(wwwDir+var['fileName']+'.pdf')
    canv.Print(wwwDir+var['fileName']+'.root')
    canv.Print(wwwDir+var['fileName']+'.png')
    canv.Close()
    


### BEGIN OF ACTUAL SCRIPT    
    
SetAtlasStyle()
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)
ROOT.TGaxis().SetMaxDigits(3)

#--- Set directory in which files should be saved
wwwDir = '/project/etp5/dprosperino/bachelor-SoSe17/plots/firstTry/Reproduction/'


#--- Setup input directories for TChains from which data shall be read
bkgDir = '/project/etp3/dhandl/samples/SUSY/Stop1L/duplicate/' 
sigDir = bkgDir 

#--- Set luminosity (ask for units)
lumi = 140000.

if not os.path.exists(wwwDir):
    os.makedirs(wwwDir)
    print('Creating Directory ', wwwDir)

#--- Set normalisation 
normalized = False
if normalized:
    normString = '_norm'
else:
    normString = ''

#--- Set Log Scale
setLogY = False

if setLogY:
    logString = '_logScale'
else:
    logString = ''

#--- Set Ratio Plot
setRatioPlot = False

#--- Chose background signal (and comment each background signal you don't want out)
allBkg = [
{'name':'ttv', 'legendName':'t#bar{t}+V', 'target':bkgDir+'mc16d_ttZ/*', 'color': ROOT.TColor.GetColor('#E67067'), 'chain_name':'mc16d_ttZ_Nom'}, 
{'name':'diboson', 'legendName':'Multiboson', 'target':bkgDir+'mc16d_multiboson/*', 'color': ROOT.TColor.GetColor('#54C571'), 'chain_name':'mc16d_multiboson_Nom'}, 
{'name':'singletop', 'legendName':'Single top', 'target':bkgDir+'mc16d_singletop/*', 'color': ROOT.TColor.GetColor('#82DE68'), 'chain_name':'mc16d_singletop_Nom'}, 
{'name':'wjets', 'legendName':'W+jets', 'target':bkgDir+'mc16d_wjets/*', 'color': ROOT.TColor.GetColor('#FCDD5D'), 'chain_name':'mc16d_wjets_Nom'}, 
{'name':'ttbar1L', 'legendName':'t#bar{t} 1L', 'target':bkgDir+'mc16d_ttbar/*', 'color':ROOT.TColor.GetColor('#0F75DB'), 'chain_name':'mc16d_ttbar_Nom', 'addCut':'( tt_cat==1 || tt_cat==4 || tt_cat==7 )' },
{'name':'ttbar2L', 'legendName':'t#bar{t} 2L', 'target':bkgDir+'mc16d_ttbar/*', 'color':ROOT.TColor.GetColor('#A5C6E8'), 'chain_name':'mc16d_ttbar_Nom', 'addCut':'( tt_cat==0 || tt_cat==2 || tt_cat==3 || tt_cat==5 || tt_cat==6 )' },
{'name':'ttbar1L1tau', 'legendName':'t#bar{t} 1L1#tau', 'target':bkgDir+'powheg_ttbar/*', 'color': ROOT.TColor.GetColor('#5E9AD6'), 'chain_name':'powheg_ttbar_Nom', 'addCut':'( tt_cat==2 || tt_cat == 5 ) '}, 
]

#--- Chose signal (Only valid signal so far is the stop_bWN_450_300 signal! Using others will throw errors!)
allSignal = [
#{'name':'stop_bWN_350_200', 'legendName':'m(#tilde{t},#tilde{#chi}_{1}^{0})=(350,200)', 'target':sigDir+'stop_bWN_350_200/*', 'color': ROOT.kBlue+2, 'chain_name':'stop_bWN_350_200_Nom'},
#{'name':'stop_bWN_400_250', 'legendName':'m(#tilde{t},#tilde{#chi}_{1}^{0})=(400,250)', 'target':sigDir+'stop_bWN_400_250/*', 'color': ROOT.kRed, 'chain_name':'stop_bWN_400_250_Nom'},
#{'name':'stop_bWN_450_300', 'legendName':'m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300)', 'target':sigDir+'stop_bWN_450_300_mc16a/*', 'color': ROOT.kGreen, 'chain_name':'stop_bWN_450_300_mc16a_Nom'},
#{'name':'stop_bWN_500_350', 'legendName':'m(#tilde{t},#tilde{#chi}_{1}^{0})=(500,350)', 'target':sigDir+'stop_bWN_500_350/*', 'color': ROOT.kMagenta, 'chain_name':'stop_bWN_500_350_Nom'},
#{'name':'stop_bWN_550_400', 'legendName':'m(#tilde{t},#tilde{#chi}_{1}^{0})=(550,400)', 'target':sigDir+'stop_bWN_550_400/*', 'color': ROOT.kCyan, 'chain_name':'stop_bWN_550_400_Nom'},
#{'name':'stop_bWN_250_100', 'legendName':'m(#tilde{t},#tilde{#chi}_{1}^{0})=(250,100)', 'target':sigDir+'stop_bWN_250_100/*', 'color': ROOT.kBlue+2, 'chain_name':'stop_bWN_250_100_Nom'},
#{'name':'stop_bWN_300_150', 'legendName':'m(#tilde{t},#tilde{#chi}_{1}^{0})=(300,150)', 'target':sigDir+'stop_bWN_300_150/*', 'color': ROOT.kRed, 'chain_name':'stop_bWN_300_150_Nom'},
{'name':'stop_bWN_450_300', 'legendName':'m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300)', 'target':sigDir+'stop_bWN_450_300_mc16d/*', 'color': ROOT.kGreen, 'chain_name':'stop_bWN_450_300_mc16d_Nom'},
#{'name':'stop_bWN_600_450', 'legendName':'m(#tilde{t},#tilde{#chi}_{1}^{0})=(600,450)', 'target':sigDir+'stop_bWN_600_450/*', 'color': ROOT.kMagenta, 'chain_name':'stop_bWN_600_450_Nom'},
#{'name':'stop_bWN_550_400', 'legendName':'m(#tilde{t},#tilde{#chi}_{1}^{0})=(550,400)', 'target':sigDir+'stop_bWN_550_400/*', 'color': ROOT.kGreen, 'chain_name':'stop_bWN_550_400_Nom'},
#{'name':'stop_bWN_600_450', 'legendName':'m(#tilde{t},#tilde{#chi}_{1}^{0})=(600,450)', 'target':sigDir+'stop_bWN_600_450/*', 'color': ROOT.kMagenta, 'chain_name':'stop_bWN_600_450_Nom'},
#{'name':'stop_bWN_650_500', 'legendName':'m(#tilde{t},#tilde{#chi}_{1}^{0})=(650,500)', 'target':sigDir+'stop_bWN_650_500/*', 'color': ROOT.kCyan, 'chain_name':'stop_bWN_650_500_Nom'},
]


for i, sample in enumerate(allBkg+allSignal):
    sample['chain'] = ROOT.TChain(sample['chain_name'])
    sample['chain'].Add(sample['target'])

fileName = datetime.now().strftime('%Y-%m-%d_%H-%M')
filepath = wwwDir + fileName + '_infofile.txt' 

isig = ''
ibkg = ''

for sig in allSignal:
    isig += sig['name'] + '; '
    
for bkg in allBkg:
    ibkg += bkg['name'] + '; '
    
def main():
    
    allVariables = []

    amt2 = {'name':'myAmt2', 'fileName':fileName+'_amt2'+normString+logString, 'varStr':'amt2', 'Xtitle':'am_{T2} [GeV]', 'Ytitle':'Events', 'binning':[30,0,600], 'binningIsExplicit':False}
    met = {'name':'myMET', 'fileName':fileName+'_met'+normString+logString, 'varStr':'(met*0.001)', 'Xtitle':'E_{T}^{miss} [GeV]', 'Ytitle':'Events', 'binning':[50,0,1000], 'binningIsExplicit':False}
    dphi_met_lep = {'name':'mydPhi', 'fileName':fileName+'_dphi_met_lep'+normString+logString, 'varStr':'dphi_met_lep', 'Xtitle':'#Delta#phi(l, E_{T}^{miss})', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
    mt = {'name':'myMT','fileName':fileName+'_mt'+normString+logString, 'varStr':'mt*0.001', 'Xtitle':'m_{T} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    Q = {'name':'myQ','fileName':fileName+'_Q'+normString+logString, 'varStr':'1-mt*mt/(2*met*lep_pt[0])', 'Xtitle':'Q', 'Ytitle':'Events', 'binning':[30,-1,1], 'binningIsExplicit':False}
    njet = {'name':'mynjet','fileName':fileName+'_njet'+normString+logString, 'varStr':'n_jet', 'Xtitle':'N jets', 'Ytitle':'Events', 'binning':[10,0,10], 'binningIsExplicit':False}
    nbjet = {'name':'mynbjet','fileName':fileName+'_nbjet'+normString+logString, 'varStr':'n_bjet', 'Xtitle':'N bjets', 'Ytitle':'Events', 'binning':[10,0,10], 'binningIsExplicit':False}
    jetpt = {'name':'myjetpT','fileName':fileName+'_jetpT'+normString+logString, 'varStr':'jet_pt*0.001', 'Xtitle':'p_{T}^{jet} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    ht = {'name':'myht','fileName':fileName+'_hT'+normString+logString, 'varStr':'ht*0.001', 'Xtitle':'h_{T} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    dphi_jet0_ptmiss = {'name':'mydPhi_jet0ptmiss', 'fileName':fileName+'_dphi_jet0_ptmiss'+normString+logString, 'varStr':'dphi_jet0_ptmiss', 'Xtitle':'#Delta#phi(jet0, p_{T}^{miss})', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
    dphi_jet1_ptmiss = {'name':'mydPhi_jet1ptmiss', 'fileName':fileName+'_dphi_jet1_ptmiss'+normString+logString, 'varStr':'dphi_jet1_ptmiss', 'Xtitle':'#Delta#phi(jet1, p_{T}^{miss})', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
    amm = {'name':'myamm','fileName':fileName+'_amm'+normString+logString, 'varStr':'(met*0.001)*(lep_pt[0]*0.001)', 'Xtitle':'amm', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    leppt0 = {'name':'myleppt0','fileName':fileName+'_lep_pt0'+normString+logString, 'varStr':'lep_pt[0]*0.001', 'Xtitle':'p_{T}^{lep} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    mbl = {'name':'mymbl','fileName':fileName+'_m_bl'+normString+logString, 'varStr':'m_bl*0.001', 'Xtitle':'m_{b,l} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    nlep = {'name':'mynlep','fileName':fileName+'_nlep'+normString+logString, 'varStr':'n_lep', 'Xtitle':'N lep', 'Ytitle':'Events', 'binning':[10,0,10], 'binningIsExplicit':False}
    lep_phi = {'name':'mylphi', 'fileName':fileName+'_lep_phi'+normString+logString, 'varStr':'lep_phi', 'Xtitle':'#phi(l)', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
    lep_eta = {'name':'myleta', 'fileName':fileName+'_lep_eta'+normString+logString, 'varStr':'lep_eta', 'Xtitle':'#eta(l)', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
    R = {'name':'myR', 'fileName':fileName+'_R'+normString+logString, 'varStr':'lep_phi*lep_phi+lep_eta*lep_eta', 'Xtitle':'R', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
    jetpt0 = {'name':'myjetpT0','fileName':fileName+'_jetpT0'+normString+logString, 'varStr':'jet_pt[0]*0.001', 'Xtitle':'p_{T}^{jet0} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    jetpt1 = {'name':'myjetpT1','fileName':fileName+'_jetpT1'+normString+logString, 'varStr':'jet_pt[1]*0.001', 'Xtitle':'p_{T}^{jet1} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    jetpt2 = {'name':'myjetpT2','fileName':fileName+'_jetpT2'+normString+logString, 'varStr':'jet_pt[2]*0.001', 'Xtitle':'p_{T}^{jet2} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    jetpt3 = {'name':'myjetpT3','fileName':fileName+'_jetpT3'+normString+logString, 'varStr':'jet_pt[3]*0.001', 'Xtitle':'p_{T}^{jet3} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    metsig = {'name':'myMET_sig', 'fileName':fileName+'_met_sig'+normString+logString, 'varStr':'met_sig', 'Xtitle':'E_{T}^{miss, sig}', 'Ytitle':'Events', 'binning':[30,0,50], 'binningIsExplicit':False}
    htsig ={'name':'myhT_sig', 'fileName':fileName+'_hT_sig'+normString+logString, 'varStr':'ht_sig', 'Xtitle':'h_{T}^{sig}', 'Ytitle':'Events', 'binning':[30,0,50], 'binningIsExplicit':False}
    dphi_b_lep_max = {'name':'mydPhi_blepmax', 'fileName':fileName+'_dphi_b_lep_max'+normString+logString, 'varStr':'dphi_b_lep_max', 'Xtitle':'max(#Delta#phi(b, l))', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
    dphi_b_ptmiss_max = {'name':'mydPhi_bptmissmax', 'fileName':fileName+'_dphi_b_ptmiss_max'+normString+logString, 'varStr':'dphi_b_ptmiss_max', 'Xtitle':'max(#Delta#phi(b, p_{T}^{miss}))', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
    metprojlep = {'name':'myMETprojLEP', 'fileName':fileName+'_met_proj_lep'+normString+logString, 'varStr':'met_proj_lep*0.001', 'Xtitle':'E_{T,l}^{miss} [GeV]', 'Ytitle':'Events', 'binning':[30,0,600], 'binningIsExplicit':False}
    dRbjetlep = {'name':'mydRbjetlep', 'fileName':fileName+'_dr_bjet_lep'+normString+logString, 'varStr':'dr_bjet_lep', 'Xtitle':'#DeltaR(b,l)', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
    bjetpt = {'name':'myBjetpT','fileName':fileName+'_bjet_pt'+normString+logString, 'varStr':'bjet_pt*0.001', 'Xtitle':'p_{T}^{bjet} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    bjetpt0 = {'name':'myBjetpT0','fileName':fileName+'_bjet_pt0'+normString+logString, 'varStr':'bjet_pt[0]*0.001', 'Xtitle':'p_{T}^{bjet0} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    bjetpt1 = {'name':'myBjetpT1','fileName':fileName+'_bjet_pt1'+normString+logString, 'varStr':'bjet_pt[1]*0.001', 'Xtitle':'p_{T}^{bjet1} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
    mTblMET = {'name':'myMtblMet','fileName':fileName+'_mT_blMET'+normString+logString, 'varStr':'mT_blMET*0.001', 'Xtitle':'m_{T}^{blMET} [GeV]', 'Ytitle':'Events', 'binning':[50,100,700], 'binningIsExplicit':False}
    mjet1jet2 = {'name':'myM_jet1_jet2T','fileName':fileName+'_m_jet1_jet2'+normString+logString, 'varStr':'m_jet1_jet2*0.001', 'Xtitle':'m_{jet1,jet2} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}


#--- Chose which variables to plot by appending only wished variables and commenting everything out

    allVariables.append(met)
    allVariables.append(mt)
    #allVariables.append(dphi_met_lep)
    #allVariables.append(amt2)
    #allVariables.append(Q)
    allVariables.append(njet)
    #allVariables.append(nbjet)
    #allVariables.append(jetpt)
    #allVariables.append(ht)
    allVariables.append(dphi_jet0_ptmiss)
    allVariables.append(dphi_jet1_ptmiss)
    ##allVariables.append(amm)
    #allVariables.append(leppt0)
    #allVariables.append(mbl)
    #allVariables.append(lep_phi)
    #allVariables.append(lep_eta)
    #allVariables.append(R)
    #allVariables.append(jetpt0)
    #allVariables.append(jetpt1)
    #allVariables.append(jetpt2)
    #allVariables.append(jetpt3)
    #allVariables.append(metsig)
    #allVariables.append(htsig)
    #allVariables.append(dphi_b_lep_max)
    #allVariables.append(dphi_b_ptmiss_max)
    #allVariables.append(metprojlep)
    #allVariables.append(dRbjetlep)
    #allVariables.append(bjetpt)
    #allVariables.append(mTblMET)
    #allVariables.append(bjetpt0)
    #allVariables.append(bjetpt1)
    ##allVariables.append(mjet1jet2) #Does not exist
    #allVariables.append(nlep)
    

#--- Set cuts

    #cut = '(n_jet>=4) && (n_lep==1) && (n_bjet>=1) && (met>=200e3) && (mt>=90e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && ( (dphi_b_lep_max<2.5) || (dphi_b_lep_max>2.5 && ((ht>300e3) || (ht<200e3)) ) ) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80))'
    
    #cut = '(n_jet>=4) && (n_lep==1) && (n_bjet>=1) && (met>=100e3) && (mt>=90e3)'
    
    cut = '(met >= 250e3) && (n_jet >= 4) && (n_bjet >= 1) && (mt >= 60e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && (jet_pt[0] > 50e3) && (jet_pt[1] > 25e3) && (jet_pt[2] > 25e3) && (jet_pt[3] > 25e3) && (mT2tauLooseTau_GeV < 80)'
    
    #cut = '(n_jet>=4) && (n_lep==1) && (lep_pt[0]>25e3) && (n_bjet>=1) && (mt>=0e3) && (met>=300e3) && (jet_pt[0]>=25e3) && (jet_pt[1]>=25e3) && (jet_pt[2]>=25e3) && (jet_pt[3]>=25e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80))'

    #cut = '(n_jet>=2) && (n_lep==3) && (lep_pt[0]>25e3) && (n_bjet>=1) && (mt>=0e3) && (met>=230e3) && (jet_pt[0]>=25e3) && (jet_pt[1]>=25e3) && (jet_pt[2]>=25e3) && (jet_pt[3]>=25e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80))'
    
    #Cut as BA vom Schramm
    # Plotting funktioniert, aber ich bekomme keinen einzigen Event... Warum?!
    # Stop Masse und Neutralino Masse anders als in seinem Skript.
    # Annahme einer viel hoehren Stop Masse und Neutralino Masse in meinen Daten
    #cut = '(met >= 120e3) && (n_bjet >= 1) && (n_jet >= 4) && (mt >= 60e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && (jet_pt[0] > 50e3) && (jet_pt[1] > 25e3) && (jet_pt[2] > 25e3) && (jet_pt[3] > 25e3) && (mT2tauLooseTau_GeV < 80)' 

    #cut = '(met >= 120e3)'

    #cut = '(n_jet>=2) && (n_lep==3) && (n_bjet>=1) && (met>=100e3) && (mt>=0e3) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80))'
    
# Weghts are set
    weight = str(lumi)+' * weight * xs_weight * sf_total * weight_sherpa22_njets'
    
# Printing infofile
    print 'Saving infofile to ' + filepath
    print 'Using cut: ' + cut
    infofile = open(filepath, 'w')
    infofile.write('Applied cuts: ' + cut + '\n')
    infofile.write('Used weights: ' + weight + '\n')
    infofile.write('Signal Files:' + isig + '\n')
    infofile.write('Background Files:' + ibkg)
    infofile.close()
    
# Artefact
    #var2 = [allVariables[i:i+9] for i in range(0,len(allVariables),9)]
    #for var in var2:    
        #plot(var, fileName, cut, weight, allSignal, allBkg)
        
# Show current status on console
    counter = len(allVariables)
        
    for var in allVariables:
        print '--------', counter, ' variables remaining to plot--------'
        counter -= 1
        plot(var, fileName, cut, weight, allSignal, allBkg)
    
if __name__=='__main__':
    main()
