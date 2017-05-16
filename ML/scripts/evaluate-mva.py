#!/usr/bin/env python
import sys
import os

from ROOT import *
gROOT.SetBatch(True)

import PlotStyle
from Loading import *
from EvaluateReader import *
from Style import *

import config

from operator import itemgetter

OUT_DIRECTORY = None

def plot_mva_distribution(sig_hist, bkg_hist, input_name, mva_name, prefix, out_name, lumi):
	out_dir = input_name
	if OUT_DIRECTORY:
		out_dir = OUT_DIRECTORY

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

	save_canv(canv, prefix + input_name + out_name, out_dir + "_" + mva_name + out_name)

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

	save_canv(canv, prefix + input_name + out_name, out_dir + "_" + mva_name + out_name)

###############################

def evaluate_mlp(sig_hist, bkg_hist, total_sig, total_bkg, input_name, mva_name, prefix, out_name, lumi):
	sig_max = plot_and_get_sig(sig_hist, bkg_hist, input_name, total_sig, total_bkg, mva_name, prefix, out_name, lumi)

	plot_roc_curve(sig_hist, bkg_hist, input_name, sig_max, mva_name, prefix, out_name, lumi)


def plot_roc_curve(sig_hist, bkg_hist, input_name, sig_max, mva_name, prefix, out_name, lumi):
	out_dir = input_name
	if OUT_DIRECTORY:
		out_dir = OUT_DIRECTORY


	roc = get_roc_curve_hist(sig_hist, bkg_hist)

	set_style(roc, kBlack)

	canv = TCanvas("roc", "", 800, 600)

	roc.SetTitle("; sig. eff.; bkg. rej.")

	roc.Draw("a l")

	leg = TLegend(0.2, 0.2, 0.5, 0.4)
	leg.AddEntry(roc, "%s @%s/fb" % (sig_max, lumi), "l")
	leg.Draw("same")

	save_canv(canv, prefix + input_name + out_name, out_dir + "_" + mva_name + out_name)

def plot_and_get_sig(sig_hist, bkg_hist, input_name, total_sig, total_bkg, mva_name, prefix, out_name, lumi):
	out_dir = input_name
	if OUT_DIRECTORY:
		out_dir = OUT_DIRECTORY


	sig = get_sig_hist(sig_hist, bkg_hist, total_sig, total_bkg, lumi)

	set_graph_style(sig, kBlack)

	sig.SetTitle(";%s;significance" % mva_name)

	canv = TCanvas("sig", "", 800, 600)

	sig.Draw("a3")
	sig.Draw("lx")

	index_max = TMath.LocMax(sig.GetN(), sig.GetY())
	sig_max = "%.1f #pm %.1f" % (sig.GetY()[index_max], sig.GetEY()[index_max])

	leg = TLegend(0.2, 0.75, 0.6, 0.9)
	PlotStyle.legend(leg)
	leg.AddEntry(sig, "%s @%s/fb" % (sig_max, lumi) ,"l")
	leg.Draw()

	save_canv(canv, prefix + input_name + out_name, out_dir + "_" + mva_name + out_name)

	return sig_max

###############################

def get_out_name(signals):
	name = ""
	for sig in signals:
		name +=  "_" + sig.name
	return name

def save_mva_hist(sig_mva, bkg_mva, name, mva_name, prefix, out_name):
	directory = "plots/" + name + "_" + mva_name + "/root/"
	if OUT_DIRECTORY:
		directory = "plots/" + OUT_DIRECTORY + "/root/"

	if not os.path.exists(directory):
		os.makedirs(directory)
	
	sig_mva.SaveAs(directory + prefix + out_name + "_sig.root")
	bkg_mva.SaveAs(directory + prefix + out_name + "_bkg.root")


