from ROOT import *

PREFIX = "/project/etp5/dhandl/samples/SUSY/Stop1L"
PREFIX_CUT = "/project/etp5/lschramm/cut_data/Stop1L"

def load(name, treename):
  chain = TChain(treename)
  chain_cut = TChain(treename)

  chain.Add(PREFIX+name)
  chain_cut.Add(PREFIX_CUT+name)

  return (chain, chain_cut)

Signal = [
	load("/stop_bWN_350_200/*.root", "stop_bWN_350_200_Nom"),
]

Background = [
	load("/powheg_ttbar/*.root", "powheg_ttbar_Nom"),
	load("/sherpa22_Wjets/*.root", "sherpa22_Wjets_Nom"),
	load("/powheg_singletop/*.root", "powheg_singletop_Nom"),
	load("/sherpa221_diboson/*.root", "sherpa221_diboson_Nom"),
	load("/amcnlo_ttV/*.root", "amcnlo_ttV_Nom")
]


sig_events, total_sig_events = 0, 0
bkg_events, total_bkg_events = 0, 0

for (chain, chain_cut) in Signal:
	sig_events 		 += chain_cut.GetEntries()
	total_sig_events += chain.GetEntries()

for (chain, chain_cut) in Background:
	bkg_events 		 += chain_cut.GetEntries()
	total_bkg_events += chain.GetEntries()

print "Sig-Eff: " + str(float(sig_events)/total_sig_events)
print "Bkg-Eff: " + str(float(total_bkg_events-bkg_events)/total_bkg_events)
