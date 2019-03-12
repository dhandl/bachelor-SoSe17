import ROOT
import math
import os, sys

from datetime import datetime
from AtlasStyle import *

ROOT.gStyle.SetPalette(ROOT.kBird)
ROOT.gStyle.SetOptTitle(0)
ROOT.gStyle.SetOptStat(0)

def main():

    wwwDir = "/project/etp5/dhandl/plots/Stop1L/FullRun2/2d/CorrelationMatrix/"
    if not os.path.exists(wwwDir):
        os.makedirs(wwwDir)
        print ('Creating Directory ', wwwDir)

    bkgDir = '/project/etp3/dhandl/samples/SUSY/Stop1L/21.2.58_ML/'
     
    lumi = str(140500.)
    
    #cut = "( " + lumi + " * weight * xs_weight * sf_total * weight_sherpa22_njets * ((stxe_trigger) && (n_jet>=4) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>130e3) && (met>300e3) && (amt2<110) && (dphi_met_lep<2.5) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) ) )"
    
    #cut = "( " + lumi + " * weight * xs_weight * sf_total * weight_sherpa22_njets * ((n_jet>=4) && (n_bjet>0) && (met>=100e3) && (mt>=90e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && ( (dphi_b_lep_max<2.5) || (dphi_b_lep_max>2.5 && ((ht>300e3) || (ht<200e3)) ) ) &&!((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80))) )"
    
    #cut = "( " + lumi + " * weight * xs_weight * sf_total * weight_sherpa22_njets * ((met>=250e3) && (mt>=90e3) && (n_lep==1)) )"
    
    ##########Cuts for NN##########
    #cut = '(n_jet>=4) && (n_lep==1) && (n_bjet>=1) && (mt>=90e3) && (met>=100e3) && (jet_pt[0]>=25e3) && (jet_pt[1]>=25e3) && (jet_pt[2]>=25e3) && (jet_pt[3]>=25e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80))'
    
        
    cut = '(' + lumi + ' * weight * xs_weight * weight_lumi * sf_total * ( (stxe_trigger) && (n_jet>=4) && (n_lep==1) && (lep_pt[0]>25e3) && (n_bjet>=1) && (mt>=110e3) && (met>=230e3) && (jet_pt[0]>=25e3) && (jet_pt[1]>=25e3) && (jet_pt[2]>=25e3) && (jet_pt[3]>=25e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) ))'

    sampleNames = [
            #{'name':'ttz', 'legendName':'t#bar{t}+Z', 'target':bkgDir+'mc16d_ttZ/*.root', 'color': ROOT.TColor.GetColor('#E67067'), 'chain_name':'mc16d_ttZ_Nom'}, 
            #{'name':'multiboson', 'legendName':'Multiboson', 'target':bkgDir+'mc16d_multiboson/*.root', 'color': ROOT.TColor.GetColor('#54C571'), 'chain_name':'mc16d_multiboson_Nom'}, 
            {'name':'ttbar2L', 'legendName':'t#bar{t} 2L', 'target':bkgDir+'mc16e_ttbar/*', 'color':ROOT.TColor.GetColor('#A5C6E8'), 'chain_name':'mc16e_ttbar_Nom', 'addCut':'( tt_cat==0 || tt_cat==2 || tt_cat==3 || tt_cat==5 || tt_cat==6 )' },
            {'name':'stop_bWN_450_330', 'legendName':'m(#tilde{t},#tilde{#chi}_{1}^{0})=(450,330)', 'target':bkgDir+'/default/mc16e_stop_bWN_450_330/*', 'color':ROOT.TColor.GetColor('#A5C6E8'), 'chain_name':'mc16e_stop_bWN_450_330_Nom'},
            {'name':'singletop', 'legendName':'Single top', 'target':bkgDir+'mc16e_singletop/*.root', 'color': ROOT.TColor.GetColor('#82DE68'), 'chain_name':'mc16e_singletop_Nom'}, 
            {'name':'wjets', 'legendName':'W+jets', 'target':bkgDir+'mc16e_wjets/*.root', 'color': ROOT.TColor.GetColor('#FCDD5D'), 'chain_name':'mc16e_wjets_Nom'}, 
            {'name':'ttbar1L', 'legendName':'t#bar{t} 1L', 'target':bkgDir+'mc16e_ttbar/*.root', 'color':ROOT.TColor.GetColor('#0F75DB'), 'chain_name':'mc16e_ttbar_Nom', 'addCut':'( tt_cat==1 || tt_cat==4 || tt_cat>=7 )' },
            #{'name':'ttbar1L1tau', 'legendName':'t#bar{t} 1L1#tau', 'target':bkgDir+'powheg_ttbar/*', 'color': ROOT.TColor.GetColor('#5E9AD6'), 'chain_name':'powheg_ttbar_Nom', 'addCut':'( tt_cat==2 || tt_cat == 5 ) '}, 
    ]

    for i, sample in enumerate(sampleNames):
        sample['chain'] = ROOT.TChain(sample['chain_name'])
        sample['chain'].Add(sample['target'])
 
    histos2D = {}
 
    for sample in sampleNames:
        histos2D[sample['name']] = {}

        fileName = datetime.now().strftime('%Y-%m-%d_%H-%M_') + sample['name']

        if sample.has_key("addCut"):
          cutString = cut + " && " + sample["addCut"]
        else: 
          cutString = cut
        
        allVariables = []
        amt2 = {'name':'myAmt2', 'fileName':fileName+'_amt2', 'varStr':'amt2', 'Xtitle':'am_{T2} [GeV]', 'Ytitle':'Events', 'binning':[20,0,500], 'binningIsExplicit':False}
        met = {'name':'myMET', 'fileName':fileName+'_met', 'varStr':'(met*0.001)', 'Xtitle':'E_{T}^{miss} [GeV]', 'Ytitle':'Events', 'binning':[40,0,1000], 'binningIsExplicit':False}
        metphi = {'name':'myMETphi', 'fileName':fileName+'_metPhi', 'varStr':'(met_phi)', 'Xtitle':'#phi(p_{T}^{miss})', 'Ytitle':'Events', 'binning':[32,-3.2,3.2], 'binningIsExplicit':False}
        dphi = {'name':'mydPhi', 'fileName':fileName+'_dphi_met_lep', 'varStr':'dphi_met_lep', 'Xtitle':'#Delta#phi(l, E_{T}^{miss})', 'Ytitle':'Events', 'binning':[16,0,3.2], 'binningIsExplicit':False}
        mt = {'name':'myMT','fileName':fileName+'_mt', 'varStr':'(mt*0.001)', 'Xtitle':'m_{T} [GeV]', 'Ytitle':'Events', 'binning':[40,0,800], 'binningIsExplicit':False}
        Q = {'name':'myQ','fileName':fileName+'_Q', 'varStr':'1-mt*mt/(2*met*lep_pt[0])', 'Xtitle':'Q', 'Ytitle':'Events', 'binning':[30,-1,1], 'binningIsExplicit':False}
        njet = {'name':'mynjet','fileName':fileName+'_njet', 'varStr':'n_jet', 'Xtitle':'jets', 'Ytitle':'Events', 'binning':[11,-0.5,10.5], 'binningIsExplicit':False}
        nbjet = {'name':'mynbjet','fileName':fileName+'_nbjet', 'varStr':'n_bjet', 'Xtitle':'b-jets', 'Ytitle':'Events', 'binning':[6,-0.5,5.5], 'binningIsExplicit':False}
        ht = {'name':'myht','fileName':fileName+'_hT', 'varStr':'(ht*0.001)', 'Xtitle':'h_{T} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
        dphi_jet0_ptmiss = {'name':'mydPhi_jet0ptmiss', 'fileName':fileName+'_dphi_jet0_ptmiss', 'varStr':'dphi_jet0_ptmiss', 'Xtitle':'#Delta#phi(jet0, p_{T}^{miss})', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
        dphi_jet1_ptmiss = {'name':'mydPhi_jet1ptmiss', 'fileName':fileName+'_dphi_jet1_ptmiss', 'varStr':'dphi_jet1_ptmiss', 'Xtitle':'#Delta#phi(jet1, p_{T}^{miss})', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
        #amm = {'name':'myamm','fileName':fileName+'_amm', 'varStr':'(met*0.001)*(lep_pt[0]*0.001)', 'Xtitle':'amm', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
        leppt0 = {'name':'myleppt0','fileName':fileName+'_lep_pt', 'varStr':'(lep_pt[0]*0.001)', 'Xtitle':'p_{T}^{lep} [GeV]', 'Ytitle':'Events', 'binning':[24,0,600], 'binningIsExplicit':False}
        mbl = {'name':'mymbl','fileName':fileName+'_m_bl', 'varStr':'(m_bl*0.001)', 'Xtitle':'m_{b,l} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
        lepphi0 = {'name':'mylphi', 'fileName':fileName+'_lep_phi', 'varStr':'lep_phi', 'Xtitle':'#phi(l)', 'Ytitle':'Events', 'binning':[16,0,3.2], 'binningIsExplicit':False}
        lepeta0 = {'name':'myleta', 'fileName':fileName+'_lep_eta', 'varStr':'lep_eta', 'Xtitle':'#eta(l)', 'Ytitle':'Events', 'binning':[32,-3.2,3.2], 'binningIsExplicit':False}
        lepe0 = {'name':'mylepe0','fileName':fileName+'_lep_e', 'varStr':'(lep_e[0]*0.001)', 'Xtitle':'E^{lep} [GeV]', 'Ytitle':'Events', 'binning':[40,0,1000], 'binningIsExplicit':False}
        R = {'name':'myR', 'fileName':fileName+'_R', 'varStr':'lep_phi*lep_phi+lep_eta*lep_eta', 'Xtitle':'R', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
        bjetpt0 = {'name':'mybjetpT0','fileName':fileName+'_bjetpt0', 'varStr':'(bjet_pt[0]*0.001)', 'Xtitle':'p_{T}^{bjet1} [GeV]', 'Ytitle':'Events', 'binning':[32,0,800], 'binningIsExplicit':False}
        jetpt0 = {'name':'myjetpT0','fileName':fileName+'_jetpt0', 'varStr':'(jet_pt[0]*0.001)', 'Xtitle':'p_{T}^{jet1} [GeV]', 'Ytitle':'Events', 'binning':[32,0,800], 'binningIsExplicit':False}
        jetpt1 = {'name':'myjetpT1','fileName':fileName+'_jetpt1', 'varStr':'(jet_pt[1]*0.001)', 'Xtitle':'p_{T}^{jet2} [GeV]', 'Ytitle':'Events', 'binning':[24,0,600], 'binningIsExplicit':False}
        jetpt2 = {'name':'myjetpT2','fileName':fileName+'_jetpt2', 'varStr':'(jet_pt[2]*0.001)', 'Xtitle':'p_{T}^{jet3} [GeV]', 'Ytitle':'Events', 'binning':[20,0,500], 'binningIsExplicit':False}
        jetpt3 = {'name':'myjetpT3','fileName':fileName+'_jetpt3', 'varStr':'(jet_pt[3]*0.001)', 'Xtitle':'p_{T}^{jet4} [GeV]', 'Ytitle':'Events', 'binning':[16,0,400], 'binningIsExplicit':False}
        metsig = {'name':'myMET_sig', 'fileName':fileName+'_met_sig', 'varStr':'met_sig', 'Xtitle':'E_{T}^{miss, sig}', 'Ytitle':'Events', 'binning':[30,0,50], 'binningIsExplicit':False}
        htsig ={'name':'myhT_sig', 'fileName':fileName+'_hT_sig', 'varStr':'ht_sig', 'Xtitle':'h_{T}^{sig}', 'Ytitle':'Events', 'binning':[30,0,50], 'binningIsExplicit':False}
        dphi_b_lep_max = {'name':'mydPhi_blepmax', 'fileName':fileName+'_dphi_b_lep_max', 'varStr':'dphi_b_lep_max', 'Xtitle':'max(#Delta#phi(b, l))', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
        dphi_b_ptmiss_max = {'name':'mydPhi_bptmissmax', 'fileName':fileName+'_dphi_b_ptmiss_max', 'varStr':'dphi_b_ptmiss_max', 'Xtitle':'max(#Delta#phi(b, p_{T}^{miss}))', 'Ytitle':'Events', 'binning':[40,0,3.2], 'binningIsExplicit':False}
        metprojlep = {'name':'myMETprojLEP', 'fileName':fileName+'_met_proj_lep', 'varStr':'met_proj_lep*0.001', 'Xtitle':'E_{T,l}^{miss} [GeV]', 'Ytitle':'Events', 'binning':[30,0,600], 'binningIsExplicit':False}
        dRbjetlep = {'name':'mydRbjetlep', 'fileName':fileName+'_dr_bjet_lep', 'varStr':'dr_bjet_lep', 'Xtitle':'#DeltaR(b,l)', 'Ytitle':'Events', 'binning':[40,0,4], 'binningIsExplicit':False}
        bjetpt1 = {'name':'myBjetpT1','fileName':fileName+'_bjet_pt1', 'varStr':'(bjet_pt[1]*0.001)', 'Xtitle':'p_{T}^{bjet1} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], 'binningIsExplicit':False}
        mTblMET = {'name':'myMtblMet','fileName':fileName+'_mT_blMET', 'varStr':'(mT_blMET*0.001)', 'Xtitle':'m_{T}^{blMET} [GeV]', 'Ytitle':'Events', 'binning':[50,100,700], 'binningIsExplicit':False}
        mtopX2 = {'name':'mymtopX2','fileName':fileName+'_m_top_chi2', 'varStr':'m_top_chi2', 'Xtitle':'m_{top}^{#chi 2} [GeV]', 'Ytitle':'Events', 'binning':[40,0,800], 'binningIsExplicit':False}
        mtop = {'name':'mymtop','fileName':fileName+'_m_top_reclustered', 'varStr':'(hadtop_cand_m[0]*0.001)', 'Xtitle':'m_{top}^{reclustered} [GeV]', 'Ytitle':'Events', 'binning':[20,0,400], 'binningIsExplicit':False}
        output = {'name':'myML','fileName':fileName+'_RNN_output', 'varStr':'outputScore_RNN', 'Xtitle':'RNN', 'Ytitle':'Events', 'binning':[25,0,1], 'binningIsExplicit':False}


        #allVariables.append(dRbjetlep)
        allVariables.append(met)
        allVariables.append(metphi)
        allVariables.append(mt)
        allVariables.append(dphi)
        allVariables.append(mbl)
        allVariables.append(bjetpt0)
        allVariables.append(njet)
        allVariables.append(nbjet)
        allVariables.append(leppt0)
        allVariables.append(lepphi0)
        allVariables.append(lepeta0)
        allVariables.append(lepe0)
        #allVariables.append(Q)
        #allVariables.append(jetpt)
        #allVariables.append(ht)
        #allVariables.append(dphi_jet0_ptmiss)
        #allVariables.append(dphi_jet1_ptmiss)
        #allVariables.append(R)
        allVariables.append(jetpt0)
        allVariables.append(jetpt1)
        allVariables.append(jetpt2)
        allVariables.append(jetpt3)
        #allVariables.append(metsig)
        #allVariables.append(htsig)
        #allVariables.append(dphi_b_lep_max)
        #allVariables.append(dphi_b_ptmiss_max)
        #allVariables.append(metprojlep)
        #allVariables.append(mTblMET)
        allVariables.append(output)
        
        print 'Using cut: ' + cutString
        
        
        #-------------Plot one variable to the rest of the list-----------
        
        print 'Plotting ' + str(len(allVariables)-1) + ' diagrams...'

        for var in allVariables:
          for var2 in allVariables:
            histos2D[sample['name']][var['name']+'_vs_'+var2['name']] = {}
            histos2D[sample['name']][var['name']+'_vs_'+var2['name']]['hist'] = ROOT.TH2F(sample['name']+'_'+var['name']+'_vs_'+var2['name'], sample['name']+'_'+var['name']+'_vs_'+var2['name'], var2['binning'][0],var2['binning'][1],var2['binning'][2], var['binning'][0], var['binning'][1], var['binning'][2])
            
            sample['chain'].Draw(var2['varStr']+':'+var['varStr']+'>>'+histos2D[sample['name']][var['name']+'_vs_'+var2['name']]['hist'].GetName(), cutString, 'goff')

        # obtain correlation factor
        for var in allVariables:
          for var2 in allVariables:
            histos2D[sample['name']][var['name']+'_vs_'+var2['name']]['corrFac'] = histos2D[sample['name']][var['name']+'_vs_'+var2['name']]['hist'].GetCorrelationFactor()
            print "Correlation in Sample {} of {} vs {}: {}".format(sample['name'], var['name'], var2['name'], histos2D[sample['name']][var['name']+'_vs_'+var2['name']]['corrFac'])
 
        corrCanvas = ROOT.TCanvas('Correlation '+sample['name'],'Correlation '+sample['name'],1600,1600)
        corr2D = ROOT.TH2F('Correlation Matrix '+sample['name'],'Correlation Matrix '+sample['name'],len(allVariables),0,len(allVariables),len(allVariables),0,len(allVariables))
        corr2D.SetMaximum(100)
        corr2D.SetMinimum(-100)
        for i_var, var in enumerate(allVariables):
          corr2D.GetXaxis().SetBinLabel(i_var+1, var['Xtitle'])
          corr2D.GetYaxis().SetBinLabel(i_var+1, var['Xtitle'])
          for i_var2, var2 in enumerate(allVariables):
            corr2D.SetBinContent(i_var2+1, i_var+1, 100*round(histos2D[sample['name']][var['name']+'_vs_'+var2['name']]['corrFac'],3))
        corr2D.Draw('COLZ TEXT')
        corrCanvas.Print(wwwDir+fileName+'.root')
        corrCanvas.Print(wwwDir+fileName+'.png')
        corrCanvas.Print(wwwDir+fileName+'.pdf')

    filepath = wwwDir + fileName + '_infofile.txt'
      
    print 'Saving infofile to' + filepath
    infofile = open(filepath, 'w')
    infofile.write('Applied cuts: ' + cut)
    infofile.close()
        
if __name__ == "__main__":
    main()
