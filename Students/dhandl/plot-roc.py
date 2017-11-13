#!/usr/bin/env python
import sys
import os

from ROOT import *
gROOT.SetBatch(True)

import PlotStyle
from Loading import *
from EvaluateReader import *
from Style import *

###############################

#DIRECTORY = "/project/etp5/lschramm/cut_data_mt60_met120"
DIRECTORY = "/project/etp5/lschramm/cut_data/Stop1L"
BACKGROUNDS = {
	"ttbar": DIRECTORY + "/powheg_ttbar/*.root/powheg_ttbar_Nom",
	"Wjets": DIRECTORY +"/sherpa22_Wjets/*.root/sherpa22_Wjets_Nom",
	"ttV": DIRECTORY +"/amcnlo_ttV/*.root/amcnlo_ttV_Nom",
	"singletop": DIRECTORY +"/powheg_singletop/*.root/powheg_singletop_Nom",
	"diboson": DIRECTORY +"/sherpa221_diboson/*.root/sherpa221_diboson_Nom",
}
SIGNALS = {
        "stop_tN_350_185": DIRECTORY + "/stop_bWN_350_185/*.root/stop_bWN_350_185_Nom",
	"stop_tN_350_200": DIRECTORY + "/stop_bWN_350_200/*.root/stop_bWN_350_200_Nom",
	"stop_tN_350_230": DIRECTORY + "/stop_bWN_350_230/*.root/stop_bWN_350_230_Nom",
}
BACKGROUNDS_LO = {
	"ttbarLo": DIRECTORY + "/ttbar_radLo/*.root/ttbar_radLo_Nom",
	"Wjets": DIRECTORY +"/sherpa22_Wjets/*.root/sherpa22_Wjets_Nom",
	"ttV": DIRECTORY +"/amcnlo_ttV/*.root/amcnlo_ttV_Nom",
	"singletop": DIRECTORY +"/powheg_singletop/*.root/powheg_singletop_Nom",
	"diboson": DIRECTORY +"/sherpa221_diboson/*.root/sherpa221_diboson_Nom",	
}

BACKGROUNDS_HI = {
	"ttbarHi": DIRECTORY + "/ttbar_radHi/*.root/ttbar_radHi_Nom",
	"Wjets": DIRECTORY +"/sherpa22_Wjets/*.root/sherpa22_Wjets_Nom",
	"ttV": DIRECTORY +"/amcnlo_ttV/*.root/amcnlo_ttV_Nom",
	"singletop": DIRECTORY +"/powheg_singletop/*.root/powheg_singletop_Nom",
	"diboson": DIRECTORY +"/sherpa221_diboson/*.root/sherpa221_diboson_Nom",	
}

WEIGHT = "xs_weight * weight * sf_total"


###############################

def evaluate_mlp(sig_hist, bkg_hist, bkgh_hist, bkgl_hist, total_sig, total_bkg, input_name, mva_name, prefix, out_name, lumi):
    
    	sig_max = plot_and_get_sig(sig_hist, bkg_hist, input_name, total_sig, total_bkg, mva_name, prefix, out_name, lumi)

	plot_roc_curve(sig_hist, bkg_hist, bkgh_hist, bkgl_hist, input_name, sig_max, mva_name, prefix, out_name, lumi)

def plot_and_get_sig(sig_hist, bkg_hist, input_name, total_sig, total_bkg, mva_name, prefix, out_name, lumi):

	sig = get_sig_hist(sig_hist, bkg_hist, total_sig, total_bkg, lumi)

	index_max = TMath.LocMax(sig.GetN(), sig.GetY())
	sig_max = "%.1f #pm %.1f" % (sig.GetY()[index_max], sig.GetEY()[index_max])

	return sig_max

def set_nicer_style(hist, color, norm=False):
	hist.SetLineWidth(1)
	hist.SetLineColor(color)
	hist.SetMarkerColor(color)
	hist.SetFillColorAlpha(color, 0.3)

	if norm:
		hist.Scale(1. / hist.Integral())

