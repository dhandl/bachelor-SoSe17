#!usr/bin/python2

# import statements
import ROOT
import numpy as np
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

def doFractions(hists, signal, Xtitle='', Ytitle='Fractions'):
  if type(hists) == list:
    hists.sort(key=lambda hist: hist.Integral())
    ntot = []
    for i in range(1, hists[0].GetNbinsX()+1):
      total = 0.
      for h in hists:
        total = total + h.GetBinContent(i)
      ntot.append(total)
 
    hStack = ROOT.THStack('bgstack', 'Background contributions')
    for hist in hists:
      h = hist.Clone()
      h.Reset()
      for i in range(1, hist.GetNbinsX()+1):
        try:
          h.SetBinContent(i, hist.GetBinContent(i)/ntot[i-1])
        except ZeroDivisionError:
          pass
      hStack.Add(h)

    hStack.SetMinimum(0.0)
    hStack.SetMaximum(1.0)
    hStack.Draw('hist')
    hStack.GetXaxis().SetTitle(Xtitle)
    hStack.GetYaxis().SetTitle(Ytitle)
    hStack.GetYaxis().SetNdivisions(505)
    hStack.GetYaxis().SetTitleSize(16)
    hStack.GetYaxis().SetTitleFont(43)
    hStack.GetYaxis().SetTitleOffset(2.0)
    hStack.GetYaxis().SetLabelFont(43)
    hStack.GetYaxis().SetLabelSize(18)
    #hStack.GetYaxis().SetLabelOffset(0.015)
    hStack.GetXaxis().SetNdivisions(510)
    hStack.GetXaxis().SetTitleSize(16)
    hStack.GetXaxis().SetTitleFont(43)
    hStack.GetXaxis().SetTitleOffset(3.4)
    hStack.GetXaxis().SetLabelFont(43)
    hStack.GetXaxis().SetLabelSize(16)
    #hStack.GetXaxis().SetLabelOffset(0.04)

    s = signal.Clone()
    for i in range(1, s.GetNbinsX()+1):
      try:
        s.SetBinContent(i, s.GetBinContent(i)/(ntot[i-1]+s.GetBinContent(i)))
      except ZeroDivisionError:
        pass
    #s.Draw('same')
    return hStack, s 
  else:
    print 'Histograms must be passed as a list!'   
    return 0

def  outputTransform(sig, sig_var, bkg, bkg_var, binning):
  zb = 2
  zs = 1
  relUnc_bkg = 0.25
  nSig = 15.
  
  db = (binning[2] - binning[1]) / binning[0]
  print binning, db
 
  ntotBkg = bkg.sum()
  ntotBkg_err = np.sqrt(bkg_var.sum()) 
  ntotSig = sig.sum()
  ntotSig_err = np.sqrt(sig_var.sum())

  nbins = len(sig)
  rebinned = [1.]
  last = -1
  print 'DEBUG: ', ntotBkg, sig, bkg
  for b in range(nbins-1,-1, -1):
    print 'DEBUG: Output transform at: ',b
    if last < 0:
      if bkg[b:].sum() > 0.:
        relBkg = np.sqrt(bkg_var[b:].sum()) / bkg[b:].sum()
        llrs = np.ma.masked_invalid(sig[b:] * np.log(1 + sig[b:]/bkg[b:])).sum()
        Z = np.sqrt(zb * bkg[b:].sum() / ntotBkg) + np.sqrt(zs * llrs)
        print 'DEBUG: ',sig[b:].sum(), bkg[b:].sum(), llrs, Z, relBkg,
      else:
        continue
    else:
      if bkg[b:last].sum() > 0.:
        relBkg = np.sqrt(bkg_var[b:last].sum()) / bkg[b:last].sum()
        llrs = np.sum(sig[b:last] * np.log(1 + sig[b:last]/bkg[b:last]))
        Z = np.sqrt(zb * bkg[b:last].sum() / ntotBkg) + np.sqrt(zs * llrs)
        print 'DEBUG: ',sig[b:last].sum(), bkg[b:last].sum(), llrs, Z, relBkg,
      else:
        continue

    if relBkg < relUnc_bkg and sig[b:last].sum() > nSig:
      print "DEBUG: Found bin from {} to {}".format(last,b) 
      last = b
      nSig = nSig - 2.
      print binning[2] - (nbins - b)*db
      rebinned.append(binning[2] - (nbins - b)*db)
      #if sig[b:last].sum()/ (bkg[b:last].sum() + sig[b:last].sum()):
      if nSig<0:
        print 'Signal contamination too low!'
        break

  rebinned.append(0.) 
  print "Output transform done: ", rebinned
  rebinned.reverse()
  return rebinned 


