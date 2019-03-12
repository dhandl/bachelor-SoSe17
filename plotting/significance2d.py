import ROOT
import math
import os, sys

from AtlasStyle import *
import PlotStyle as PS
ROOT.gStyle.SetPalette(57)

from hfUtils import *
from funcs import  getYieldFromChain


def asimovZ(s, b, b_err, syst=False):
  tot = s + b
  b2 = b*b
  if syst:
    b_err2 = math.sqrt( b_err*b_err + (b*0.25)*(b*0.25) )
  else:
    b_err2 = b_err * b_err
  b_plus_err2 = b + b_err2
  Z = math.sqrt(2 * ((tot)*math.log(tot * b_plus_err2 / (b2 + tot * b_err2)) - b2 / b_err2 * math.log(1 + b_err2 * s / (b * b_plus_err2))))
  return Z

def main():

    plotSig = True 
    filename = "SR_RNN0p86-1p0"
    if plotSig:
      filename = filename+"_Significance"
    else:
      filename = filename+"_signal_contamination"

    wwwDir = "/project/etp5/dhandl/plots/Stop1L/FullRun2/SignifcanceScan/21.2.60/"
    if not os.path.exists(wwwDir):
        os.makedirs(wwwDir)
        print ('Creating Directory...')

    bkgDir = '/project/etp3/dhandl/samples/SUSY/Stop1L/21.2.60_ML/'
    #sigDir = '/project/etp5/dhandl/myFork-stop1l/export/default/'
    sigDir = bkgDir
     
    lumi = str(140500.)
    
    cut = '(n_jet>=4) && (n_lep==1) && (lep_pt[0]>25e3) && (n_bjet>=1) && (mt>=110e3) && (met>=230e3) && (jet_pt[0]>=25e3) && (jet_pt[1]>=25e3) && (jet_pt[2]>=25e3) && (jet_pt[3]>=25e3) && (dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (outputScore_RNN >= 0.86) && (outputScore_RNN<1.0)'

    weight = 'weight * xs_weight * lumi_weight * sf_total'

    sampleNames = [
    {'name':'ttbar', 'target':[bkgDir+'mc16a_ttbar/*.root',bkgDir+'mc16d_ttbar/*.root',bkgDir+'mc16e_ttbar/*.root'], 'chain_name':'ttbar_Nom', 'class':'bkg'},
    {'name':'singletop', 'target':[bkgDir+'mc16a_singletop/*.root', bkgDir+'mc16d_singletop/*.root', bkgDir+'mc16e_singletop/*.root'], 'chain_name':'singletop_Nom', 'class':'bkg'}, 
    {'name':'wjets', 'target':[bkgDir+'mc16a_wjets/*.root', bkgDir+'mc16d_wjets/*.root', bkgDir+'mc16e_wjets/*.root'], 'chain_name':'wjets_Nom', 'class':'bkg'},
    {'name':'ttV', 'target':[bkgDir+'mc16a_ttV/*.root', bkgDir+'mc16d_ttV/*.root', bkgDir+'mc16e_ttV/*.root'], 'chain_name':'ttV_Nom', 'class':'bkg'},
    {'name':'multiboson', 'target':[bkgDir+'mc16a_multiboson/*.root',bkgDir+'mc16d_multiboson/*.root',bkgDir+'mc16e_multiboson/*.root'], 'chain_name':'multiboson_Nom', 'class':'bkg'},

    ### bWN ###

    {'name':'bWN_400_235', 'target':[bkgDir+'mc16a_bWN_400_235/*.root',bkgDir+'mc16d_bWN_400_235/*.root',bkgDir+'mc16e_bWN_400_235/*.root'], 'chain_name':'bWN_400_235_Nom', 'class':'sig'},
    {'name':'bWN_400_250', 'target':[bkgDir+'mc16a_bWN_400_250/*.root',bkgDir+'mc16d_bWN_400_250/*.root',bkgDir+'mc16e_bWN_400_250/*.root'], 'chain_name':'bWN_400_250_Nom', 'class':'sig'},
    {'name':'bWN_400_280', 'target':[bkgDir+'mc16a_bWN_400_280/*.root',bkgDir+'mc16d_bWN_400_280/*.root',bkgDir+'mc16e_bWN_400_280/*.root'], 'chain_name':'bWN_400_280_Nom', 'class':'sig'},
    {'name':'bWN_400_310', 'target':[bkgDir+'mc16a_bWN_400_310/*.root',bkgDir+'mc16d_bWN_400_310/*.root',bkgDir+'mc16e_bWN_400_310/*.root'], 'chain_name':'bWN_400_310_Nom', 'class':'sig'},
    {'name':'bWN_450_285', 'target':[bkgDir+'mc16a_bWN_450_285/*.root',bkgDir+'mc16d_bWN_450_285/*.root',bkgDir+'mc16e_bWN_450_285/*.root'], 'chain_name':'bWN_450_285_Nom', 'class':'sig'},
    {'name':'bWN_450_300', 'target':[bkgDir+'mc16a_bWN_450_300/*.root',bkgDir+'mc16d_bWN_450_300/*.root',bkgDir+'mc16e_bWN_450_300/*.root'], 'chain_name':'bWN_450_300_Nom', 'class':'sig'},
    {'name':'bWN_450_330', 'target':[bkgDir+'mc16a_bWN_450_330/*.root',bkgDir+'mc16d_bWN_450_330/*.root',bkgDir+'mc16e_bWN_450_330/*.root'], 'chain_name':'bWN_450_330_Nom', 'class':'sig'},
    {'name':'bWN_450_360', 'target':[bkgDir+'mc16a_bWN_450_360/*.root',bkgDir+'mc16d_bWN_450_360/*.root',bkgDir+'mc16e_bWN_450_360/*.root'], 'chain_name':'bWN_450_360_Nom', 'class':'sig'},
    {'name':'bWN_500_335', 'target':[bkgDir+'mc16a_bWN_500_335/*.root',bkgDir+'mc16d_bWN_500_335/*.root',bkgDir+'mc16e_bWN_500_335/*.root'], 'chain_name':'bWN_500_335_Nom', 'class':'sig'},
    {'name':'bWN_500_350', 'target':[bkgDir+'mc16a_bWN_500_350/*.root',bkgDir+'mc16d_bWN_500_350/*.root',bkgDir+'mc16e_bWN_500_350/*.root'], 'chain_name':'bWN_500_350_Nom', 'class':'sig'},
    {'name':'bWN_500_380', 'target':[bkgDir+'mc16a_bWN_500_380/*.root',bkgDir+'mc16d_bWN_500_380/*.root',bkgDir+'mc16e_bWN_500_380/*.root'], 'chain_name':'bWN_500_380_Nom', 'class':'sig'},
    {'name':'bWN_500_410', 'target':[bkgDir+'mc16a_bWN_500_410/*.root',bkgDir+'mc16d_bWN_500_410/*.root',bkgDir+'mc16e_bWN_500_410/*.root'], 'chain_name':'bWN_500_410_Nom', 'class':'sig'},
    {'name':'bWN_550_385', 'target':[bkgDir+'mc16a_bWN_550_385/*.root',bkgDir+'mc16d_bWN_550_385/*.root',bkgDir+'mc16e_bWN_550_385/*.root'], 'chain_name':'bWN_550_385_Nom', 'class':'sig'},
    {'name':'bWN_550_400', 'target':[bkgDir+'mc16a_bWN_550_400/*.root',bkgDir+'mc16d_bWN_550_400/*.root',bkgDir+'mc16e_bWN_550_400/*.root'], 'chain_name':'bWN_550_400_Nom', 'class':'sig'},
    {'name':'bWN_550_430', 'target':[bkgDir+'mc16a_bWN_550_430/*.root',bkgDir+'mc16d_bWN_550_430/*.root',bkgDir+'mc16e_bWN_550_430/*.root'], 'chain_name':'bWN_550_430_Nom', 'class':'sig'},
    {'name':'bWN_550_460', 'target':[bkgDir+'mc16a_bWN_550_460/*.root',bkgDir+'mc16d_bWN_550_460/*.root',bkgDir+'mc16e_bWN_550_460/*.root'], 'chain_name':'bWN_550_460_Nom', 'class':'sig'},
    {'name':'bWN_600_435', 'target':[bkgDir+'mc16a_bWN_600_435/*.root',bkgDir+'mc16d_bWN_600_435/*.root',bkgDir+'mc16e_bWN_600_435/*.root'], 'chain_name':'bWN_600_435_Nom', 'class':'sig'},
    {'name':'bWN_600_450', 'target':[bkgDir+'mc16a_bWN_600_450/*.root',bkgDir+'mc16d_bWN_600_450/*.root',bkgDir+'mc16e_bWN_600_450/*.root'], 'chain_name':'bWN_600_450_Nom', 'class':'sig'},
    {'name':'bWN_600_480', 'target':[bkgDir+'mc16a_bWN_600_480/*.root',bkgDir+'mc16d_bWN_600_480/*.root',bkgDir+'mc16e_bWN_600_480/*.root'], 'chain_name':'bWN_600_480_Nom', 'class':'sig'},
    {'name':'bWN_600_510', 'target':[bkgDir+'mc16a_bWN_600_510/*.root',bkgDir+'mc16d_bWN_600_510/*.root',bkgDir+'mc16e_bWN_600_510/*.root'], 'chain_name':'bWN_600_510_Nom', 'class':'sig'},
    {'name':'bWN_650_485', 'target':[bkgDir+'mc16a_bWN_650_485/*.root',bkgDir+'mc16d_bWN_650_485/*.root',bkgDir+'mc16e_bWN_650_485/*.root'], 'chain_name':'bWN_650_485_Nom', 'class':'sig'},
    {'name':'bWN_650_500', 'target':[bkgDir+'mc16a_bWN_650_500/*.root',bkgDir+'mc16d_bWN_650_500/*.root',bkgDir+'mc16e_bWN_650_500/*.root'], 'chain_name':'bWN_650_500_Nom', 'class':'sig'},
    {'name':'bWN_650_530', 'target':[bkgDir+'mc16a_bWN_650_530/*.root',bkgDir+'mc16d_bWN_650_530/*.root',bkgDir+'mc16e_bWN_650_530/*.root'], 'chain_name':'bWN_650_530_Nom', 'class':'sig'},
    {'name':'bWN_650_560', 'target':[bkgDir+'mc16a_bWN_650_560/*.root',bkgDir+'mc16d_bWN_650_560/*.root',bkgDir+'mc16e_bWN_650_560/*.root'], 'chain_name':'bWN_650_560_Nom', 'class':'sig'},
    {'name':'bWN_700_535', 'target':[bkgDir+'mc16a_bWN_700_535/*.root',bkgDir+'mc16d_bWN_700_535/*.root',bkgDir+'mc16e_bWN_700_535/*.root'], 'chain_name':'bWN_700_535_Nom', 'class':'sig'},
    {'name':'bWN_700_550', 'target':[bkgDir+'mc16a_bWN_700_550/*.root',bkgDir+'mc16d_bWN_700_550/*.root',bkgDir+'mc16e_bWN_700_550/*.root'], 'chain_name':'bWN_700_550_Nom', 'class':'sig'},
    {'name':'bWN_700_580', 'target':[bkgDir+'mc16a_bWN_700_580/*.root',bkgDir+'mc16d_bWN_700_580/*.root',bkgDir+'mc16e_bWN_700_580/*.root'], 'chain_name':'bWN_700_580_Nom', 'class':'sig'},
    {'name':'bWN_700_610', 'target':[bkgDir+'mc16a_bWN_700_610/*.root',bkgDir+'mc16d_bWN_700_610/*.root',bkgDir+'mc16e_bWN_700_610/*.root'], 'chain_name':'bWN_700_610_Nom', 'class':'sig'},
    {'name':'bWN_750_585', 'target':[bkgDir+'mc16a_bWN_750_585/*.root',bkgDir+'mc16d_bWN_750_585/*.root',bkgDir+'mc16e_bWN_750_585/*.root'], 'chain_name':'bWN_750_585_Nom', 'class':'sig'},
    {'name':'bWN_750_600', 'target':[bkgDir+'mc16a_bWN_750_600/*.root',bkgDir+'mc16d_bWN_750_600/*.root',bkgDir+'mc16e_bWN_750_600/*.root'], 'chain_name':'bWN_750_600_Nom', 'class':'sig'},
    {'name':'bWN_750_630', 'target':[bkgDir+'mc16a_bWN_750_630/*.root',bkgDir+'mc16d_bWN_750_630/*.root',bkgDir+'mc16e_bWN_750_630/*.root'], 'chain_name':'bWN_750_630_Nom', 'class':'sig'},
    {'name':'bWN_750_660', 'target':[bkgDir+'mc16a_bWN_750_660/*.root',bkgDir+'mc16d_bWN_750_660/*.root',bkgDir+'mc16e_bWN_750_660/*.root'], 'chain_name':'bWN_750_660_Nom', 'class':'sig'},

    ### bffN ###
    {'name':'bffN_300_220', 'target':[bkgDir+'mc16a_bffN_300_220/*.root',bkgDir+'mc16d_bffN_300_220/*.root',bkgDir+'mc16e_bffN_300_220/*.root'], 'chain_name':'bffN_300_220_Nom', 'class':'sig'},
    {'name':'bffN_300_250', 'target':[bkgDir+'mc16a_bffN_300_250/*.root',bkgDir+'mc16d_bffN_300_250/*.root',bkgDir+'mc16e_bffN_300_250/*.root'], 'chain_name':'bffN_300_250_Nom', 'class':'sig'},
    {'name':'bffN_300_280', 'target':[bkgDir+'mc16a_bffN_300_280/*.root',bkgDir+'mc16d_bffN_300_280/*.root',bkgDir+'mc16e_bffN_300_280/*.root'], 'chain_name':'bffN_300_280_Nom', 'class':'sig'},
    {'name':'bffN_300_293', 'target':[bkgDir+'mc16a_bffN_300_293/*.root',bkgDir+'mc16d_bffN_300_293/*.root',bkgDir+'mc16e_bffN_300_293/*.root'], 'chain_name':'bffN_300_293_Nom', 'class':'sig'},
                                                                                                                                            
    {'name':'bffN_350_270', 'target':[bkgDir+'mc16a_bffN_350_270/*.root',bkgDir+'mc16d_bffN_350_270/*.root',bkgDir+'mc16e_bffN_350_270/*.root'], 'chain_name':'bffN_350_270_Nom', 'class':'sig'},
    {'name':'bffN_350_300', 'target':[bkgDir+'mc16a_bffN_350_300/*.root',bkgDir+'mc16d_bffN_350_300/*.root',bkgDir+'mc16e_bffN_350_300/*.root'], 'chain_name':'bffN_350_300_Nom', 'class':'sig'},
    {'name':'bffN_350_330', 'target':[bkgDir+'mc16a_bffN_350_330/*.root',bkgDir+'mc16d_bffN_350_330/*.root',bkgDir+'mc16e_bffN_350_330/*.root'], 'chain_name':'bffN_350_330_Nom', 'class':'sig'},
    {'name':'bffN_350_243', 'target':[bkgDir+'mc16a_bffN_350_243/*.root',bkgDir+'mc16d_bffN_350_243/*.root',bkgDir+'mc16e_bffN_350_243/*.root'], 'chain_name':'bffN_350_243_Nom', 'class':'sig'},
                                                                                                                                            
    {'name':'bffN_400_320', 'target':[bkgDir+'mc16a_bffN_400_320/*.root',bkgDir+'mc16d_bffN_400_320/*.root',bkgDir+'mc16e_bffN_400_320/*.root'], 'chain_name':'bffN_400_320_Nom', 'class':'sig'},
    {'name':'bffN_400_350', 'target':[bkgDir+'mc16a_bffN_400_350/*.root',bkgDir+'mc16d_bffN_400_350/*.root',bkgDir+'mc16e_bffN_400_350/*.root'], 'chain_name':'bffN_400_350_Nom', 'class':'sig'},
    {'name':'bffN_400_380', 'target':[bkgDir+'mc16a_bffN_400_380/*.root',bkgDir+'mc16d_bffN_400_380/*.root',bkgDir+'mc16e_bffN_400_380/*.root'], 'chain_name':'bffN_400_380_Nom', 'class':'sig'},
    {'name':'bffN_400_393', 'target':[bkgDir+'mc16a_bffN_400_393/*.root',bkgDir+'mc16d_bffN_400_393/*.root',bkgDir+'mc16e_bffN_400_393/*.root'], 'chain_name':'bffN_400_393_Nom', 'class':'sig'},
                                                                                                                                            
    {'name':'bffN_450_370', 'target':[bkgDir+'mc16a_bffN_450_370/*.root',bkgDir+'mc16d_bffN_450_370/*.root',bkgDir+'mc16e_bffN_450_370/*.root'], 'chain_name':'bffN_450_370_Nom', 'class':'sig'},
    {'name':'bffN_450_400', 'target':[bkgDir+'mc16a_bffN_450_400/*.root',bkgDir+'mc16d_bffN_450_400/*.root',bkgDir+'mc16e_bffN_450_400/*.root'], 'chain_name':'bffN_450_400_Nom', 'class':'sig'},
    {'name':'bffN_450_430', 'target':[bkgDir+'mc16a_bffN_450_430/*.root',bkgDir+'mc16d_bffN_450_430/*.root',bkgDir+'mc16e_bffN_450_430/*.root'], 'chain_name':'bffN_450_430_Nom', 'class':'sig'},
    {'name':'bffN_450_443', 'target':[bkgDir+'mc16a_bffN_450_443/*.root',bkgDir+'mc16d_bffN_450_443/*.root',bkgDir+'mc16e_bffN_450_443/*.root'], 'chain_name':'bffN_450_443_Nom', 'class':'sig'},
                                                                                                                                            
    {'name':'bffN_500_420', 'target':[bkgDir+'mc16a_bffN_500_420/*.root',bkgDir+'mc16d_bffN_500_420/*.root',bkgDir+'mc16e_bffN_500_420/*.root'], 'chain_name':'bffN_500_420_Nom', 'class':'sig'},
    {'name':'bffN_500_450', 'target':[bkgDir+'mc16a_bffN_500_450/*.root',bkgDir+'mc16d_bffN_500_450/*.root',bkgDir+'mc16e_bffN_500_450/*.root'], 'chain_name':'bffN_500_450_Nom', 'class':'sig'},
    {'name':'bffN_500_480', 'target':[bkgDir+'mc16a_bffN_500_480/*.root',bkgDir+'mc16d_bffN_500_480/*.root',bkgDir+'mc16e_bffN_500_480/*.root'], 'chain_name':'bffN_500_480_Nom', 'class':'sig'},
    {'name':'bffN_500_493', 'target':[bkgDir+'mc16a_bffN_500_493/*.root',bkgDir+'mc16d_bffN_500_493/*.root',bkgDir+'mc16e_bffN_500_493/*.root'], 'chain_name':'bffN_500_493_Nom', 'class':'sig'},
                                                                                                                                            
    {'name':'bffN_550_470', 'target':[bkgDir+'mc16a_bffN_550_470/*.root',bkgDir+'mc16d_bffN_550_470/*.root',bkgDir+'mc16e_bffN_550_470/*.root'], 'chain_name':'bffN_550_470_Nom', 'class':'sig'},
    {'name':'bffN_550_500', 'target':[bkgDir+'mc16a_bffN_550_500/*.root',bkgDir+'mc16d_bffN_550_500/*.root',bkgDir+'mc16e_bffN_550_500/*.root'], 'chain_name':'bffN_550_500_Nom', 'class':'sig'},
    {'name':'bffN_550_530', 'target':[bkgDir+'mc16a_bffN_550_530/*.root',bkgDir+'mc16d_bffN_550_530/*.root',bkgDir+'mc16e_bffN_550_530/*.root'], 'chain_name':'bffN_550_530_Nom', 'class':'sig'},
    {'name':'bffN_550_543', 'target':[bkgDir+'mc16a_bffN_550_543/*.root',bkgDir+'mc16d_bffN_550_543/*.root',bkgDir+'mc16e_bffN_550_543/*.root'], 'chain_name':'bffN_550_543_Nom', 'class':'sig'},
                                                                                                                                            
    {'name':'bffN_600_520', 'target':[bkgDir+'mc16a_bffN_600_520/*.root',bkgDir+'mc16d_bffN_600_520/*.root',bkgDir+'mc16e_bffN_600_520/*.root'], 'chain_name':'bffN_600_520_Nom', 'class':'sig'},
    {'name':'bffN_600_550', 'target':[bkgDir+'mc16a_bffN_600_550/*.root',bkgDir+'mc16d_bffN_600_550/*.root',bkgDir+'mc16e_bffN_600_550/*.root'], 'chain_name':'bffN_600_550_Nom', 'class':'sig'},
    {'name':'bffN_600_580', 'target':[bkgDir+'mc16a_bffN_600_580/*.root',bkgDir+'mc16d_bffN_600_580/*.root',bkgDir+'mc16e_bffN_600_580/*.root'], 'chain_name':'bffN_600_580_Nom', 'class':'sig'},
    {'name':'bffN_600_593', 'target':[bkgDir+'mc16a_bffN_600_593/*.root',bkgDir+'mc16d_bffN_600_593/*.root',bkgDir+'mc16e_bffN_600_593/*.root'], 'chain_name':'bffN_600_593_Nom', 'class':'sig'},
                                                                                                                                            
    {'name':'bffN_650_570', 'target':[bkgDir+'mc16a_bffN_650_570/*.root',bkgDir+'mc16d_bffN_650_570/*.root',bkgDir+'mc16e_bffN_650_570/*.root'], 'chain_name':'bffN_650_570_Nom', 'class':'sig'},
    {'name':'bffN_650_600', 'target':[bkgDir+'mc16a_bffN_650_600/*.root',bkgDir+'mc16d_bffN_650_600/*.root',bkgDir+'mc16e_bffN_650_600/*.root'], 'chain_name':'bffN_650_600_Nom', 'class':'sig'},
    {'name':'bffN_650_630', 'target':[bkgDir+'mc16a_bffN_650_630/*.root',bkgDir+'mc16d_bffN_650_630/*.root',bkgDir+'mc16e_bffN_650_630/*.root'], 'chain_name':'bffN_650_630_Nom', 'class':'sig'},
    {'name':'bffN_650_643', 'target':[bkgDir+'mc16a_bffN_650_643/*.root',bkgDir+'mc16d_bffN_650_643/*.root',bkgDir+'mc16e_bffN_650_643/*.root'], 'chain_name':'bffN_650_643_Nom', 'class':'sig'},
    
    ### tN ###

  {'name':'tN_190_17', 'target':[bkgDir+'mc16a_tN_190_17/*.root',bkgDir+'mc16d_tN_190_17/*.root',bkgDir+'mc16e_tN_190_17/*.root'], 'chain_name':'tN_190_17_Nom', 'class':'sig'},
  {'name':'tN_400_200', 'target':[bkgDir+'mc16a_tN_400_200/*.root',bkgDir+'mc16d_tN_400_200/*.root',bkgDir+'mc16e_tN_400_200/*.root'], 'chain_name':'tN_400_200_Nom', 'class':'sig'},
  {'name':'tN_500_300', 'target':[bkgDir+'mc16a_tN_500_300/*.root',bkgDir+'mc16d_tN_500_300/*.root',bkgDir+'mc16e_tN_500_300/*.root'], 'chain_name':'tN_500_300_Nom', 'class':'sig'},
  {'name':'tN_500_312', 'target':[bkgDir+'mc16a_tN_500_312/*.root',bkgDir+'mc16d_tN_500_312/*.root',bkgDir+'mc16e_tN_500_312/*.root'], 'chain_name':'tN_500_312_Nom', 'class':'sig'},
  {'name':'tN_500_327', 'target':[bkgDir+'mc16a_tN_500_327/*.root',bkgDir+'mc16d_tN_500_327/*.root',bkgDir+'mc16e_tN_500_327/*.root'], 'chain_name':'tN_500_327_Nom', 'class':'sig'},
  {'name':'tN_550_350', 'target':[bkgDir+'mc16a_tN_550_350/*.root',bkgDir+'mc16d_tN_550_350/*.root',bkgDir+'mc16e_tN_550_350/*.root'], 'chain_name':'tN_550_350_Nom', 'class':'sig'},
  {'name':'tN_550_362', 'target':[bkgDir+'mc16a_tN_550_362/*.root',bkgDir+'mc16d_tN_550_362/*.root',bkgDir+'mc16e_tN_550_362/*.root'], 'chain_name':'tN_550_362_Nom', 'class':'sig'},
  {'name':'tN_550_377', 'target':[bkgDir+'mc16a_tN_550_377/*.root',bkgDir+'mc16d_tN_550_377/*.root',bkgDir+'mc16e_tN_550_377/*.root'], 'chain_name':'tN_550_377_Nom', 'class':'sig'},
  {'name':'tN_600_400', 'target':[bkgDir+'mc16a_tN_600_400/*.root',bkgDir+'mc16d_tN_600_400/*.root',bkgDir+'mc16e_tN_600_400/*.root'], 'chain_name':'tN_600_400_Nom', 'class':'sig'},
  {'name':'tN_600_412', 'target':[bkgDir+'mc16a_tN_600_412/*.root',bkgDir+'mc16d_tN_600_412/*.root',bkgDir+'mc16e_tN_600_412/*.root'], 'chain_name':'tN_600_412_Nom', 'class':'sig'},
  {'name':'tN_600_427', 'target':[bkgDir+'mc16a_tN_600_427/*.root',bkgDir+'mc16d_tN_600_427/*.root',bkgDir+'mc16e_tN_600_427/*.root'], 'chain_name':'tN_600_427_Nom', 'class':'sig'},
  {'name':'tN_650_450', 'target':[bkgDir+'mc16a_tN_650_450/*.root',bkgDir+'mc16d_tN_650_450/*.root',bkgDir+'mc16e_tN_650_450/*.root'], 'chain_name':'tN_650_450_Nom', 'class':'sig'},
  {'name':'tN_650_462', 'target':[bkgDir+'mc16a_tN_650_462/*.root',bkgDir+'mc16d_tN_650_462/*.root',bkgDir+'mc16e_tN_650_462/*.root'], 'chain_name':'tN_650_462_Nom', 'class':'sig'},
  {'name':'tN_650_477', 'target':[bkgDir+'mc16a_tN_650_477/*.root',bkgDir+'mc16d_tN_650_477/*.root',bkgDir+'mc16e_tN_650_477/*.root'], 'chain_name':'tN_650_477_Nom', 'class':'sig'},
  {'name':'tN_700_500', 'target':[bkgDir+'mc16a_tN_700_500/*.root',bkgDir+'mc16d_tN_700_500/*.root',bkgDir+'mc16e_tN_700_500/*.root'], 'chain_name':'tN_700_500_Nom', 'class':'sig'},

    ]

    harvest = [
    ### bWN ###
    {'mT':400, 'mX':235, 'yield':0, 'var':0},
    {'mT':400, 'mX':250, 'yield':0, 'var':0},
    {'mT':400, 'mX':280, 'yield':0, 'var':0},
    {'mT':400, 'mX':310, 'yield':0, 'var':0},

    {'mT':450, 'mX':285, 'yield':0, 'var':0},
    {'mT':450, 'mX':300, 'yield':0, 'var':0},
    {'mT':450, 'mX':330, 'yield':0, 'var':0},
    {'mT':450, 'mX':360, 'yield':0, 'var':0},

    {'mT':500, 'mX':335, 'yield':0, 'var':0},
    {'mT':500, 'mX':350, 'yield':0, 'var':0},
    {'mT':500, 'mX':380, 'yield':0, 'var':0},
    {'mT':500, 'mX':410, 'yield':0, 'var':0},

    {'mT':550, 'mX':385, 'yield':0, 'var':0},
    {'mT':550, 'mX':400, 'yield':0, 'var':0},
    {'mT':550, 'mX':430, 'yield':0, 'var':0},
    {'mT':550, 'mX':460, 'yield':0, 'var':0},

    {'mT':600, 'mX':435, 'yield':0, 'var':0},
    {'mT':600, 'mX':450, 'yield':0, 'var':0},
    {'mT':600, 'mX':480, 'yield':0, 'var':0},
    {'mT':600, 'mX':510, 'yield':0, 'var':0},

    {'mT':650, 'mX':485, 'yield':0, 'var':0},
    {'mT':650, 'mX':500, 'yield':0, 'var':0},
    {'mT':650, 'mX':530, 'yield':0, 'var':0},
    {'mT':650, 'mX':560, 'yield':0, 'var':0},

    {'mT':700, 'mX':535, 'yield':0, 'var':0},
    {'mT':700, 'mX':550, 'yield':0, 'var':0},
    {'mT':700, 'mX':580, 'yield':0, 'var':0},
    {'mT':700, 'mX':610, 'yield':0, 'var':0},

    {'mT':750, 'mX':585, 'yield':0, 'var':0},
    {'mT':750, 'mX':600, 'yield':0, 'var':0},
    {'mT':750, 'mX':630, 'yield':0, 'var':0},
    {'mT':750, 'mX':660, 'yield':0, 'var':0},

    ### bffN ###
    {'mT':300, 'mX':220, 'yield':0, 'var':0},
    {'mT':300, 'mX':250, 'yield':0, 'var':0},
    {'mT':300, 'mX':280, 'yield':0, 'var':0},
    {'mT':300, 'mX':293, 'yield':0, 'var':0},

    {'mT':350, 'mX':270, 'yield':0, 'var':0},
    {'mT':350, 'mX':300, 'yield':0, 'var':0},
    {'mT':350, 'mX':330, 'yield':0, 'var':0},
    {'mT':350, 'mX':343, 'yield':0, 'var':0},

    {'mT':400, 'mX':320, 'yield':0, 'var':0},
    {'mT':400, 'mX':350, 'yield':0, 'var':0},
    {'mT':400, 'mX':380, 'yield':0, 'var':0},
    {'mT':400, 'mX':393, 'yield':0, 'var':0},

    {'mT':450, 'mX':370, 'yield':0, 'var':0},
    {'mT':450, 'mX':400, 'yield':0, 'var':0},
    {'mT':450, 'mX':430, 'yield':0, 'var':0},
    {'mT':450, 'mX':443, 'yield':0, 'var':0},

    {'mT':500, 'mX':420, 'yield':0, 'var':0},
    {'mT':500, 'mX':450, 'yield':0, 'var':0},
    {'mT':500, 'mX':480, 'yield':0, 'var':0},
    {'mT':500, 'mX':493, 'yield':0, 'var':0},

    {'mT':550, 'mX':470, 'yield':0, 'var':0},
    {'mT':550, 'mX':500, 'yield':0, 'var':0},
    {'mT':550, 'mX':530, 'yield':0, 'var':0},
    {'mT':550, 'mX':543, 'yield':0, 'var':0},

    {'mT':600, 'mX':520, 'yield':0, 'var':0},
    {'mT':600, 'mX':550, 'yield':0, 'var':0},
    {'mT':600, 'mX':580, 'yield':0, 'var':0},
    {'mT':600, 'mX':593, 'yield':0, 'var':0},

    {'mT':650, 'mX':570, 'yield':0, 'var':0},
    {'mT':650, 'mX':600, 'yield':0, 'var':0},
    {'mT':650, 'mX':630, 'yield':0, 'var':0},
    {'mT':650, 'mX':643, 'yield':0, 'var':0},

    ### tN ###
    {'mT':190, 'mX':17, 'yield':0, 'var':0},
    {'mT':400, 'mX':200, 'yield':0, 'var':0},
    {'mT':500, 'mX':300, 'yield':0, 'var':0},
    {'mT':500, 'mX':312, 'yield':0, 'var':0},
    {'mT':500, 'mX':327, 'yield':0, 'var':0},
    {'mT':550, 'mX':350, 'yield':0, 'var':0},
    {'mT':550, 'mX':362, 'yield':0, 'var':0},
    {'mT':550, 'mX':377, 'yield':0, 'var':0},
    {'mT':600, 'mX':400, 'yield':0, 'var':0},
    {'mT':600, 'mX':412, 'yield':0, 'var':0},
    {'mT':600, 'mX':427, 'yield':0, 'var':0},
    {'mT':650, 'mX':450, 'yield':0, 'var':0},
    {'mT':650, 'mX':462, 'yield':0, 'var':0},
    {'mT':650, 'mX':477, 'yield':0, 'var':0},
    {'mT':700, 'mX':500, 'yield':0, 'var':0},
    ]

    for i, sample in enumerate(sampleNames):
        sample['chain'] = ROOT.TChain(sample['chain_name'])
        for target in sample['target']:
          sample['chain'].Add(target)
 
    totBkg = 0
    totBkgVar = 0

    for sample in sampleNames:
      sample['yield'], sample['error'] = getYieldFromChain(sample['chain'], cut, lumi, weight=weight, returnError=True)

      if sample['class'] == 'bkg':
        totBkg += sample['yield']
        totBkgVar += sample['error']**2
         
      elif sample['class'] == 'sig':
        for point in harvest:
          if (str(point['mT']) in sample['name']) and (str(point['mX']) in sample['name']):
            point['yield'] += sample['yield']
            point['var'] += sample['error']**2
    
    print totBkg, totBkgVar 
    relBkg = math.sqrt(totBkgVar/(totBkg**2) + 0.25*0.25) 

    xs = []
    ys = []
    zs = []

    for point in harvest:
      print "Signal point: mT {}, mX {}".format(point['mT'],point['mX'])
      point['Z'] = ROOT.RooStats.NumberCountingUtils.BinomialExpZ(point['yield'], totBkg, relBkg)
      if point['Z'] <0.:
        point['Z'] = 0.
      try: 
        point['A'] = asimovZ(point['yield'], totBkg, math.sqrt(totBkgVar), syst=True)
      except ValueError:
        point['A'] = 0.
      point['C'] = point['yield'] / (point['yield'] + totBkg)
      xs.append(point['mT'])
      ys.append(point['mX'])

      if plotSig:
        zs.append(point['Z'])
      else:
        zs.append(point['C'])

    print("X"*50)
    print(len(xs))
    for x in xs:
        print("{:.5f},".format(x))
    print("Y"*50)
    print(len(ys))
    for y in ys:
        print("{:.5f},".format(y))
    print("Z"*50)
    print(len(zs))
    for z in zs:
        print("{:.5f},".format(z))

    if plotSig:
      sig = triwsmooth(harvest, 'A', 'mT', 'mX', transformation=None, smooth=True, npx=100, npy=100)
      fixedhist = FixAndSetBorders(sig, "significance", "significance") 
      contours = getContours(fixedhist, 3.)
    else:
      sig = triwsmooth(harvest, 'C', 'mT', 'mX', transformation=None, smooth=True, npx=100, npy=100)
      fixedhist = FixAndSetBorders(sig, "signal_contamination", "signal_contamination") 
      contours = getContours(fixedhist, .05)
      #contours = getContours(fixedhist, .10)

    c = ROOT.TCanvas()
    c.SetRightMargin(0.15)
    leg = ROOT.TLegend(0.18, PS.ThirdLine-0.12, 0.4, PS.ThirdLine-0.03)
    PS.legend(leg)
    fixedhist.GetXaxis().SetTitle("m_{#tilde{t}} [GeV]") 
    fixedhist.GetYaxis().SetTitle("m_{#tilde{#chi}} [GeV]") 

    #if plotSig:
    #  numbers = drawNumbers(harvest, "Z", x, y)
    #else:
    #  numbers = drawNumbers(harvest, "C", x, y)
    fixedhist.Draw("colz")

    #for contour in contours + contours2:
    for contour in contours:
        contour.SetLineStyle(1)
        contour.SetLineColor(ROOT.kBlack)
        contour.Draw("l same")
    if plotSig:
      leg.AddEntry(contours[0], '3 #sigma' ,'l')
    else:
      leg.AddEntry(contours[0], '5% sig. cont.', 'l')

    #if plotSig:
    #  numbers = drawNumbers(exampleHarvest, "Z", x, y)
    #else:
    #  numbers = drawNumbers(exampleHarvest, "Z", x, y)

    leg.Draw()
    PS.atlas('Work in progress')
    PS.sqrts_lumi(13, 140.5, x=0.18)
    PS.string(x=0.18, y=PS.ThirdLine, text="Simulation")

    c.SaveAs(wwwDir+filename+".pdf")
    c.SaveAs(wwwDir+filename+".png")
    c.SaveAs(wwwDir+filename+".root")

           
if __name__ == "__main__":
    main()
    