def plot_roc_curve(sig_hist, bkg_hist, bkgh_hist, bkgl_hist, input_name, sig_max, mva_name, prefix, out_name, lumi):
	out_dir = input_name
	if OUT_DIRECTORY:
		out_dir = OUT_DIRECTORY


	roc, aroc = get_roc_curve_hist_and_area(sig_hist, bkg_hist)
	rocl, arocl = get_roc_curve_hist_and_area(sig_hist, bkgl_hist)
	roch, aroch = get_roc_curve_hist_and_area(sig_hist, bkgh_hist)

	set_nicer_style(roc, kBlack)
	set_nicer_style(rocl, kMagenta)
	set_nicer_style(roch, kGreen + 2)

	canv = TCanvas("roc", "", 800, 600)

	roc.SetTitle("; sig. eff.; bkg. rej.")

	roc.Draw("a l")
	rocl.Draw("same l")
	roch.Draw("same l")

	leg = TLegend(0.2, 0.2, 0.6, 0.4)
	leg.AddEntry(roc, "%s @%s/fb; Area: %f" % (sig_max, lumi, aroc), "l")
	leg.AddEntry(rocl, "Low radiation; Area: %f" % (arocl), "l")
	leg.AddEntry(roch, "High radiation; Area: %f" % (aroch), "l")
	leg.Draw("same")

	save_canv(canv, prefix + input_name + out_name, out_dir + "_" + mva_name + out_name)
###############################

def get_out_name(SIGNALS):
	name = ""
	for n, _smp in SIGNALS.iteritems():
		name +=  "_" + n 
	return name

def parse_options():
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument("name", help="the name of the input xml file")
	parser.add_argument("-v", "--variables", help="configuration file for the used variables", default="variables")

	parser.add_argument("-r", "--random-variable", help="a variable which should be replaced by some random distribution for the evaluation", dest="random_var")

	parser.add_argument("-b", "--nbins", help="binning for mlp distribution", type=int, default=50)
	parser.add_argument("--min", help="minimum x-range for mlp distribution", type=float, default=-1.)
	parser.add_argument("--max", help="maximum x-range for mlp distribution", type=float, default=1.)

	parser.add_argument("-l", "--lumi", help="the luminostity in fb^-1 used to calculate the expected significance", type=float, default=30.)

	parser.add_argument("--sig", help="specify specific signal samples", action="append")

	parser.add_argument("--add-var", help="add an additional variable", action="append")
	parser.add_argument("--rm-var", help="remove a variable", action="append")
	parser.add_argument("--directory", help="specify a directory, if you prefer some special naming scheme")

	opts = parser.parse_args()

	if opts.directory:
		global OUT_DIRECTORY
		OUT_DIRECTORY = opts.directory

	if opts.sig:
		global SIGNALS
		SIGNALS = {}
		for s in opts.sig:
			SIGNALS[s] = DIRECTORY + "/" + s + "/*.root/" + s + "_Nom"


	opts.prefix = ""
	if opts.random_var:
		opts.prefix = opts.random_var + "_"

	return opts

OUT_DIRECTORY = None

def main():
        opts = parse_options()
	out_name = "allSignal"
        
        PRESELECTION = "1.0"
	bkg_tree = load_tree(BACKGROUNDS, PRESELECTION)
	sig_tree = load_tree(SIGNALS, PRESELECTION)
	bkgh_tree = load_tree(BACKGROUNDS_HI, PRESELECTION)
	bkgl_tree = load_tree(BACKGROUNDS_LO, PRESELECTION)

	variables = load_var_list("config/{cfg}.py".format(cfg=opts.variables), opts.add_var, opts.rm_var)
	reader, var_store = create_reader(variables, opts.name)

	random_var_hist = None
	rnd_var_index = None

	bkg_mva = evaluate_mva("bkg", bkg_tree, opts.name.split("_")[-1], reader, var_store, 4000, -1, 1, rnd_var_index, random_var_hist)
	sig_mva = evaluate_mva("sig", sig_tree, opts.name.split("_")[-1], reader, var_store, 4000, -1, 1, rnd_var_index, random_var_hist)
	bkgh_mva = evaluate_mva("bkgh", bkgh_tree, opts.name.split("_")[-1], reader, var_store, 4000, -1, 1, rnd_var_index, random_var_hist)
	bkgl_mva = evaluate_mva("bkgl", bkgl_tree, opts.name.split("_")[-1], reader, var_store, 4000, -1, 1, rnd_var_index, random_var_hist)

	total_sig = get_total_events([sig_tree], "1", weights="weight * sf_total * xs_weight")
	total_bkg = get_total_events([bkg_tree], "1", weights="weight * sf_total * xs_weight")
        total_bkgh = get_total_events([bkgh_tree], "1", weights="weight * sf_total * xs_weight")
	total_bkgl = get_total_events([bkgl_tree], "1", weights="weight * sf_total * xs_weight")

	print "total_sig", total_sig
	print "total_bkg", total_bkg
	print "total_bkgh", total_bkgh
	print "total_bkgl", total_bkgl

	evaluate_mlp(sig_mva, bkg_mva, bkgh_mva, bkgl_mva, total_sig, total_bkg, "_".join(opts.name.split("_")[:-1]), opts.name.split("_")[-1], opts.prefix, out_name, opts.lumi)


###############################

if __name__ == '__main__':
	main()