def parse_options():
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument("name", help="the name of the input xml file", default=None, nargs="?")
	parser.add_argument("-s", "--samples", help="configuration file for the input samples", default="samples")
	parser.add_argument("-v", "--variables", help="configuration file for the used variables", default="variables")

	parser.add_argument("-r", "--random-variable", help="a variable which should be replaced by some random distribution for the evaluation", dest="random_var")

	parser.add_argument("-b", "--nbins", help="binning for mlp distribution", type=int, default=50)
	parser.add_argument("--min", help="minimum x-range for mlp distribution", type=float, default=-1.)
	parser.add_argument("--max", help="maximum x-range for mlp distribution", type=float, default=1.)

	parser.add_argument("-l", "--lumi", help="the luminostity in fb^-1 used to calculate the expected significance", type=float, default=30.)

	parser.add_argument("--sig", help="specify specific signal samples", action="append", default=[])

	parser.add_argument("--add-var", help="add an additional variable", action="append", default=[])
	parser.add_argument("--rm-var", help="remove a variable", action="append", default=[])

	parser.add_argument("--directory", help="specify a directory, if you prefer some special naming scheme", default="output")

	opts = parser.parse_args()

	"""
	if opts.sig:
		global SIGNALS
		SIGNALS = {}
		for s in opts.sig:
			SIGNALS[s] = DIRECTORY + "/" + s + "/*.root/" + s + "_Nom"
	"""		

	opts.prefix = ""
	if opts.random_var:
		opts.prefix = opts.random_var + "_"

	return opts

def main():
	opts = parse_options()

	if not opts.name:
		files = [f for f in os.listdir(os.path.join(opts.directory, "weights")) if f.endswith(".weights.xml")]
		files = [(f, os.path.getmtime(os.path.join(opts.directory, "weights", f))) for f in files]
		files.sort(reverse=True, key=itemgetter(1))
		opts.name = files[0][0].replace(".weights.xml", "")
		print "No file specified. Using the newest file '{}' instead".format(opts.name)

	sample_info = getattr(__import__("config." + opts.samples), opts.samples)
	out_name = get_out_name(sample_info.Signal)

	_t = TChain()
	for add_bkg in sample_info.Background:
		_t.Add(add_bkg.tree)
	bkg_tree = _t.CopyTree(sample_info.Preselection)

	_t = TChain()
	for add_sig in sample_info.Signal:
		_t.Add(add_sig.tree)
	sig_tree = _t.CopyTree(sample_info.Preselection)

	variables = config.load_var_list(opts.variables, opts.add_var, opts.rm_var)
	reader, var_store = create_reader(variables, opts.directory, opts.name)

	random_var_hist = None
	rnd_var_index = None
	if opts.random_var:
		bkg_tree.Draw("%s>>random_var_hist" % opts.random_var, "weight * sf_total * xs_weight")
		random_var_hist = gDirectory.Get("random_var_hist")
		remove_negative_entries(random_var_hist)
		random_var_hist.SetDirectory(None)

		rnd_var_index = get_var_index(opts.random_var)

	bkg_mva = evaluate_mva("bkg", bkg_tree, opts.name.split("_")[-1], reader, var_store, opts.nbins, opts.min, opts.max, rnd_var_index, random_var_hist)
	sig_mva = evaluate_mva("sig", sig_tree, opts.name.split("_")[-1], reader, var_store, opts.nbins, opts.min, opts.max, rnd_var_index, random_var_hist)
	save_mva_hist(sig_mva, bkg_mva, "_".join(opts.name.split("_")[:-1]), opts.name.split("_")[-1], opts.prefix, out_name)

	plot_mva_distribution(sig_mva, bkg_mva, "_".join(opts.name.split("_")[:-1]), opts.name.split("_")[-1], opts.prefix, out_name, opts.lumi)

	total_sig = get_total_events([sig_tree], "1", weights="weight * sf_total * xs_weight")
	total_bkg = get_total_events([bkg_tree], "1", weights="weight * sf_total * xs_weight")
	print "total_sig", total_sig
	print "total_bkg", total_bkg

	evaluate_mlp(sig_mva, bkg_mva, total_sig, total_bkg, "_".join(opts.name.split("_")[:-1]), opts.name.split("_")[-1], opts.prefix, out_name, opts.lumi)


###############################

if __name__ == '__main__':
	main()
