import ROOT
import math
import os, sys

from datetime import datetime
from AtlasStyle import *

def plot(var1, var2, sampleName, xtitle, ytitle, cut, fileName):
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
    
    xbins=30
    xstart=0
    xstop=600
    ybins=30
    ystart=0
    ystop=600
    
    if var1 in ('n_jet','n_bjet'):
        xbins=12
        xstart=0
        xstop=12
    
    if var2 in ('n_jet','n_bjet'):
        ybins=12
        ystart=0
        ystop=12
    
    if var1 in ('dphi_jet0_ptmiss','dphi_jet1_ptmiss','dphi_met_lep'):
        xbins=40
        xstart=0
        xstop=3.2
        
    if var2 in ('dphi_jet0_ptmiss','dphi_jet1_ptmiss','dphi_met_lep'):
        ybins=40
        ystart=0
        ystop=3.2
        
    if (var1=='1-mt*mt/(2*met*lep_pt[0])'):
        xbins=40
        xstart=-1
        xstop=1
        
    if (var2=='1-mt*mt/(2*met*lep_pt[0])'):
        ybins=40
        ystart=-1
        ystop=-1

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
    
    cut = "( " + lumi + " * weight * xs_weight * sf_total * weight_sherpa22_njets * ((n_jet>=4) && (jet_pt[0]>25e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>90e3) && (met>100e3) && (dphi_met_lep<2.5) && (n_bjet>0) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) ) )"
    
    sampleName = 'stop_bWN_300_150'
    fileName = datetime.now().strftime('%Y-%m-%d_%H-%M_') + "nominal_"+sampleName
    
    variables = ['amt2','ht*0.001','met*0.001','n_jet','n_bjet','dphi_met_lep', '1-mt*mt/(2*met*lep_pt[0])', 'dphi_jet0_ptmiss', 'dphi_jet1_ptmiss']
    names = ["am_{T2}", 'h_{T}', 'E_{T}^{miss}', 'N jets', 'N bjets', '#Delta#phi(l, E_{T}^{miss})', 'Q', '#Delta#phi(jet0, p_{T}^{miss})', '#Delta#phi(jet1, p_{T}^{miss})']
    filenames = ['amT2', 'hT', 'met', 'n_jet', 'n_bjet', 'dphi_met_lep', 'Q', 'dphi_jet0_ptmiss', 'dphi_jet1_ptmiss']
    
    for i in range(0,len(variables)):
        for j in range(0, len(variables)):
            if (i>j):
                plot(variables[i],variables[j],sampleName,names[j],names[i],cut, fileName +'_'+filenames[i]+'vs'+filenames[j])
                
    filepath = './plots/2D/' + fileName + '_infofile.txt'
    
    print 'Saving infofile to' + filepath
    infofile = open(filepath, 'w')
    infofile.write('Applied cuts: ' + cut)
    infofile.close()

if __name__ == "__main__":
    main()
    
