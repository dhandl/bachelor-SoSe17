from collections import namedtuple

_V = namedtuple("Variable", "title unit binning tags")

DPHI_BINNING = "32,0,3.2"
PHI_BINNING = "20,-3.2,3.2"
ETA_BINNING = "20,-2.5,2.5"

Variables = {
	'dilep_mbl': _V("reco min-max m_{bl}", "GeV", "20,0,200", tags=["common"]),
	'dilep_mbl_truth': _V("truth min-max m_{bl}", "GeV", "20,0,200", tags=["common"]),
        'dilep_mt2': _V('reco m_{T2}','GeV', "20,0,200", tags=["common"]),
        'dilep_mt2_truth': _V('truth m_{T2}','GeV', "20,0,200", tags=["common"]),

	'sqrt((lep_pt[0]+met*cos(dphi_met_lep))^2+(met*sin(dphi_met_lep))^2)/1e3': _V("p_{T}(W)", "GeV", "20,0,200", tags=["common"]),

	'n_jet': _V("Jet multiplicity", None, "15,-.5,14.5", tags=["common"]),
	'n_bjet': _V("b-jet multiplicity", None, "5,-.5,4.5", tags=["common"]),
	'n_ph': _V("Photon multiplicity", None, "5,-.5,4.5", tags=["common"]),
	'n_fatjet': _V("large-R jet multiplicity", None, "9,-.5,8.5", tags=[]),

	'n_fatjet_R10_L0': _V("large-R jet multiplicity", None, "6,-.5,5.5", tags=[]),
	'n_fatjet_R12_L0': _V("large-R jet multiplicity", None, "6,-.5,5.5", tags=[]),

	'av_int_per_xing': _V("<mu>", None, "50,0,50", tags=[]),
	'av_int_per_xing/(1+0.16*(xs_weight==1))': _V("Corrected <mu>", None, "50,0,50", tags=[]),
	'num_pv': _V("Number of primary vertices", None, "50,.5,50.5", tags=[]),

	'met': _V("E_{T}^{miss}", "GeV", "40,100,1000", tags=["common"]),
	'met_phi': _V("E_{T}^{miss} #phi", None, PHI_BINNING, tags=[]),
	'met_cst': _V("E_{T}^{miss} (CST)", "GeV", "45,100,1000", tags=["common"]),
	'met_soft': _V("E_{T}^{miss} (TST)", "GeV", "50,0,500", tags=["common"]),
	'met_sumet': _V("sumet", "GeV", "100,0,4000", tags=["common"]),
	'mt': _V("m_{T}", "GeV", "30,0,600", tags=["common"]),
	'photon_mt': _V("#tilde{m}_{T} = m_{T} with photon added", "GeV", "25,0,500", tags=["common"]),
	'ph_pt[0]': _V("photon p_{T}", "GeV", "20,0,500", tags=["common"]),
	'ph_pt': _V("photon p_{T}", "GeV", "20,0,500", tags=["common"]),
	'cst_mt': _V("m_{T} (CST)", "GeV", "30,0,600", tags=["common"]),
	'neutrino_met': _V("truth HS E_{T}^{miss}", "GeV", "45,100,1000", tags=["common"]),
	'photon_met': _V("#tilde{E}_{T}^{miss} = E_{T}^{miss} with photon added", "GeV", "25,0,500", tags=["common"]),
	'dilep_m': _V("m_{ll}", "GeV", "20,0,200", tags=["common"]),

	'mt2stop': _V("m_{T2}(#tilde{t})", "GeV", "90,0,900", tags=[]),

	'amt2': _V("am_{T2}", "GeV", "25,0,500", tags=["common"]),
	'mt2_tau': _V("m_{T2}^{#tau}", "GeV", "25,0,500", tags=["common"]),
	'mT2tauLooseTau_GeV': _V("m_{T2}^{#tau}", "GeV", "25,0,500", tags=["common"]),
	'topness': _V("topness", None, "30,-10,20", tags=["common"]),
	'ht': _V("H_{T}", "GeV", "20,0,1600", tags=["common"]),
	'ht_sig': _V("H_{T}^{miss} significance", None, "30,0,30", tags=["common"]),
	'ht_sig200': _V("H_{T}^{miss} significance (M=200)", None, "30,0,30", tags=["common"]),
	'ht_sig300': _V("H_{T}^{miss} significance (M=300)", None, "30,0,30", tags=["common"]),
	'ht_sig50': _V("H_{T}^{miss} significance (M=50)", None, "30,0,30", tags=["common"]),
	'ht_sig0': _V("H_{T}^{miss} significance (M=0)", None, "30,10,40", tags=["common"]),


	'ht_sig_photon': _V("#tilde{H}_{T}^{miss} significance", None, "30,0,30", tags=["common"]),
	'met_sig': _V("E_{T}^{miss}/#sqrt{H_{T}}", None, "25,0,25", tags=["common"]),
	'm_top': _V("#DeltaR based m_{t,had}", "GeV", "30,100,400", tags=["common"]),
	'm_top_chi2': _V("#chi^{2} based m_{t,had}", "GeV", "25,100,350", tags=["common"]),
	'dr_bjet_lep': _V("#DeltaR(b-jet, lepton)", "", "25,0,5", tags=[] ),
	'mindr_bjet_lep': _V("#DeltaR(b-jet, lepton)", "", "25,0,5", tags=[] ),
	'top_dr_bjet_lep': _V("#DeltaR(b-jet, lepton)", "", "25,0,5", tags=[] ),
	'm_bl': _V("m_{b+l}", "GeV", "25,0,500", tags=["common"]),

	'lep_pt[0]': _V("lepton p_{T}", "GeV", "25,0,500", tags=["common"]),
	'lep_phi[0]': _V("lepton #phi", None, PHI_BINNING, tags=["common"]),
	'lep_eta[0]': _V("lepton #eta", None, ETA_BINNING, tags=["common"]),
	'abs(ROOT::Math::VectorUtil::Phi_mpi_pi(lep_phi[0] - met_phi))': _V("|#Delta#phi(lep,E_{T}^{miss})|", None, PHI_BINNING, tags=[]),

	'el_pt[0]': _V("electron p_{T}", "GeV", "25,0,500", tags=["common"]),
	'el_phi[0]': _V("electron #phi", None, PHI_BINNING, tags=["common"]),
	'el_eta[0]': _V("electron #eta", None, ETA_BINNING, tags=["common"]),

	'mu_pt[0]': _V("muon p_{T}", "GeV", "25,0,500", tags=["common"]),
	'mu_phi[0]': _V("muon #phi", None, PHI_BINNING, tags=["common"]),
	'mu_eta[0]': _V("muon #eta", None, ETA_BINNING, tags=["common"]),

	'jet_pt[0]': _V("first jet p_{T}", "GeV", "25,0,500", tags=["common"]),
	'jet_phi[0]': _V("first jet #phi", None, PHI_BINNING, tags=["common"]),
	'jet_eta[0]': _V("first jet #eta", None, ETA_BINNING, tags=["common"]),
	'jet_Jvt[0]': _V("first jet JVT", None, "30,0,1", tags=[]),
	'abs(ROOT::Math::VectorUtil::Phi_mpi_pi(jet_phi[0] - met_phi))': _V("|#Delta#phi(jet_{1},E_{T}^{miss})|", None, PHI_BINNING, tags=[]),

	'jet_pt[1]': _V("second jet p_{T}", "GeV", "35,0,350", tags=["common"]),
	'jet_phi[1]': _V("second jet #phi", None, PHI_BINNING, tags=["common"]),
	'jet_eta[1]': _V("second jet #eta", None, ETA_BINNING, tags=["common"]),
	'jet_Jvt[1]': _V("second jet JVT", None, "30,0,1", tags=[]),
	'abs(ROOT::Math::VectorUtil::Phi_mpi_pi(jet_phi[1] - met_phi))': _V("|#Delta#phi(jet_{2},E_{T}^{miss})|", None, PHI_BINNING, tags=[]),
	'jet_pt[2]': _V("third jet p_{T}", "GeV", "25,0,250", tags=["common"]),
	'jet_phi[2]': _V("third jet #phi", None, PHI_BINNING, tags=["common"]),
	'jet_eta[2]': _V("third jet #eta", None, ETA_BINNING, tags=["common"]),
	'jet_Jvt[2]': _V("third jet JVT", None, "30,0,1", tags=[]),
	'abs(ROOT::Math::VectorUtil::Phi_mpi_pi(jet_phi[2] - met_phi))': _V("|#Delta#phi(jet_{3},E_{T}^{miss})|", None, PHI_BINNING, tags=[]),
	'jet_pt[3]': _V("fourth jet p_{T}", "GeV", "20,0,200", tags=["common"]),
	'jet_phi[3]': _V("fourth jet #phi", None, PHI_BINNING, tags=["common"]),
	'jet_eta[3]': _V("fourth jet #eta", None, ETA_BINNING, tags=["common"]),
	'jet_Jvt[3]': _V("fourth jet JVT", None, "30,0,1", tags=[]),
	'abs(ROOT::Math::VectorUtil::Phi_mpi_pi(jet_phi[3] - met_phi))': _V("|#Delta#phi(jet_{4},E_{T}^{miss})|", None, PHI_BINNING, tags=[]),

	'jet_m[0]': _V("first jet mass", "GeV", "70,0,350", tags=["common"]),
	'jet_m[1]': _V("second jet mass", "GeV", "70,0,350", tags=["common"]),
	'jet_m[2]': _V("third jet mass", "GeV", "70,0,350", tags=["common"]),
	'jet_m[3]': _V("fourth jet mass", "GeV", "70,0,350", tags=["common"]),


	'bjet_pt[0]': _V("first b-jet p_{T}", "GeV", "50,0,500", tags=["common"]),
	'bjet_phi[0]': _V("first b-jet #phi", None, PHI_BINNING, tags=["common"]),
	'bjet_eta[0]': _V("first b-jet #eta", None, ETA_BINNING, tags=["common"]),
	'bjet_pt[1]': _V("second b-jet p_{T}", "GeV", "50,0,500", tags=["common"]),
	'bjet_phi[1]': _V("second b-jet #phi", None, PHI_BINNING, tags=["common"]),
	'bjet_eta[1]': _V("second b-jet #eta", None, ETA_BINNING, tags=["common"]),
	'min(calc_mbl(bjet_pt[0],bjet_eta[0],bjet_phi[0],bjet_e[0],lep_pt[0],lep_eta[0],lep_phi[0],lep_e[0]),calc_mbl(bjet_pt[1],bjet_eta[1],bjet_phi[1],bjet_e[1],lep_pt[0],lep_eta[0],lep_phi[0],lep_e[0]))': _V("m_{b+l}", "GeV", "50,0,1500", tags=["common"]),
	'deltaRbb_orderpt': _V("#DeltaR(b_{1}, b_{2})", None, "10,0,6", tags=["common"]),
	'calc_Bosonpt(met,lep_pt[0],met_phi,lep_phi[0])': _V("boson p_{T}", "GeV", "50,0,1500", tags=["common"]),
	

	'fatjet_pt[0]': _V("first large-R jet p_{T}", "GeV", "65,150,800", tags=[]),
	'fatjet_phi[0]': _V("first large-R jet #phi", None, PHI_BINNING, tags=[]),
	'fatjet_eta[0]': _V("first large-R jet #eta", None, ETA_BINNING, tags=[]),
	'fatjet_m[0]': _V("first large-R jet mass", "GeV", "70,0,350", tags=[]),
	'fatjet_width[0]': _V("first large-R jet width", None, "50,0,1", tags=[]),
	'fatjet_split12[0]': _V("first large-R jet splitting scale", "GeV", "50,0,300", tags=[]),
	'fatjet_tau1[0]': _V("first large-R jet #tau_{1}", None, "50,0,1", tags=[]),
	'fatjet_tau2[0]': _V("first large-R jet #tau_{2}", None, "50,0,1", tags=[]),
	'fatjet_tau3[0]': _V("first large-R jet #tau_{3}", None, "50,0,1", tags=[]),
	'fatjet_tau21[0]': _V("first large-R jet #tau_{2}/#tau_{1}", None, "50,0,1", tags=[]),
	'fatjet_tau31[0]': _V("first large-R jet #tau_{3}/#tau_{1}", None, "50,0,1", tags=[]),
	'fatjet_tau32[0]': _V("first large-R jet #tau_{3}/#tau_{2}", None, "50,0,1", tags=[]),

	'fatjet_R12_L0_pt[0]': _V("large-R jet p_{T}", "GeV", "35,150,850", tags=[]),
	'fatjet_R12_L0_m[0]': _V("large-R jet mass", "GeV", "35,0,350", tags=[]),
	'fatjet_R10_L0_pt[0]': _V("leading large-R jet p_{T}", "GeV", "35,150,850", tags=[]),
	'fatjet_R10_L0_m[0]': _V("leading large-R jet mass", "GeV", "35,0,350", tags=[]),
	'fatjet_R10_L0_pt[1]': _V("sub-leading large-R jet p_{T}", "GeV", "35,150,850", tags=[]),
	'fatjet_R10_L0_m[1]': _V("sub-leading large-R jet mass", "GeV", "35,0,350", tags=[]),

	'fatjet_R8_L0_pt[0]': _V("large-R=0.8 jet p_{T}", "GeV", "35,150,850", tags=[]),
	'fatjet_R8_L0_m[0]': _V("large-R=0.8 jet mass", "GeV", "35,0,350", tags=[]),
	'fatjet_R6_L0_pt[0]': _V("large-R=0.6 jet p_{T}", "GeV", "35,150,850", tags=[]),
	'fatjet_R6_L0_m[0]': _V("large-R=0.6 jet mass", "GeV", "35,0,350", tags=[]),

	'fatjet_VR350_pt[0]': _V("VR_{#rho=350 GeV} jet p_{T}", "GeV", "35,150,850", tags=[]),
	'fatjet_VR350_m[0]': _V("VR_{#rho=350 GeV} jet mass", "GeV", "35,0,350", tags=[]),
	'fatjet_mo_VR350_pt[0]': _V("VR_{#rho=350 GeV} jet p_{T}", "GeV", "35,150,850", tags=[]),
	'fatjet_mo_VR350_m[0]': _V("VR_{#rho=350 GeV} jet mass", "GeV", "35,0,350", tags=[]),

	'minDRfatjetTop': _V("min #DeltaR(truth top, J_{1})", None, "50,0,2", tags=[]),

	'truth_met_reso': _V("(E_{T,reco}^{miss} - E_{T,truth}^{miss}) / E_{T,truth}^{miss}", None, "100,-1.2,1.2", tags=["truth"]),
	'truth_met_reso_phi': _V("(#phi(E_{T,reco}^{miss}) - #phi(E_{T,truth}^{miss})) / #phi(E_{T,truth}^{miss})", None, "100,-1.2,1.2", tags=["truth"]),

	'truth_met': _V("truth E_{T}^{miss}", "GeV", "50,0,1000", tags=["truth"]),
	'truth_met_sumet': _V("truth sumet", "GeV", "100,0,1000", tags=["truth"]),

	'met-truth_met': _V("E_{T,reco}^{miss} - E_{T,truth}^{miss}", "GeV", "100,-50,50", tags=["truth"]),
	'met_phi-truth_met_phi': _V("#phi(E_{T,reco}^{miss}) - #phi(E_{T,truth}^{miss})", "rad", "100,-3.2,3.2", tags=["truth"]),

	'dphi_met_fatjet1_R12_L0': _V("#Delta#phi(2^{nd} Large R jet, E_{T}^{miss})", None, PHI_BINNING, tags=[]),
	'dphi_met_lep': _V("#Delta#phi(lep, E_{T}^{miss})", None, PHI_BINNING, tags=[]),
	'dphi_ttbar': _V("#Delta#phi(t_{lep},t_{had})", None, PHI_BINNING, tags=[]),
	'dphi_leptop_met': _V("#Delta#phi(t_{lep},E_{T}^{miss})", None, PHI_BINNING, tags=[]),
	'dphi_hadtop_met': _V("#Delta#phi(t_{had},E_{T}^{miss})", None, PHI_BINNING, tags=[]),
	'dphi_jet0_ptmiss': _V("#Delta#phi(E_{T}^{miss}, j_{1})", None, PHI_BINNING, tags=[]),
	'dphi_jet1_ptmiss': _V("#Delta#phi(E_{T}^{miss}, j_{2})", None, PHI_BINNING, tags=[]),
	'dphi_min_ptmiss': _V("min #Delta#phi(E_{T}^{miss}, j)", None, PHI_BINNING, tags=[]),

	'met_perp': _V("perp. E_{T}^{miss}", "GeV", "32,0,800", tags=["top"]),
	'ttbar_m': _V("m_{t#bar{t}}", "GeV", "50,0,1500", tags=["top"]),
	'ttbar_pt': _V("p_{T}(t#bar{t})", "GeV", "50,0,500", tags=["top"]),

	'hadtop_pt': _V("hadronic top p_{T}", "GeV", "50,0,1000", tags=["top"]),
	'leptop_pt': _V("leptonic top p_{T}", "GeV", "50, 0, 500", tags=["top"]),
	'truth_hadtop_pt': _V("hadronic top p_{T}", "GeV", "50,0,1000", tags=["top"]),
	'truth_leptop_pt': _V("leptonic top p_{T}", "GeV", "50, 0, 500", tags=["top"]),

	'abs(dphi_ttbar)': _V("|#Delta#phi(t_{lep},t_{had})|", None, "50,0,3.2", tags=["top"]),
	'abs(dphi_leptop_met)': _V("|#Delta#phi(t_{lep},E_{T}^{miss})|", None, "50,0,3.2", tags=["top"]),
	'abs(dphi_hadtop_met)': _V("|#Delta#phi(t_{had},E_{T}^{miss})|", None, "50,0,3.2", tags=["top"]),
	'abs(dphi_met_lep)': _V("|#Delta#phi(lep, E_{T}^{miss})|", None, "50,0,3.2", tags=["top"]),

	'truth_met_perp': _V("truth perp. E_{T}^{miss}", "GeV", "80,0,800", tags=["top"]),
	'truth_ttbar_m': _V("truth m_{t#bar{t}}", "GeV", "50,0,1500", tags=["top"]),
	'truth_ttbar_pt': _V("truth p_{T}(t#bar{t})", "GeV", "50,0,500", tags=["top"]),

	'abs(truth_dphi_ttbar)': _V("truth |#Delta#phi(t_{lep},t_{had})|", None, "50,0,3.2", tags=["top"]),
	'abs(truth_dphi_leptop_met)': _V("truth |#Delta#phi(t_{lep},E_{T}^{miss})|", None, "50,0,3.2", tags=["top"]),
	'abs(truth_dphi_hadtop_met)': _V("truth |#Delta#phi(t_{had},E_{T}^{miss})|", None, "50,0,3.2", tags=["top"]),


	'incb_met_perp': _V("perp. E_{T}^{miss}", "GeV", "80,0,800", tags=["top"]),
	'incb_ttbar_m': _V("m_{t#bar{t}}", "GeV", "50,0,1500", tags=["top"]),
	'incb_ttbar_pt': _V("p_{T}(t#bar{t})", "GeV", "50,0,500", tags=["top"]),
	'abs(incb_dphi_ttbar)': _V("|#Delta#phi(t_{lep},t_{had})|", None, "50,0,3.2", tags=["top"]),
	'abs(incb_dphi_leptop_met)': _V("|#Delta#phi(t_{lep},E_{T}^{miss})|", None, "50,0,3.2", tags=["top"]),
	'abs(incb_dphi_hadtop_met)': _V("|#Delta#phi(t_{had},E_{T}^{miss})|", None, "50,0,3.2", tags=["top"]),

	'el_ptcone20[0]': _V("e ptcone20", "GeV", "50,0,10", tags=["iso"]),
	'mu_ptcone20[0]': _V("#mu ptcone20", "GeV", "50,0,10", tags=["iso"]),
	'el_ptvarcone20[0]': _V("e ptvarcone20", "GeV", "50,0,10", tags=["iso"]),
	'mu_ptvarcone20[0]': _V("#mu ptvarcone20", "GeV", "50,0,10", tags=["iso"]),

	'n_hadtop_cand': _V("reclustered jet multiplicity", None, "5,-0.5,4.5", tags=[]),
	'hadtop_cand_m[0]': _V("reclustered jet mass", "GeV", "35,0,350", tags=[]),
	'hadw_cand_m[0]': _V("reclustered jet mass (W hypothesis)", "GeV", "20,0,200", tags=[]),
	'hadtop_cand_pt[0]': _V("reclustered jet p_{T}", "GeV",  "50,0,1000", tags=[]),
	'hadtop_cand_r[0]': _V("reclustered jet radius", "", "30,0,3", tags=[]),
	'hadtop_cand_n_constit[0]': _V("reclustered jet constituents", "", "10,0.5,10.5", tags=[]),
	'hadtop_cand_n_btag[0]': _V("reclustered jet btag multiplicity", "", "6,-.5,5.5", tags=[]),


	'rrtop_m': _V("reclustered jet mass", "GeV", "35,0,350", tags=[]),
	'rrtop_pt': _V("reclustered jet p_{T}", "GeV",  "50,0,1000", tags=[]),
	'rrtop_r': _V("reclustered jet radius", "", "30,0,3", tags=[]),
	'rrtop_n_constit': _V("reclustered jet constituents", "", "10,0.5,10.5", tags=[]),
	'rrtop_n_btag': _V("reclustered jet btag multiplicity", "", "6,-.5,5.5", tags=[]),


	'rrtop_m[0]': _V("leading reclustered jet mass", "GeV", "35,0,350", tags=[]),
	'rrtop_m[1]': _V("sub-leading reclustered jet mass", "GeV", "35,0,350", tags=[]),
	'rrtop_pt[0]': _V("leading reclustered jet p_{T}", "GeV",  "35,0,700", tags=[]),
	'rrtop_pt[1]': _V("sub-leading reclustered jet p_{T}", "GeV",  "35,0,700", tags=[]),
	'n_rrtop': _V("reclustered jet multiplicity", "", "5,-.5,4.5", tags=[]),

	'rrtop_r[0]': _V("leading reclustered jet radius", "", "30,0,3", tags=[]),
	'rrtop_r[1]': _V("sub-leading reclustered jet radius", "", "30,0,3", tags=[]),

	'rrtop_n_constit[0]': _V("leading reclustered jet constituents", "", "10,0.5,10.5", tags=[]),
	'rrtop_n_constit[1]': _V("sub-leading reclustered jet constituents", "", "10,0.5,10.5", tags=[]),
	'rrtop_n_btag[0]': _V("leading reclustered jet btag multiplicity", "", "6,-.5,5.5", tags=[]),
	'rrtop_n_btag[1]': _V("sub-leading reclustered jet btag multiplicity", "", "6,-.5,5.5", tags=[]),

	'mt2stop_chi2': _V("m_{T2}(#tilde{t})", "GeV", "100,0,1000", tags=[]),
	'mt2stop_top_cand': _V("m_{T2}(#tilde{t})", "GeV", "100,0,1000", tags=[]),
	'mt2stop_fatjet_R10': _V("m_{T2}(#tilde{t})", "GeV", "100,0,1000", tags=[]),
	'mt2stop_fatjet_R12': _V("m_{T2}(#tilde{t})", "GeV", "100,0,1000", tags=[]),

	'tt_cat': _V("t#bar{t} decay", None, "11,0,11", tags=["common"]),
	'TT_decay_mode': _V("TT decay", None, "6,0.5,6.5", tags=[]),

	'fatjet_ta_R10_L0_pt[0]': _V("leading large-R jet p_{T} (TA)", "GeV", "35,150,850", tags=[]),
	'fatjet_ta_R10_L0_m[0]': _V("leading large-R jet mass (TA)", "GeV", "35,0,350", tags=[]),
	'fatjet_ta_R10_L0_pt[1]': _V("sub-leading large-R jet p_{T} (TA)", "GeV", "35,150,850", tags=[]),
	'fatjet_ta_R10_L0_m[1]': _V("sub-leading large-R jet mass (TA)", "GeV", "35,0,350", tags=[]),

	'lost_lep_pt[0]': _V("lost lepton p_{T}", "GeV", "15,0,150", tags=[]),
	'lost_lep_eta[0]': _V("lost lepton #eta", None, "50,-5,5", tags=[]),
	'lost_lep_phi[0]': _V("lost lepton #phi", None, PHI_BINNING, tags=[]),
	'lost_lep_e[0]': _V("lost lepton energy", "GeV", "15,0,150", tags=[]),
	'abs(lost_lep_pdg_id[0])': _V("lost lepton type", None, "3,10,16", tags=[]),

	'BDT250_highmT': _V("BDT", "", "50,-1,1", tags=[]),

}

