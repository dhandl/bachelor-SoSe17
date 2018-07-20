from collections import namedtuple
from ROOT import TChain

Sample = namedtuple("Sample", "name tree")

def _load_chain(filenames, treename, print_files=False):
  chain = TChain(treename)
  for name in filenames:
    chain.Add(name)

  if print_files:
    for filename in chain.GetListOfFiles():
      print filename.GetTitle()

  return chain

Preselection = "(dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && (n_jet>=2) && (n_bjet<1) && (jet_pt[0]>25e3) && (jet_pt[1]>25e3) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (met>300e3) &&  (lepPt_over_met<0.06) && (lep_pt<30e3) && (lepJet1_energy_ratio<0.1)"
#Preselection = "(n_jet>=4)"



_PREFIX = "/project/etp5/dbuchin/samples/SUSY/Stop1L/softLepton/"
#_PREFIX = "/project/etp5/dhandl/samples/ttbar_rew/TRUTH3/"

Signal = [
	Sample("stop_bffN_300_280", _load_chain([_PREFIX+"/TT_bffN_300_280/*.root"], "TT_bffN_300_280_Nom"), ),
	Sample("stop_bffN_350_330", _load_chain([_PREFIX+"/TT_bffN_350_330/*.root"], "TT_bffN_350_330_Nom"), ),
	Sample("stop_bffN_400_380", _load_chain([_PREFIX+"/TT_bffN_400_380/*.root"], "TT_bffN_400_380_Nom"), ),
	Sample("stop_bffN_250_230", _load_chain([_PREFIX+"/TT_bffN_250_230/*.root"], "TT_bffN_250_230_Nom"), ),
	Sample("stop_bffN_450_430", _load_chain([_PREFIX+"/TT_bffN_450_430/*.root"], "TT_bffN_450_430_Nom"), ),
	Sample("stop_bffN_500_480", _load_chain([_PREFIX+"/TT_bffN_500_480/*.root"], "TT_bffN_500_480_Nom"), ),
#        Sample("stop_bffN_550_530", _load_chain([_PREFIX+"/TT_bffN_550_530/*.root"], "TT_bffN_550_530_Nom"), ),
#	Sample("stop_bffN_250_200", _load_chain([_PREFIX+"/TT_bffN_250_200/*.root"], "TT_bffN_250_200_Nom"), ),
#	Sample("stop_bffN_300_250", _load_chain([_PREFIX+"/TT_bffN_300_250/*.root"], "TT_bffN_300_250_Nom"), ),
#	Sample("stop_bffN_350_300", _load_chain([_PREFIX+"/TT_bffN_350_300/*.root"], "TT_bffN_350_300_Nom"), ),
#	Sample("stop_bffN_400_350", _load_chain([_PREFIX+"/TT_bffN_400_350/*.root"], "TT_bffN_400_350_Nom"), ),
#	Sample("stop_bffN_450_400", _load_chain([_PREFIX+"/TT_bffN_450_400/*.root"], "TT_bffN_450_400_Nom"), ),
#	Sample("stop_bffN_500_450", _load_chain([_PREFIX+"/TT_bffN_500_450/*.root"], "TT_bffN_500_450_Nom"), ),
#	Sample("stop_bffN_550_500", _load_chain([_PREFIX+"/TT_bffN_550_500/*.root"], "TT_bffN_550_500_Nom"), ),
	#Sample("stop_bffN_550_385", _load_chain([_PREFIX+"/TT_bffN_550_385/*.root"], "TT_bffN_550_385_Nom"), ),
	#Sample("stop_bffN_550_400", _load_chain([_PREFIX+"/TT_bffN_550_400/*.root"], "TT_bffN_550_400_Nom"), ),
	#Sample("stop_bffN_550_430", _load_chain([_PREFIX+"/TT_bffN_550_430/*.root"], "TT_bffN_550_430_Nom"), ),
	#Sample("stop_bffN_550_460", _load_chain([_PREFIX+"/TT_bffN_550_460/*.root"], "TT_bffN_550_460_Nom"), ),
	#Sample("stop_bffN_600_435", _load_chain([_PREFIX+"/TT_bffN_600_435/*.root"], "TT_bffN_600_435_Nom"), ),
	#Sample("stop_bffN_600_450", _load_chain([_PREFIX+"/TT_bffN_600_450/*.root"], "TT_bffN_600_450_Nom"), ),
	#Sample("stop_bffN_600_480", _load_chain([_PREFIX+"/TT_bffN_600_480/*.root"], "TT_bffN_600_480_Nom"), ),
	#Sample("stop_bffN_600_510", _load_chain([_PREFIX+"/TT_bffN_600_510/*.root"], "TT_bffN_600_510_Nom"), ),
	#Sample("stop_bffN_650_485", _load_chain([_PREFIX+"/TT_bffN_650_485/*.root"], "TT_bffN_650_485_Nom"), ),
	#Sample("stop_bffN_650_500", _load_chain([_PREFIX+"/TT_bffN_650_500/*.root"], "TT_bffN_650_500_Nom"), ),
	#Sample("stop_bffN_650_530", _load_chain([_PREFIX+"/TT_bffN_650_530/*.root"], "TT_bffN_650_530_Nom"), ),
	#Sample("stop_bffN_650_560", _load_chain([_PREFIX+"/TT_bffN_350_560/*.root"], "TT_bffN_650_560_Nom"), ),
]

Background = [
	Sample("ttbar",     _load_chain([_PREFIX+"/powheg_ttbar/*.root"],       "powheg_ttbar_Nom"), ),
	#Sample("ttbar_radLo",_load_chain([_PREFIX+"/ttbar_radLo_TRUTH3/*.root"], "ttbar_radLo_TRUTH3_Nom"), ),
	Sample("Wjets",     _load_chain([_PREFIX+"/sherpa22_Wjets/*.root"],     "sherpa22_Wjets_Nom"), ),
	Sample("Zjets",     _load_chain([_PREFIX+"/sherpa22_Zjets/*.root"],     "sherpa22_Zjets_Nom"), ),
	Sample("singletop", _load_chain([_PREFIX+"/powheg_singletop/*.root"],   "powheg_singletop_Nom"), ),
	Sample("Diboson",   _load_chain([_PREFIX+"/sherpa221_diboson/*.root"],  "sherpa221_diboson_Nom"), ),
	Sample("ttV",       _load_chain([_PREFIX+"/amcnlo_ttV/*.root"],         "amcnlo_ttV_Nom"), ),
]

Weight = "xs_weight*weight*sf_total*weight_sherpa22_njets"