def plot(var, fileName, cut, weight, allSignal, allBkg):
  """ Creates a plot """
  
  histos = {}

  sig = []
  sig_var = []
  first = True
  for sample in allBkg+allSignal:
    
    print sample['name']
 
    histos[sample['name']] = {}

    histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'],*var['binning'])
    
    # Check if variable has explicit cutt
    if sample.has_key('addCut'):
      cutString = cut+' && '+sample['addCut']
    else:
      cutString = cut
    
    # Draws value of key "chain"
    sample['chain'].Draw(var['varStr']+'>>'+histos[sample['name']][var['name']].GetName(), '('+weight+') * ('+cutString+')','goff')

    nbins = histos[sample['name']][var['name']].GetNbinsX()

    if not sample.has_key("isSignal") and first:
      totBkg = nbins*[0.]
      totBkg_var = nbins*[0.]
      first = False
      
    for i in range(nbins):  
      y = histos[sample['name']][var['name']].GetBinContent(i+1)
      y_err = histos[sample['name']][var['name']].GetBinError(i+1)
      y_var = y_err * y_err

      if sample.has_key("isSignal") and sample['isSignal']:
        sig.append(y)
        sig_var.append(y_var)

      else:
        totBkg[i] = totBkg[i] + y
        totBkg_var[i] = totBkg_var[i] + y_var

  sig = np.array(sig) 
  sig_var = np.array(sig_var)
  totBkg = np.array(totBkg) 
  totBkg_var = np.array(totBkg_var)
  rebinned = outputTransform(sig, sig_var, totBkg, totBkg_var, var['binning']) 

  # Redraw the hists with variable bin width
  for sample in allBkg+allSignal:

    histos[sample['name']][var['name']] = ROOT.TH1F(sample['name']+'_'+var['name'], sample['name']+'_'+var['name'], len(rebinned)-1, array('d', rebinned))
    
    # Check if variable has explicit cutt
    if sample.has_key('addCut'):
      cutString = cut+' && '+sample['addCut']
    else:
      cutString = cut
    
    # Draws value of key "chain"
    sample['chain'].Draw(var['varStr']+'>>'+histos[sample['name']][var['name']].GetName(), '('+weight+') * ('+cutString+')','goff')

  
  canv = ROOT.TCanvas(var['name']+'_Window',var['name']+'_Window',600,500)
  if setRatioPlot or BgFractions:
    pad1 = ROOT.TPad('pad1','pad1',0.,0.3,1.,1.)
    pad1.SetBottomMargin(0.018)
    pad1.SetRightMargin(0.06)
    pad1.SetTopMargin(0.06)
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
  bkgHists = []    

  # Draw each background sample in histogram and stack values!
  for sample in allBkg:
    histos[sample['name']][var['name']].SetLineColor(ROOT.kBlack)
    histos[sample['name']][var['name']].SetLineWidth(2)
    histos[sample['name']][var['name']].SetFillColor(sample['color'])
    histos[sample['name']][var['name']].SetMarkerStyle(0)
    histos[sample['name']][var['name']].GetXaxis().SetTitle(var['Xtitle'])
    histos[sample['name']][var['name']].GetYaxis().SetTitle(var['Ytitle'])# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
    if setRatioPlot or BgFractions:
      histos[sample['name']][var['name']].GetXaxis().SetLabelSize(0.0)
    #histos[sample['name']][var['name']].GetYaxis().SetLabelSize(0.04)
    stack.Add(histos[sample['name']][var['name']])
    legend.AddEntry(histos[sample['name']][var['name']], sample['legendName'],'f')
    bkgHists.append(histos[sample['name']][var['name']])
          
  stack.Draw('hist')
  stack.GetXaxis().SetTitle(var['Xtitle'])
  if setRatioPlot or BgFractions:
    stack.GetXaxis().SetLabelSize(0.0)
  stack.GetYaxis().SetTitle(var['Ytitle'])# / '+ str( (var['binning'][2] - var['binning'][1])/var['binning'][0])+'GeV')
  
  # Check for logarithmic scale    
  if setLogY:
    stack.SetMinimum(10**(-2))
    stack.SetMaximum(100*stack.GetMaximum())
  else:
    stack.SetMinimum(0.)
    stack.SetMaximum(1.7*stack.GetMaximum())
  
  # Plotting signal in same histogram with set style. Do NOT stack!
  for sig in allSignal:
    histos[sig['name']][var['name']].SetLineColor(sig['color'])
    histos[sig['name']][var['name']].SetLineWidth(2)
    histos[sig['name']][var['name']].SetLineStyle(ROOT.kDashed)
    histos[sig['name']][var['name']].SetFillColor(0)
    histos[sig['name']][var['name']].SetMarkerStyle(0)
    if setRatioPlot or BgFractions:
      histos[sample['name']][var['name']].GetXaxis().SetLabelSize(0.0)
    
    # Trick for scaling up signal data and make it more visible, fakes higher luminosity for better visibility
    # Comment out if not needed.        
    #if histos['ttbar1L'][var['name']].Integral()>0.:
    #    histos[sig['name']][var['name']].Scale(histos['ttbar1L'][var['name']].Integral()/histos[sig['name']][var['name']].Integral())
    
    # Draw        
    histos[sig['name']][var['name']].Draw('hist same')
    legend.AddEntry(histos[sig['name']][var['name']], sig['legendName'])
                      
  legend.Draw()

  canv.cd()

  # Check if ratio plot is true. If ratio plot is set, two diagrams will appear
  if setRatioPlot:
      helpers.ATLASLabelRatioPad(0.18,0.89,'Work in progress')
      helpers.ATLASLumiLabelRatioPad(0.18,0.88, str(lumi*0.001))
      pad2 = ROOT.TPad('pad2','pad2',0.,0.,1.,0.3)
      pad2.SetTopMargin(0.01)
      pad2.SetBottomMargin(0.32)
      pad2.SetRightMargin(0.06)
      pad2.SetGrid()
      pad2.Draw()
      pad2.cd()


      ratio1 = doRatio(histos['ttbar2L'][var['name']],histos['ttbar1L'][var['name']],var['Xtitle'])
      ratio1.Draw('hist')

  elif BgFractions:
    ATLASLabel(0.18,0.88,'Work in progress')
    ATLASLumiLabel(0.18,0.86, str(lumi*0.001))
    pad2 = ROOT.TPad('pad2','pad2',0.,0.,1.,0.3)
    pad2.SetTopMargin(0.01)
    pad2.SetBottomMargin(0.32)
    pad2.SetRightMargin(0.06)
    pad2.SetGrid()
    pad2.Draw()
    pad2.cd()
    
    bkgFrac, sigFrac =doFractions(bkgHists, histos['stop_bWN_450_300'][var['name']], var['Xtitle'])
    bkgFrac.Draw('hist')
    sigFrac.Draw('hist same')
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
wwwDir = '/project/etp5/dhandl/MachineLearning/plots/evaluateRNNTruthReo/outputTransform/'


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
#----------------------------#
setRatioPlot = False 
BgFractions = True
#----------------------------#