BinLabels = {
	'tt_cat': ("#font[12]{l}#font[12]{l}", "#font[12]{l}h", "#font[12]{l}#tau_{h}", "#font[12]{l}#tau_{#font[12]{l}}",
	           "#tau_{#font[12]{l}}h", "#tau_{#font[12]{l}}#tau_{h}", "#tau_{#font[12]{l}}#tau_{#font[12]{l}}", "hh",
	           "h#tau_{h}", "#tau_{h}#tau_{h}", "other" ),

	'TT_decay_mode': (
		"WbWb", "ZtZt", "WbZt", "HtHt", "WbHt", "ZtHt", #"", "Error",
	),

	'abs(lost_lep_pdg_id[0])': ("e", "#mu", "#tau"),
}

ConvertToGeV = [
	'met', 'mt','ht', 'cst_mt', 'neutrino_met',
	'jet_pt', 'jet_m', 'jet_ta_m', 'lep_pt', 'el_pt', 'mu_pt', 'bjet_pt','dilep_m',
	'm_top',
	'fatjet_pt',
	'fatjet_m',
	'fatjet_R12_L0_pt',
	'fatjet_R12_L0_m',
	'fatjet_R10_L0_pt',
	'fatjet_R10_L0_m',
	'fatjet_ta_R10_L0_pt',
	'fatjet_ta_R10_L0_m',
	'fatjet_R8_L0_pt',
	'fatjet_R8_L0_m',
	'fatjet_R6_L0_pt',
	'fatjet_R6_L0_m',
	'fatjet_VR350_pt',
	'fatjet_VR350_m',
	'fatjet_mo_VR350_pt',
	'fatjet_mo_VR350_m',
	'met-truth_met',
	'photon_met','photon_mt','ph_pt',

	"el_ptcone",
	"mu_ptcone",
	"el_ptvarcone",
	"mu_ptvarcone",

	'mt2stop',
	'min(calc',

	'hadtop_pt', 'leptop_pt',
	'truth_hadtop_pt', 'truth_leptop_pt',

	'met_perp', 'ttbar_m', 'ttbar_pt',
	'truth_met',
	'truth_met_perp', 'truth_ttbar_m', 'truth_ttbar_pt',
	'incb_met_perp', 'incb_ttbar_m', 'incb_ttbar_pt',
        'm_bl',

	'rrtop_pt', 'rrtop_e', 'rrtop_m',
	'hadtop_cand_pt', 'hadtop_cand_e', 'hadtop_cand_m', 'hadw_cand_m'
	'hadtop_cand_pt', 'hadtop_cand_e', 'hadtop_cand_m',

	'lost_lep_pt',
]

