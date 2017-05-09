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

Preselection = "(dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && (n_jet>=4) && (n_bjet>0) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>130e3) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (met >230e3)"

_PREFIX = "/media/Felix.Scheinost/DATEN/Stop1L"

Signal = [
	Sample("stop_bWN_350_200", _load_chain([_PREFIX+"/stop_bWN_350_200/*.root"], "stop_bWN_350_200_Nom"), ),
]

Background = [
	Sample("ttbar",     _load_chain([_PREFIX+"/powheg_ttbar/*.root"],       "powheg_ttbar_Nom"), ),
	#Sample("Wjets",     _load_chain([_PREFIX+"/sherpa22_Wjets/*.root"],     "sherpa22_Wjets_Nom"), ),
	#Sample("singletop", _load_chain([_PREFIX+"/powheg_singletop/*.root"],   "powheg_singletop_Nom"), ),
	#Sample("Diboson",   _load_chain([_PREFIX+"/sherpa221_diboson/*.root"],  "sherpa221_diboson_Nom"), ),
	#Sample("ttV",       _load_chain([_PREFIX+"/amcnlo_ttV/*.root"],         "amcnlo_ttV_Nom"), ),
]

Weight = "xs_weight * weight * sf_total * weight_sherpa22_njets"
