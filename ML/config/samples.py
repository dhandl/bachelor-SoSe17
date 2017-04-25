
Preselection = "(dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && (n_jet>=4) && (n_bjet>0) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>120e3) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (met >120e3)"


PREFIX = "/lustre/boerner/swup/stop1l-xaod/export/default_moriond17"
Signal = [
	Sample("stop_tN_250_62", load_chain([PREFIX+"/stop_tN_250_62/*.root"], "stop_tN_250_62_Nom"), ),
	]

Backgrounds = [
	Sample("ttbar", load_chain([PREFIX+"/powheg_ttbar/*.root"], "powheg_ttbar_Nom"), ),
	Sample("Wjets", load_chain([PREFIX+"/sherpa22_Wjets/*.root"], "sherpa22_Wjets_Nom"), ),
]

Weight = "xs_weight * weight * sf_total"
