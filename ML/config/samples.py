
Preselection = "(dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && (n_jet>=4) && (n_bjet>0) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>130e3) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (met >230e3)"


PREFIX = "/project/etp5/dhandl/samples/SUSY/Stop1L/"
Signal = [
	Sample("stop_bWN_350_200", load_chain([PREFIX+"/stop_bWN_350_200/*.root"], "stop_bWN_350_200_Nom"), ),
	]

Backgrounds = [
	Sample("ttbar",     load_chain([PREFIX+"/powheg_ttbar/*.root"],       "powheg_ttbar_Nom"), ),
	Sample("Wjets",     load_chain([PREFIX+"/sherpa22_Wjets/*.root"],     "sherpa22_Wjets_Nom"), ),
	Sample("singletop", load_chain([PREFIX+"/powheg_singletop/*.root"],   "powheg_singletop_Nom"), ),
	Sample("Diboson",   load_chain([PREFIX+"/sherpa221_diboson/*.root"],  "sherpa221_diboson_Nom"), ),
	Sample("ttV",       load_chain([PREFIX+"/amcnlo_ttV/*.root"],         "amcnlo_ttV_Nom"), ),
]

Weight = "xs_weight * weight * sf_total * weight_sherpa22_njets"
