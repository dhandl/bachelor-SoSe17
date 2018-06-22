import ROOT
import math
import os, sys

from datetime import datetime
from AtlasStyle import *

def plot(var1, var2, sampleName, xtitle, ytitle, cut, fileName, bins1, bins2):
    SetAtlasStyle()
    ROOT.gStyle.SetOptTitle(0)
    ROOT.gStyle.SetOptStat(0)

    ROOT.TGaxis().SetMaxDigits(4)

    wwwDir = "/project/etp5/aschwemmer/bachelor-SoSe17/plots/2D/"
    if not os.path.exists(wwwDir):
        os.makedirs(wwwDir)
        print ('Creating Directory ', wwwDir)

    sampleDir = '/project/etp5/dhandl/samples/SUSY/Stop1L/'
    
    #fileName = fileName +'_'+var1+'vs'+var2
    #fileName = fileName.replace('*0.001','').replace('/','D')

    c=ROOT.TChain(sampleName+'_Nom')
    c.Add(sampleDir+sampleName+'/*')
    
    #xbins=30
    #xstart=0
    #xstop=600
    #ybins=30
    #ystart=0
    #ystop=600
    
    #if var1 in ('n_jet','n_bjet'):
        #xbins=12
        #xstart=0
        #xstop=12
    
    #if var2 in ('n_jet','n_bjet'):
        #ybins=12
        #ystart=0
        #ystop=12
    
    #if var1 in ('dphi_jet0_ptmiss','dphi_jet1_ptmiss','dphi_met_lep'):
        #xbins=40
        #xstart=0
        #xstop=3.2
        
    #if var2 in ('dphi_jet0_ptmiss','dphi_jet1_ptmiss','dphi_met_lep'):
        #ybins=40
        #ystart=0
        #ystop=3.2
        
    #if (var1=='1-mt*mt/(2*met*lep_pt[0])'):
        #xbins=40
        #xstart=-1
        #xstop=1
        
    #if (var2=='1-mt*mt/(2*met*lep_pt[0])'):
        #ybins=40
        #ystart=-1
        #ystop=-1
    
    #For var1
    xbins = bins1[0]
    xstart = bins1[1]
    xstop = bins1[2]
    
    #For var2
    ybins=bins2[0]
    ystart=bins2[1]
    ystop=bins2[2]

    h=ROOT.TH2F("h","h",ybins,ystart,ystop,xbins,xstart,xstop)
    c.Draw(var1+':'+var2+'>>h',cut,"goff") #Erst y, dann x

    c0 = ROOT.TCanvas("c0","c0",600,500)
    c0.SetFillColor(10)
    c0.SetBorderSize(1)
    #c0.SetLogz()
    c0.SetRightMargin(0.15)
    #c0.SetGridy()
    #c0.SetGridx()

    h.Draw("colz")
    h.GetYaxis().SetTitle(ytitle)
    #h.GetYaxis().SetTitle("#Delta#Phi(E_{T}^{miss},l)")
    h.GetXaxis().SetTitle(xtitle)

    corr = h.GetCorrelationFactor()

    ATLASLabel(0.18,0.9,"Work in progress")
    ATLASLumiLabel(0.18,0.89,"140.0")

    text = ROOT.TLatex()
    text.SetNDC()
    text.SetTextSize(0.045)
    text.SetTextAlign(11) 
    text.DrawLatex(0.1,0.04,"r = %.3f"%corr)
    #text.DrawLatex(0.5,0.8,"m(#tilde{t},#tilde{#chi}_{1}^{0})_{3-body}=(%i,%i) GeV"%(sig[0],sig[1]))
    #ROOT.myText(0.15,0.335,1,"Data 16, RN 297041")
    #ROOT.myText(0.15,0.285,1,"#sqrt{s} = 13TeV")
    #ROOT.myText(0.15,0.235,1,"Elec. Noise [MeV], EM1")
    
    print 'Saving File to ' + wwwDir+fileName

    c0.SaveAs(wwwDir+fileName+".pdf")
    c0.SaveAs(wwwDir+fileName+".root")
    c0.SaveAs(wwwDir+fileName+".png")

