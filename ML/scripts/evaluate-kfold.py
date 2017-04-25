#!/usr/bin/env python
import sys
import os

from ROOT import *
gROOT.SetBatch(True)

import PlotStyle
from Style import *
from Loading import *
from EvaluateReader import *

###############################

DIRECTORY = "/lustre/boerner/swup/stop1l-xaod/export/default_moriond17/"
BACKGROUNDS = {
	"ttbar": DIRECTORY + "/powheg_ttbar/*.root/powheg_ttbar_Nom",
	"Wjets": DIRECTORY +"/sherpa22_Wjets/*.root/sherpa22_Wjets_Nom",
#	"ttV": DIRECTORY +"/madgraph_ttV/*.root/madgraph_ttV_Nom",
#	"singletop": DIRECTORY +"/powheg_singletop/*.root/powheg_singletop_Nom",
#	"diboson": DIRECTORY +"/sherpa_diboson/*.root/sherpa_diboson_Nom",
}
SIGNALS = {
	"stop_tN_250_62": DIRECTORY + "/stop_tN_250_62/*.root/stop_tN_250_62_Nom",
	#"stop_tN_300_112_MET100": DIRECTORY +"/stop_tN_300_112_MET100/*.root/stop_tN_300_112_MET100_Nom",
	#"stop_tN_350_162_MET100": DIRECTORY +"/stop_tN_350_162_MET100/*.root/stop_tN_350_162_MET100_Nom",	
}

PRESELECTION = "(dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && (n_jet>=4) && (n_bjet>0) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>120e3) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (met>120e3)"

WEIGHT = "xs_weight * weight * sf_total"


###############################

def plot_mva_distribution(sig_hist, bkg_hist, input_name, mva_name, lumi, iteration, k_fold):
	set_style(sig_hist, kRed)
	set_style(bkg_hist, kBlue)

	bkg_lumi = bkg_hist.Clone()
	sig_lumi = sig_hist.Clone()

	bkg_lumi.Scale(lumi*1000)
	sig_lumi.Scale(lumi*1000)

	# plot not normalized
	canv = TCanvas("mlp_distribution", "", 800, 600)
	bkg_lumi.SetTitle("; %s; number of events" % mva_name)

	bkg_lumi.Draw("hist")
	sig_lumi.Draw("same hist")

	leg = TLegend(0.5, 0.8, 0.8, 0.9)
	leg.AddEntry(sig_lumi, "Signal", "f")
	leg.AddEntry(bkg_lumi, "Background", "f")
	leg.Draw("same")

	save_canv(canv, input_name + "_" + mva_name + "_k" + str(k_fold) + "_i" + str(iteration), input_name + "_" + mva_name + "_" + str(k_fold) )

	# plot  normalized
	canv = TCanvas("mlp_distribution_norm", "", 800, 600)
	bkg_hist.SetTitle("; %s; fraction of events" % mva_name)


	bkg_norm = bkg_hist.Clone()
	sig_norm = sig_hist.Clone()
	bkg_norm.Scale(1. / bkg_norm.Integral())
	sig_norm.Scale(1. / sig_norm.Integral())

	bkg_norm.Draw("hist")
	sig_norm.Draw("same hist")

	leg = TLegend(0.5, 0.8, 0.8, 0.9)
	leg.AddEntry(sig_norm, "Signal", "f")
	leg.AddEntry(bkg_norm, "Background", "f")
	leg.Draw("same")

	save_canv(canv, input_name + "_" + mva_name + "_k" + str(k_fold) + "_i" + str(iteration), input_name + "_" + mva_name + "_" + str(k_fold))


###############################

def plot_roc_curve(sig_hist, bkg_hist, input_name, sig_max, mva_name, k_fold, lumi):
	roc = get_roc_curve_hist(sig_hist, bkg_hist)

	set_style(roc, kBlack)

	canv = TCanvas("roc", "", 800, 600)

	roc.SetTitle("; sig. eff.; bkg. rej.")

	roc.Draw("a l")

	leg = TLegend(0.2, 0.2, 0.5, 0.4)
	leg.AddEntry(roc, "%.1f @%s/fb" % (sig_max, lumi), "l")
	leg.Draw("same")

	save_canv(canv, input_name, input_name + "_" + mva_name + "_" + str(k_fold))

