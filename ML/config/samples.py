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

Preselection = "(dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && (n_jet>=4) && (n_bjet>=1) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (mt>30e3) && (met>230e3)"
#Preselection = "(n_jet>=4)"



_PREFIX = "/project/etp5/dhandl/samples/SUSY/Stop1L/"
#_PREFIX = "/project/etp5/dhandl/samples/ttbar_rew/TRUTH3/"

Signal = [
	#Sample("stop_bWN_190_23", _load_chain([_PREFIX+"/stop_bWN_190_23/*.root"], "stop_bWN_190_23_Nom"), ),
	#Sample("stop_bWN_220_53", _load_chain([_PREFIX+"/stop_bWN_220_53/*.root"], "stop_bWN_220_53_Nom"), ),
	#Sample("stop_bWN_250_100", _load_chain([_PREFIX+"/stop_bWN_250_100/*.root"], "stop_bWN_250_100_Nom"), ),
	#Sample("stop_bWN_250_130", _load_chain([_PREFIX+"/stop_bWN_250_130/*.root"], "stop_bWN_250_130_Nom"), ),
	#Sample("stop_bWN_250_160", _load_chain([_PREFIX+"/stop_bWN_250_160/*.root"], "stop_bWN_250_160_Nom"), ),
	#Sample("stop_bWN_300_150", _load_chain([_PREFIX+"/stop_bWN_300_150/*.root"], "stop_bWN_300_150_Nom"), ),
	#Sample("stop_bWN_300_180", _load_chain([_PREFIX+"/stop_bWN_300_180/*.root"], "stop_bWN_300_180_Nom"), ),
	#Sample("stop_bWN_300_210", _load_chain([_PREFIX+"/stop_bWN_300_210/*.root"], "stop_bWN_300_210_Nom"), ),
	#Sample("stop_bWN_350_185", _load_chain([_PREFIX+"/stop_bWN_350_185/*.root"], "stop_bWN_350_185_Nom"), ),
	Sample("stop_bWN_350_200", _load_chain([_PREFIX+"/stop_bWN_350_200/*.root"], "stop_bWN_350_200_Nom"), ),
	#Sample("stop_bWN_350_230", _load_chain([_PREFIX+"/stop_bWN_350_230/*.root"], "stop_bWN_350_230_Nom"), ),
	#Sample("stop_bWN_350_260", _load_chain([_PREFIX+"/stop_bWN_350_260/*.root"], "stop_bWN_350_260_Nom"), ),
	#Sample("stop_bWN_400_235", _load_chain([_PREFIX+"/stop_bWN_400_235/*.root"], "stop_bWN_400_235_Nom"), ),
	#Sample("stop_bWN_400_250", _load_chain([_PREFIX+"/stop_bWN_400_250/*.root"], "stop_bWN_400_250_Nom"), ),
	#Sample("stop_bWN_400_280", _load_chain([_PREFIX+"/stop_bWN_400_280/*.root"], "stop_bWN_400_280_Nom"), ),
	#Sample("stop_bWN_400_310", _load_chain([_PREFIX+"/stop_bWN_400_310/*.root"], "stop_bWN_400_310_Nom"), ),
	#Sample("stop_bWN_450_285", _load_chain([_PREFIX+"/stop_bWN_450_285/*.root"], "stop_bWN_450_285_Nom"), ),
	#Sample("stop_bWN_450_300", _load_chain([_PREFIX+"/stop_bWN_450_300/*.root"], "stop_bWN_450_300_Nom"), ),
	#Sample("stop_bWN_450_330", _load_chain([_PREFIX+"/stop_bWN_450_330/*.root"], "stop_bWN_450_330_Nom"), ),
	#Sample("stop_bWN_450_360", _load_chain([_PREFIX+"/stop_bWN_450_360/*.root"], "stop_bWN_450_360_Nom"), ),
	#Sample("stop_bWN_500_335", _load_chain([_PREFIX+"/stop_bWN_500_335/*.root"], "stop_bWN_500_335_Nom"), ),
	#Sample("stop_bWN_500_350", _load_chain([_PREFIX+"/stop_bWN_500_350/*.root"], "stop_bWN_500_350_Nom"), ),
	#Sample("stop_bWN_500_380", _load_chain([_PREFIX+"/stop_bWN_500_380/*.root"], "stop_bWN_500_380_Nom"), ),
	#Sample("stop_bWN_550_385", _load_chain([_PREFIX+"/stop_bWN_550_385/*.root"], "stop_bWN_550_385_Nom"), ),
	#Sample("stop_bWN_550_400", _load_chain([_PREFIX+"/stop_bWN_550_400/*.root"], "stop_bWN_550_400_Nom"), ),
	#Sample("stop_bWN_550_430", _load_chain([_PREFIX+"/stop_bWN_550_430/*.root"], "stop_bWN_550_430_Nom"), ),
	#Sample("stop_bWN_550_460", _load_chain([_PREFIX+"/stop_bWN_550_460/*.root"], "stop_bWN_550_460_Nom"), ),
	#Sample("stop_bWN_600_435", _load_chain([_PREFIX+"/stop_bWN_600_435/*.root"], "stop_bWN_600_435_Nom"), ),
	#Sample("stop_bWN_600_450", _load_chain([_PREFIX+"/stop_bWN_600_450/*.root"], "stop_bWN_600_450_Nom"), ),
	#Sample("stop_bWN_600_480", _load_chain([_PREFIX+"/stop_bWN_600_480/*.root"], "stop_bWN_600_480_Nom"), ),
	#Sample("stop_bWN_600_510", _load_chain([_PREFIX+"/stop_bWN_600_510/*.root"], "stop_bWN_600_510_Nom"), ),
	#Sample("stop_bWN_650_485", _load_chain([_PREFIX+"/stop_bWN_650_485/*.root"], "stop_bWN_650_485_Nom"), ),
	#Sample("stop_bWN_650_500", _load_chain([_PREFIX+"/stop_bWN_650_500/*.root"], "stop_bWN_650_500_Nom"), ),
	#Sample("stop_bWN_650_530", _load_chain([_PREFIX+"/stop_bWN_650_530/*.root"], "stop_bWN_650_530_Nom"), ),
	#Sample("stop_bWN_650_560", _load_chain([_PREFIX+"/stop_bWN_350_560/*.root"], "stop_bWN_650_560_Nom"), ),
	#Sample("ttbar",     _load_chain([_PREFIX+"/powheg_ttbar_TRUTH3/*.root"],       "powheg_ttbar_TRUTH3_Nom"), ),
]

Background = [
	Sample("ttbar",     _load_chain([_PREFIX+"/powheg_ttbar/*.root"],       "powheg_ttbar_Nom"), ),
	#Sample("ttbar_radLo",_load_chain([_PREFIX+"/ttbar_radLo_TRUTH3/*.root"], "ttbar_radLo_TRUTH3_Nom"), ),
	#Sample("Wjets",     _load_chain([_PREFIX+"/sherpa22_Wjets/*.root"],     "sherpa22_Wjets_Nom"), ),
	#Sample("singletop", _load_chain([_PREFIX+"/powheg_singletop/*.root"],   "powheg_singletop_Nom"), ),
	#Sample("Diboson",   _load_chain([_PREFIX+"/sherpa221_diboson/*.root"],  "sherpa221_diboson_Nom"), ),
	#Sample("ttV",       _load_chain([_PREFIX+"/amcnlo_ttV/*.root"],         "amcnlo_ttV_Nom"), ),
]

Weight = "xs_weight*weight*sf_total*weight_sherpa22_njets"