#--- Chose background signal (and comment each background signal you don't want out)
allBkg = [
{'name':'ttz', 'legendName':'t#bar{t}+Z', 'target':bkgDir+'mc16d_ttZ/*.root', 'color': ROOT.TColor.GetColor('#E67067'), 'chain_name':'mc16d_ttZ_Nom'}, 
{'name':'multiboson', 'legendName':'Multiboson', 'target':bkgDir+'mc16d_multiboson/*.root', 'color': ROOT.TColor.GetColor('#54C571'), 'chain_name':'mc16d_multiboson_Nom'}, 
{'name':'singletop', 'legendName':'Single top', 'target':bkgDir+'mc16d_singletop/*.root', 'color': ROOT.TColor.GetColor('#82DE68'), 'chain_name':'mc16d_singletop_Nom'}, 
{'name':'wjets', 'legendName':'W+jets', 'target':bkgDir+'mc16d_wjets/*.root', 'color': ROOT.TColor.GetColor('#FCDD5D'), 'chain_name':'mc16d_wjets_Nom'}, 
{'name':'ttbar1L', 'legendName':'t#bar{t} 1L', 'target':bkgDir+'mc16d_ttbar/*.root', 'color':ROOT.TColor.GetColor('#0F75DB'), 'chain_name':'mc16d_ttbar_Nom', 'addCut':'( tt_cat==1 || tt_cat==4 || tt_cat==7 )' },
{'name':'ttbar2L', 'legendName':'t#bar{t} 2L', 'target':bkgDir+'mc16d_ttbar/*', 'color':ROOT.TColor.GetColor('#A5C6E8'), 'chain_name':'mc16d_ttbar_Nom', 'addCut':'( tt_cat==0 || tt_cat==2 || tt_cat==3 || tt_cat==5 || tt_cat==6 )' },
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
{'name':'stop_bWN_450_300', 'legendName':'m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,300)', 'target':sigDir+'stop_bWN_450_300_mc16d/*', 'color': ROOT.kRed, 'chain_name':'stop_bWN_450_300_mc16d_Nom', 'isSignal':True},
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
    
  amt2 = {'name':'myAmt2', 'fileName':fileName+'_amt2'+normString+logString, 'varStr':'amt2', 'Xtitle':'am_{T2} [GeV]', 'Ytitle':'Events', 'binning':[25,80,130], 'binningIsExplicit':False}
  met = {'name':'myMET', 'fileName':fileName+'_met'+normString+logString, 'varStr':'(met*0.001)', 'Xtitle':'E_{T}^{miss} [GeV]', 'Ytitle':'Events', 'binning':[50,0,1000], 'binningIsExplicit':False}
  dphi_met_lep = {'name':'mydPhi', 'fileName':fileName+'_dphi_met_lep'+normString+logString, 'varStr':'dphi_met_lep', 'Xtitle':'#Delta#phi(l, E_{T}^{miss})', 'Ytitle':'Events', 'binning':[32,0,3.2], 'binningIsExplicit':False}
  mt = {'name':'myMT','fileName':fileName+'_mt'+normString+logString, 'varStr':'mt*0.001', 'Xtitle':'m_{T} [GeV]', 'Ytitle':'Events', 'binning':[40,100,500], 'binningIsExplicit':False}
  njet = {'name':'mynjet','fileName':fileName+'_njet'+normString+logString, 'varStr':'n_jet', 'Xtitle':'n_{jet}', 'Ytitle':'Events', 'binning':[11,-0.5,10.5], 'binningIsExplicit':False}
  nbjet = {'name':'mynbjet','fileName':fileName+'_nbjet'+normString+logString, 'varStr':'n_bjet', 'Xtitle':'n_{b-jet}', 'Ytitle':'Events', 'binning':[6,-0.5,5.5], 'binningIsExplicit':False}
  ht = {'name':'myht','fileName':fileName+'_hT'+normString+logString, 'varStr':'ht*0.001', 'Xtitle':'H_{T} [GeV]', 'Ytitle':'Events', 'binning':[25,0,500], 'binningIsExplicit':False}
  dphi_jet0_ptmiss = {'name':'mydPhi_jet0ptmiss', 'fileName':fileName+'_dphi_jet0_ptmiss'+normString+logString, 'varStr':'dphi_jet0_ptmiss', 'Xtitle':'#Delta#phi(1^{st} jet, p_{T}^{miss})', 'Ytitle':'Events', 'binning':[32,0,3.2], 'binningIsExplicit':False}
  dphi_jet1_ptmiss = {'name':'mydPhi_jet1ptmiss', 'fileName':fileName+'_dphi_jet1_ptmiss'+normString+logString, 'varStr':'dphi_jet1_ptmiss', 'Xtitle':'#Delta#phi(2^{nd} jet, p_{T}^{miss})', 'Ytitle':'Events', 'binning':[32,0,3.2], 'binningIsExplicit':False}
  leppt0 = {'name':'myleppt0','fileName':fileName+'_lep_pt0'+normString+logString, 'varStr':'lep_pt[0]*0.001', 'Xtitle':'p_{T}^{lep} [GeV]', 'Ytitle':'Events', 'binning':[25,0,500], 'binningIsExplicit':False}
  mbl = {'name':'mymbl','fileName':fileName+'_m_bl'+normString+logString, 'varStr':'m_bl*0.001', 'Xtitle':'m_{b,l} [GeV]', 'Ytitle':'Events', 'binning':[25,0,500], 'binningIsExplicit':False}
  lep_phi = {'name':'mylphi', 'fileName':fileName+'_lep_phi'+normString+logString, 'varStr':'lep_phi', 'Xtitle':'#phi(l)', 'Ytitle':'Events', 'binning':[16,0,3.2], 'binningIsExplicit':False}
  lep_eta = {'name':'myleta', 'fileName':fileName+'_lep_eta'+normString+logString, 'varStr':'lep_eta', 'Xtitle':'#eta(l)', 'Ytitle':'Events', 'binning':[32,-3.2,3.2], 'binningIsExplicit':False}
  R = {'name':'myR', 'fileName':fileName+'_R'+normString+logString, 'varStr':'lep_phi*lep_phi+lep_eta*lep_eta', 'Xtitle':'R', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
  jetpt0 = {'name':'myjetpT0','fileName':fileName+'_jetpT0'+normString+logString, 'varStr':'jet_pt[0]*0.001', 'Xtitle':'p_{T}^{jet1} [GeV]', 'Ytitle':'Events', 'binning':[40,0,800], 'binningIsExplicit':False}
  jetpt1 = {'name':'myjetpT1','fileName':fileName+'_jetpT1'+normString+logString, 'varStr':'jet_pt[1]*0.001', 'Xtitle':'p_{T}^{jet2} [GeV]', 'Ytitle':'Events', 'binning':[30,0,600], 'binningIsExplicit':False}
  jetpt2 = {'name':'myjetpT2','fileName':fileName+'_jetpT2'+normString+logString, 'varStr':'jet_pt[2]*0.001', 'Xtitle':'p_{T}^{jet3} [GeV]', 'Ytitle':'Events', 'binning':[25,0,500], 'binningIsExplicit':False}
  jetpt3 = {'name':'myjetpT3','fileName':fileName+'_jetpT3'+normString+logString, 'varStr':'jet_pt[3]*0.001', 'Xtitle':'p_{T}^{jet4} [GeV]', 'Ytitle':'Events', 'binning':[20,0,400], 'binningIsExplicit':False}
  metsig = {'name':'myMET_sig', 'fileName':fileName+'_met_sig'+normString+logString, 'varStr':'met_sig', 'Xtitle':'E_{T}^{miss, sig}', 'Ytitle':'Events', 'binning':[25,0,50], 'binningIsExplicit':False}
  htsig ={'name':'myhT_sig', 'fileName':fileName+'_hT_sig'+normString+logString, 'varStr':'ht_sig', 'Xtitle':'h_{T}^{sig}', 'Ytitle':'Events', 'binning':[25,0,50], 'binningIsExplicit':False}
  dphi_b_lep_max = {'name':'mydPhi_blepmax', 'fileName':fileName+'_dphi_b_lep_max'+normString+logString, 'varStr':'dphi_b_lep_max', 'Xtitle':'max(#Delta#phi(b, l))', 'Ytitle':'Events', 'binning':[32,0,3.2], 'binningIsExplicit':False}
  dphi_b_ptmiss_max = {'name':'mydPhi_bptmissmax', 'fileName':fileName+'_dphi_b_ptmiss_max'+normString+logString, 'varStr':'dphi_b_ptmiss_max', 'Xtitle':'max(#Delta#phi(b, p_{T}^{miss}))', 'Ytitle':'Events', 'binning':[32,0,3.2], 'binningIsExplicit':False}
  metprojlep = {'name':'myMETprojLEP', 'fileName':fileName+'_met_proj_lep'+normString+logString, 'varStr':'met_proj_lep*0.001', 'Xtitle':'E_{T,l}^{miss} [GeV]', 'Ytitle':'Events', 'binning':[30,0,600], 'binningIsExplicit':False}
  dRbjetlep = {'name':'mydRbjetlep', 'fileName':fileName+'_dr_bjet_lep'+normString+logString, 'varStr':'dr_bjet_lep', 'Xtitle':'#DeltaR(b,l)', 'Ytitle':'Events', 'binning':[32,0,3.2], 'binningIsExplicit':False}
  bjetpt = {'name':'myBjetpT','fileName':fileName+'_bjet_pt'+normString+logString, 'varStr':'bjet_pt*0.001', 'Xtitle':'p_{T}^{bjet} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
  bjetpt0 = {'name':'myBjetpT0','fileName':fileName+'_bjet_pt0'+normString+logString, 'varStr':'bjet_pt[0]*0.001', 'Xtitle':'leading p_{T}^{b-jet} [GeV]', 'Ytitle':'Events', 'binning':[25,0,500], 'binningIsExplicit':False}
  bjetpt1 = {'name':'myBjetpT1','fileName':fileName+'_bjet_pt1'+normString+logString, 'varStr':'bjet_pt[1]*0.001', 'Xtitle':'sub-lead. p_{T}^{bjet1} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
  mTblMET = {'name':'myMtblMet','fileName':fileName+'_mT_blMET'+normString+logString, 'varStr':'mT_blMET*0.001', 'Xtitle':'m_{T}^{blMET} [GeV]', 'Ytitle':'Events', 'binning':[30,100,700], 'binningIsExplicit':False}
  output = {'name':'myRNN','fileName':fileName+'_RNN_output'+normString+logString, 'varStr':'outputScore', 'Xtitle':'RNN', 'Ytitle':'Events', 'binning':[100,0.,1.0], 'binningIsExplicit':False}
  ntop = {'name':'myNtop','fileName':fileName+'_NhadTop'+normString+logString, 'varStr':'n_hadtop_cand', 'Xtitle':'n_{had. top}', 'Ytitle':'Events', 'binning':[4,-0.5,3.5], 'binningIsExplicit':False}
  mtop = {'name':'mytop','fileName':fileName+'_reclusteredTopMass'+normString+logString, 'varStr':'hadtop_cand_m[0]', 'Xtitle':'m^{recl.}_{top}', 'Ytitle':'Events', 'binning':[30,0,600], 'binningIsExplicit':False}
  mtopX2 = {'name':'mytopX2','fileName':fileName+'_TopMassX2'+normString+logString, 'varStr':'m_top_chi2', 'Xtitle':'m^{#chi^{2}}_{top}', 'Ytitle':'Events', 'binning':[30,0,600], 'binningIsExplicit':False}

  var = output
  
  cut = '(n_jet>=4) && (n_lep==1) && (lep_pt[0]>25e3) && (n_bjet>=1) && (mt>=110e3) && (met>=230e3) && (jet_pt[0]>=25e3) && (jet_pt[1]>=25e3) && (jet_pt[2]>=25e3) && (jet_pt[3]>=25e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80))'

  weight = str(lumi)+' * weight * xs_weight * sf_total * weight_sherpa22_njets'
  
  print 'Saving infofile to ' + filepath
  print 'Using cut: ' + cut
  infofile = open(filepath, 'w')
  infofile.write('Applied cuts: ' + cut + '\n')
  infofile.write('Used weights: ' + weight + '\n')
  infofile.write('Signal Files:' + isig + '\n')
  infofile.write('Background Files:' + ibkg)
  #infofile.write('Z_threshold: 2.0, zb: 2, zs: 1, relBkg: 0.25')
  infofile.close()
      
  plot(var, fileName, cut, weight, allSignal, allBkg)
    
if __name__=='__main__':
    main()