def plot_and_get_sig(sig_hist, bkg_hist, input_name, total_sig, total_bkg, mva_name, k_fold, lumi):
	sig = get_sig_hist(sig_hist, bkg_hist, total_sig, total_bkg, lumi)

	set_graph_style(sig, kBlack)

	sig.SetTitle(";%s;significance" % mva_name)

	canv = TCanvas("sig", "", 800, 600)

	sig.Draw("a3")
	sig.Draw("lx")

	sig_max = TMath.MaxElement(sig.GetN(), sig.GetY())

	leg = TLegend(0.2, 0.75, 0.6, 0.9)
	PlotStyle.legend(leg)
	leg.AddEntry(sig, "%.1f @%s/fb" % (sig_max, lumi) ,"l")
	leg.Draw()

	save_canv(canv, input_name, input_name + "_" + mva_name + "_" + str(k_fold))

	return sig_max

def evaluate_mlp(sig_hist, bkg_hist, total_sig, total_bkg, input_name, mva_name, k_fold, lumi):
	sig_max = plot_and_get_sig(sig_hist, bkg_hist, input_name, total_sig, total_bkg, mva_name, k_fold, lumi)
	plot_roc_curve(sig_hist, bkg_hist, input_name, sig_max, mva_name, k_fold, lumi)

###############################


def evaluate_k_fold(sig_tree, bkg_tree, total_sig, total_bkg, mva_name, name, reader_list, var_store_list, nbins, min, max, k_fold, lumi):
	bkg_mva = evaluate_mva_k_fold("bkg", bkg_tree, mva_name, reader_list, var_store_list, nbins, min, max, k_fold)
	sig_mva = evaluate_mva_k_fold("sig", sig_tree, mva_name, reader_list, var_store_list, nbins, min, max, k_fold)
	save_mva_hist(sig_mva, bkg_mva, name, mva_name, "all", k_fold)

	plot_mva_distribution(sig_mva, bkg_mva, name, mva_name, lumi, "all", k_fold)

	evaluate_mlp(sig_mva, bkg_mva, total_sig, total_bkg, name, mva_name, k_fold, lumi)

def evaluate_k_fold_test_train(sig_tree, bkg_tree, total_sig, total_bkg, mva_name, name, reader_list, var_store_list, nbins, min, max, k_fold, lumi):
	bkg_mva_test, bkg_mva_train = evaluate_mva_k_fold_test_train("bkg", bkg_tree, mva_name, reader_list, var_store_list, nbins, min, max, k_fold)
	sig_mva_test, sig_mva_train = evaluate_mva_k_fold_test_train("sig", sig_tree, mva_name, reader_list, var_store_list, nbins, min, max, k_fold)

	sig_train = get_max_sig_hist(sig_mva_train, bkg_mva_train, total_sig, total_bkg, lumi)
	sig_test = get_max_sig_hist(sig_mva_test, bkg_mva_test, total_sig, total_bkg, lumi)
	print sig_train, sig_test

	set_style(sig_mva_test, kRed, norm=True)
	set_style(sig_mva_train, kRed, norm=True)

	set_style(bkg_mva_test, kBlue, norm=True)
	set_style(bkg_mva_train, kBlue, norm=True)

	# plot train and test
	canv = TCanvas("mva_dist", "", 800, 600)
	bkg_mva_test.SetTitle("; %s; fraction of events" % mva_name)
	bkg_mva_test.GetYaxis().SetRangeUser(0, bkg_mva_test.GetMaximum() * 1.7)

	bkg_mva_test.Draw("hist")
	sig_mva_test.Draw("same hist")
	bkg_mva_train.Draw("same p")
	sig_mva_train.Draw("same p")

	leg = TLegend(0.3, 0.7, 0.6, 0.9)
	leg.AddEntry(sig_mva_test, "Signal Test", "f")
	leg.AddEntry(bkg_mva_test, "Background Test", "f")
	leg.AddEntry(sig_mva_train, "Signal Train", "pl")
	leg.AddEntry(bkg_mva_train, "Background Train", "pl")
	leg.Draw("same")

	kolmogorov_bkg = bkg_mva_test.KolmogorovTest(bkg_mva_train)
	kolmogorov_sig = sig_mva_test.KolmogorovTest(sig_mva_train)
	chi2_bkg = bkg_mva_test.Chi2Test(bkg_mva_train, "WW CHI2/NDF")
	chi2_sig = sig_mva_test.Chi2Test(sig_mva_train, "WW CHI2/NDF")
	PlotStyle.string(0.65, 0.85, "Kolomogorov Bkg: %1.2f" %kolmogorov_bkg, rel=0.7)
	PlotStyle.string(0.65, 0.8, "Kolomogorov Sig: %1.2f" %kolmogorov_sig, rel=0.7)
	PlotStyle.string(0.65, 0.75, "red. #chi^{2} Bkg: %1.2f" %chi2_bkg, rel=0.7)
	PlotStyle.string(0.65, 0.7, "red. #chi^{2} Sig: %1.2f" %chi2_sig, rel=0.7)

	save_canv(canv, name + "_full", name + "_" + mva_name + "_" + str(k_fold))

	# plot roc curve
	roc_test = get_roc_curve_hist(sig_mva_test, bkg_mva_test)
	roc_train = get_roc_curve_hist(sig_mva_train, bkg_mva_train)

	set_style(roc_train, kCyan+2)
	set_style(roc_test, kBlack)

	canv = TCanvas("roc", "", 800, 600)

	roc_test.SetTitle("; sig. eff.; bkg. rej.")

	roc_test.Draw("a l")
	roc_train.Draw("same l")

	leg = TLegend(0.2, 0.2, 0.5, 0.4)
	leg.AddEntry(roc_train, "Train: %.1f @%s/fb" % (sig_train, lumi), "l")
	leg.AddEntry(roc_test, "Test: %.1f @%s/fb" % (sig_test, lumi), "l")
	leg.Draw("same")

	save_canv(canv, name + "_full", name + "_" + mva_name + "_" + str(k_fold))