def main():
    
    lumi = str(140000.)
    
    #cut = "( " + lumi + " * weight * xs_weight * sf_total * weight_sherpa22_njets * ((stxe_trigger) && (n_jet>=4) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>130e3) && (met>300e3) && (amt2<110) && (dphi_met_lep<2.5) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) ) )"
    
    #cut = "( " + lumi + " * weight * xs_weight * sf_total * weight_sherpa22_njets * ((n_jet>=4) && (n_bjet>0) && (met>=100e3) && (mt>=90e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && ( (dphi_b_lep_max<2.5) || (dphi_b_lep_max>2.5 && ((ht>300e3) || (ht<200e3)) ) ) &&!((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80))) )"
    
    #cut = "( " + lumi + " * weight * xs_weight * sf_total * weight_sherpa22_njets * ((met>=250e3) && (mt>=90e3) && (n_lep==1)) )"
    
    ##########Cuts for NN##########
    #cut = '(n_jet>=4) && (n_lep==1) && (n_bjet>=1) && (mt>=90e3) && (met>=100e3) && (jet_pt[0]>=25e3) && (jet_pt[1]>=25e3) && (jet_pt[2]>=25e3) && (jet_pt[3]>=25e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80))'
    
    cut = '(met>=100e3) && (jet_pt[0]>=25e3) && (jet_pt[1]>=25e3) && (jet_pt[2]>=25e3) && (jet_pt[3]>=25e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80))'
        
    sampleNames = []
    
    sampleNames.append('stop_bWN_350_200')
    sampleNames.append('powheg_ttbar')
    sampleNames.append('powheg_singletop')
    sampleNames.append('sherpa22_Wjets')

    #Signal=['stop_bWN_250_100','stop_bWN_300_150','stop_bWN_350_200','stop_bWN_400_250','stop_bWN_450_300','stop_bWN_500_350','stop_bWN_550_400','stop_bWN_600_450','stop_bWN_650_500','stop_bWN_250_130','stop_bWN_300_180','stop_bWN_350_230','stop_bWN_400_280','stop_bWN_450_330','stop_bWN_500_380','stop_bWN_550_430','stop_bWN_600_480','stop_bWN_650_530']

    #sampleNames.extend(Signal)
        
    for sampleName in sampleNames:
    
        fileName = datetime.now().strftime('%Y-%m-%d_%H-%M_') + "nominal_"+sampleName
        #fileName = datetime.now().strftime('%Y-%m-%d_%H-%M_') + "debugging_"+sampleName
        
        #allVariables = []
        
        #amt2 = {'name':'am_{T2} [GeV]', 'strVar':'amt2', 'filename':'amt2'}
        #ht = {'name':'h_{T} [GeV]', 'strVar':'ht*0.001', 'filename':'hT'}
        #met = {'name':'E_{T}^{miss} [GeV]', 'strVar':'met*0.001', 'filename':'met'}
        #njet = {'name':'N jets', 'strVar':'n_jet', 'filename':'n_jet'}
        #nbjet = {'name':'N bjets', 'strVar':'n_bjet', 'filename':'n_bjet'}
        #dphimetlep = {'name':'#Delta#phi(l, E_{T}^{miss})', 'strVar':'dphi_met_lep', 'filename':'dphi_met_lep'}
        #Q = {'name':'Q', 'strVar':'1-mt*mt/(2*met*lep_pt[0])', 'filename':'Q'}
        #dphijet0ptmiss = {'name':'#Delta#phi(jet0, p_{T}^{miss})', 'strVar':'dphi_jet0_ptmiss', 'filename':'dphi_jet0_ptmiss'}
        #dphijet1ptmiss = {'name':'#Delta#phi(jet1, p_{T}^{miss})', 'strVar':'dphi_jet1_ptmiss', 'filename':'dphi_jet1_ptmiss'}
        #mbl = {'name':'m_{b,l} [GeV]', 'strVar':'m_bl*0.001', 'filename':'m_bl'}
        #mt = {'name':'m_{T} [GeV]', 'strVar':'mt*0.001', 'filename':'mT'}
        
        #allVariables.append(amt2)
        #allVariables.append(ht)
        #allVariables.append(met)
        #allVariables.append(njet)
        #allVariables.append(nbjet)
        #allVariables.append(dphimetlep)
        #allVariables.append(Q)
        #allVariables.append(dphijet0ptmiss)
        #allVariables.append(dphijet1ptmiss)
        #allVariables.append(mbl)
        #allVariables.append(mt)
        
        allVariables = []

        amt2 = {'name':'myAmt2', "fileName":"amt2", 'varStr':"amt2", 'Xtitle':'am_{T2} [GeV]', 'Ytitle':'Events', 'binning':[30,0,600], "binningIsExplicit":False}
        met = {'name':'myMET', "fileName":"met", 'varStr':"(met*0.001)", 'Xtitle':'E_{T}^{miss} [GeV]', 'Ytitle':'Events', 'binning':[30,0,600], "binningIsExplicit":False}
        dphimetlep = {'name':'mydPhi', "fileName":"dphi_met_lep", 'varStr':"dphi_met_lep", 'Xtitle':'#Delta#phi(l, E_{T}^{miss})', 'Ytitle':'Events', 'binning':[40,0,3.2], "binningIsExplicit":False}
        mt = {'name':'myMT',"fileName":"mt", 'varStr':"mt*0.001", 'Xtitle':'m_{T} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], "binningIsExplicit":False}
        Q = {'name':'myQ',"fileName":"Q", 'varStr':"1-mt*mt/(2*met*lep_pt[0])", 'Xtitle':'Q', 'Ytitle':'Events', 'binning':[30,-1,1], "binningIsExplicit":False}
        njet = {'name':'mynjet',"fileName":"njet", 'varStr':"n_jet", 'Xtitle':'N jets', 'Ytitle':'Events', 'binning':[10,0,10], "binningIsExplicit":False}
        nbjet = {'name':'mynbjet',"fileName":"nbjet", 'varStr':"n_bjet", 'Xtitle':'N bjets', 'Ytitle':'Events', 'binning':[10,0,10], "binningIsExplicit":False}
        jetpt = {'name':'myjetpT',"fileName":"jetpT", 'varStr':"jet_pt*0.001", 'Xtitle':'p_{T}^{jet} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], "binningIsExplicit":False}
        ht = {'name':'myht',"fileName":"hT", 'varStr':"ht*0.001", 'Xtitle':'h_{T} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], "binningIsExplicit":False}
        dphi_jet0_ptmiss = {'name':'mydPhi_jet0ptmiss', "fileName":"dphi_jet0_ptmiss", 'varStr':"dphi_jet0_ptmiss", 'Xtitle':'#Delta#phi(jet0, p_{T}^{miss})', 'Ytitle':'Events', 'binning':[40,0,3.2], "binningIsExplicit":False}
        dphi_jet1_ptmiss = {'name':'mydPhi_jet1ptmiss', "fileName":"dphi_jet1_ptmiss", 'varStr':"dphi_jet1_ptmiss", 'Xtitle':'#Delta#phi(jet1, p_{T}^{miss})', 'Ytitle':'Events', 'binning':[40,0,3.2], "binningIsExplicit":False}
        #amm = {'name':'myamm',"fileName":"amm", 'varStr':"(met*0.001)*(lep_pt[0]*0.001)", 'Xtitle':'amm', 'Ytitle':'Events', 'binning':[30,0,500], "binningIsExplicit":False}
        leppt0 = {'name':'myleppt0',"fileName":"lep_pt0", 'varStr':"lep_pt[0]*0.001", 'Xtitle':'p_{T}^{lep} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], "binningIsExplicit":False}
        mbl = {'name':'mymbl',"fileName":"m_bl", 'varStr':"m_bl*0.001", 'Xtitle':'m_{b,l} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], "binningIsExplicit":False}
        lep_phi = {'name':'mylphi', "fileName":"lep_phi", 'varStr':"lep_phi", 'Xtitle':'#phi(l)', 'Ytitle':'Events', 'binning':[40,0,3.2], "binningIsExplicit":False}
        lep_eta = {'name':'mydPhi', "fileName":"lep_eta", 'varStr':"lep_eta", 'Xtitle':'#eta(l)', 'Ytitle':'Events', 'binning':[40,0,3.2], "binningIsExplicit":False}
        R = {'name':'myR', "fileName":"R", 'varStr':"lep_phi*lep_phi+lep_eta*lep_eta", 'Xtitle':'R', 'Ytitle':'Events', 'binning':[40,0,3.2], "binningIsExplicit":False}
        jetpt0 = {'name':'myjetpT0',"fileName":"jetpT0", 'varStr':"jet_pt[0]*0.001", 'Xtitle':'p_{T}^{jet0} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], "binningIsExplicit":False}
        jetpt1 = {'name':'myjetpT1',"fileName":"jetpT1", 'varStr':"jet_pt[1]*0.001", 'Xtitle':'p_{T}^{jet1} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], "binningIsExplicit":False}
        jetpt2 = {'name':'myjetpT2',"fileName":"jetpT2", 'varStr':"jet_pt[2]*0.001", 'Xtitle':'p_{T}^{jet2} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], "binningIsExplicit":False}
        jetpt3 = {'name':'myjetpT3',"fileName":"jetpT3", 'varStr':"jet_pt[3]*0.001", 'Xtitle':'p_{T}^{jet3} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], "binningIsExplicit":False}
        metsig = {'name':'myMET_sig', "fileName":"met_sig", 'varStr':"met_sig", 'Xtitle':'E_{T}^{miss}-sig', 'Ytitle':'Events', 'binning':[30,0,50], "binningIsExplicit":False}
        htsig ={'name':'myhT_sig', "fileName":"hT_sig", 'varStr':"ht_sig", 'Xtitle':'h_{T}-sig', 'Ytitle':'Events', 'binning':[30,0,50], "binningIsExplicit":False}
        dphi_b_lep_max = {'name':'mydPhi_blepmax', "fileName":"dphi_b_lep_max", 'varStr':"dphi_b_lep_max", 'Xtitle':'max(#Delta#phi(b, l))', 'Ytitle':'Events', 'binning':[40,0,3.2], "binningIsExplicit":False}
        dphi_b_ptmiss_max = {'name':'mydPhi_bptmissmax', "fileName":"dphi_b_ptmiss_max", 'varStr':"dphi_b_ptmiss_max", 'Xtitle':'max(#Delta#phi(b, p_{T}^{miss}))', 'Ytitle':'Events', 'binning':[40,0,3.2], "binningIsExplicit":False}
        metprojlep = {'name':'myMETprojLEP', "fileName":"met_proj_lep", 'varStr':"met_proj_lep*0.001", 'Xtitle':'E_{T,l}^{miss} [GeV]', 'Ytitle':'Events', 'binning':[30,0,600], "binningIsExplicit":False}
        dRbjetlep = {'name':'mydRbjetlep', "fileName":"dr_bjet_lep", 'varStr':"dr_bjet_lep", 'Xtitle':'#DeltaR(b,l)', 'Ytitle':'Events', 'binning':[40,0,3.2], "binningIsExplicit":False}
        bjetpt = {'name':'myBjetpT',"fileName":"bjet_pt", 'varStr':"bjet_pt*0.001", 'Xtitle':'p_{T}^{bjet} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], "binningIsExplicit":False}
        bjetpt0 = {'name':'myBjetpT0',"fileName":"bjet_pt0", 'varStr':"bjet_pt[0]*0.001", 'Xtitle':'p_{T}^{bjet0} [GeV]', 'Ytitle':'Events', 'binning':[30,0,500], "binningIsExplicit":False}
        mTblMET = {'name':'myMtblMet',"fileName":"mT_blMET", 'varStr':"mT_blMET*0.001", 'Xtitle':'m_{T}^{blMET} [GeV]', 'Ytitle':'Events', 'binning':[50,100,700], "binningIsExplicit":False}


        #allVariables.append(met)
        #allVariables.append(dphimetlep)
        #allVariables.append(amt2)
        #allVariables.append(mt)
        #allVariables.append(Q)
        allVariables.append(njet)
        allVariables.append(nbjet)
        #allVariables.append(jetpt)
        #allVariables.append(ht)
        #allVariables.append(dphi_jet0_ptmiss)
        #allVariables.append(dphi_jet1_ptmiss)
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
        
        #names = ["am_{T2}", 'h_{T}', 'E_{T}^{miss}', 'N jets', 'N bjets', '#Delta#phi(l, E_{T}^{miss})', 'Q', '#Delta#phi(jet0, p_{T}^{miss})', '#Delta#phi(jet1, p_{T}^{miss})','m_{b,l}','m_{T}']
        #variables = ['amt2','ht*0.001','met*0.001','n_jet','n_bjet','#Delta#phi(l, E_{T}^{miss})', '1-mt*mt/(2*met*lep_pt[0])', 'dphi_jet0_ptmiss', 'dphi_jet1_ptmiss','m_bl*0.001','mt*0.001']
        #filenames = ['amT2', 'hT', 'met', 'n_jet', 'n_bjet', 'dphi_met_lep', 'Q', 'dphi_jet0_ptmiss', 'dphi_jet1_ptmiss','m_bl', 'mT']
    
        countdiagrams = len(allVariables)*(len(allVariables)-1)/2
        nod = countdiagrams
    
        print 'Using cut: ' + cut
        
        
        #print 'Plotting ' + str(countdiagrams) + ' diagrams...'
    
        #for i in range(0,len(allVariables)):
            #for j in range(0, len(allVariables)):
                #if (i>j):
                    #plot(allVariables[i]['varStr'],allVariables[j]['varStr'],sampleName,allVariables[j]['Xtitle'],allVariables[i]['Xtitle'],cut, fileName +'_'+allVariables[i]['fileName']+'vs'+allVariables[j]['fileName'],allVariables[i]['binning'],allVariables[j]['binning'])
                    #countdiagrams -= 1
                    #print str(countdiagrams) +'/'+ str(nod) + ' diagrams remaining to plot...'
                    
                    
        #-------------Plot one variable to the rest of the list-----------
        
        variab=mt  #Variable to plot
        
        print 'Plotting ' + str(len(allVariables)-1) + ' diagrams...'
        for var in allVariables:
            if var['name'] != variab['name']:
                plot(variab['varStr'],var['varStr'],sampleName,var['Xtitle'],variab['Xtitle'],cut, fileName +'_'+variab['fileName']+'vs'+var['fileName'],variab['binning'],var['binning'])
                
        filepath = './plots/2D/' + fileName + '_infofile.txt'
    
        print 'Saving infofile to' + filepath
        infofile = open(filepath, 'w')
        infofile.write('Applied cuts: ' + cut)
        infofile.close()

if __name__ == "__main__":
    main()
    