ConversionBlacklist = [
	'mt2_tau', 'm_top_chi2', 'ht_sig', 'ht_sig_photon', 'met_sig',
	'dilep_mbl','dilep_mbl_truth',
	'dilep_mt2','dilep_mt2_truth',
	'mt2_tau', 'm_top_chi2', 'ht_sig', 'ht_sig200', 'ht_sig0', 'ht_sig300', 'ht_sig50', 'ht_sig_photon', 'met_sig',
	'met_phi', 'truth_met_phi',

	'truth_met_reso',
	'truth_met_reso_phi',
]

ConversionBlacklistMarkers = [
	'*', '/', ':',
]

def title(var):
	return Variables.get(var, _V(var, None, None, [])).title

def unit(var):
	return Variables.get(var, _V(var, None, None, [])).unit

def binning(var, uservalue=None):
	if uservalue:
		return uservalue

	if ":" in var and not "::" in var and not '?' in var:
		yname, xname = var.split(":")

		yvar = Variables.get(yname, None)
		xvar = Variables.get(xname, None)

		if yvar and xvar and xvar.binning and yvar.binning:
			return "%s,%s" % (xvar.binning, yvar.binning)
		return None

	return Variables.get(var, _V(var, None, uservalue, [])).binning

def convert_to_GeV(var):
	if var in ConversionBlacklist:
		return False

	for marker in  ConversionBlacklistMarkers:
		if marker in var:
			return False

	for conv in ConvertToGeV:
		if var.startswith(conv):
			return True

	return False

def conv_unit(var):
	if convert_to_GeV(var):
		return "((%s)*1e-3)" % var

	return var

#Allows users to keep non-default binnings, update variables and add new ones
try:
	import SWup.Variables_private

	if hasattr(SWup.Variables_private, 'update_variables'):
		SWup.Variables_private.update_variables(Variables, _V)
except ImportError:
	pass