def save_mva_hist(sig_mva, bkg_mva, name, mva_name, iteration, k_fold):
	directory = "plots/" + name + "_" + mva_name + "_" + str(k_fold) + "/root/"
	if not os.path.exists(directory):
		os.makedirs(directory)
	sig_mva.SaveAs(directory + "sig_" + str(iteration) + ".root")
	bkg_mva.SaveAs(directory + "bkg_" + str(iteration) + ".root")


def parse_options():
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument("name", help="the name of the input xml file")
	parser.add_argument("-t", help="the type of the MVA", dest="mva_name", default="BDT")
	parser.add_argument("-k", help="number used for k-fold cross-validation", dest="k_fold", default=5, type=int)
	parser.add_argument("-v", "--variables", help="configuration file for the used variables", default="variables")

	parser.add_argument("-b", "--nbins", help="binning for mlp distribution", type=int, default=50)
	parser.add_argument("--min", help="minimum x-range for mlp distribution", type=float, default=-1.)
	parser.add_argument("--max", help="maximum x-range for mlp distribution", type=float, default=1.)

	parser.add_argument("-l", "--lumi", help="the luminostity in fb^-1 used to calculate the expected significance", type=float, default=30.)

	opts = parser.parse_args()

	return opts

def main():
	opts = parse_options()

	bkg_tree = load_tree(BACKGROUNDS, PRESELECTION)
	sig_tree = load_tree(SIGNALS, PRESELECTION)

	variables = load_var_list("config/{cfg}.py".format(cfg=opts.variables))

	reader_list = []
	var_store_list = []
	for index in xrange(0, opts.k_fold):
		reader, var_store = create_reader(variables, opts.name + "_k" + str(opts.k_fold) + "_i" + str(index) + "_" + opts.mva_name)	
		reader_list.append(reader)
		var_store_list.append(var_store)				

		bkg_mva = evaluate_mva("bkg_" + str(index), bkg_tree, opts.mva_name, reader, var_store, opts.nbins, opts.min, opts.max)
		sig_mva = evaluate_mva("sig_" + str(index), sig_tree, opts.mva_name, reader, var_store, opts.nbins, opts.min, opts.max)
		save_mva_hist(sig_mva, bkg_mva, opts.name, opts.mva_name, index, opts.k_fold)

		plot_mva_distribution(sig_mva, bkg_mva, opts.name, opts.mva_name, opts.lumi, index, opts.k_fold)

	total_sig = get_total_events([sig_tree], "1", weights="weight * sf_total * xs_weight")
	total_bkg = get_total_events([bkg_tree], "1", weights="weight * sf_total * xs_weight")
	print "total_sig", total_sig
	print "total_bkg", total_bkg

	evaluate_k_fold(sig_tree, bkg_tree, total_sig, total_bkg, opts.mva_name, opts.name, reader_list, var_store_list, opts.nbins, opts.min, opts.max, opts.k_fold, opts.lumi)
	evaluate_k_fold_test_train(sig_tree, bkg_tree, total_sig, total_bkg, opts.mva_name, opts.name, reader_list, var_store_list, opts.nbins, opts.min, opts.max, opts.k_fold, opts.lumi)


###############################

if __name__ == '__main__':
	main()
