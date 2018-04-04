#!/usr/bin/env python
import sys
import os

from ROOT import *
gROOT.SetBatch(True)

import PlotStyle
from Style import *
from Loading import *
import Variables

from operator import itemgetter

###############################

def plot_mlp_distribution(train_tree, test_tree, input_name, nbins, min, max, mva_name, output):
	mlp_train_sig, mlp_train_bkg = load_mlp(train_tree, "train", mva_name, nbins, min, max, norm=True)
	mlp_test_sig, mlp_test_bkg = load_mlp(test_tree, "test", mva_name, nbins, min, max, norm=True)

	# save all bdt distributions
	if output:
		try:
			os.makedirs(os.path.join(output, "bdt_dist"))
		except:
			pass
		outfile = TFile(os.path.join(output, "bdt_dist", input_name + ".root"), "recreate")
		outfile.WriteTObject(mlp_test_sig, "mlp_test_sig")
		outfile.WriteTObject(mlp_train_sig, "mlp_train_sig")
		outfile.WriteTObject(mlp_test_bkg, "mlp_test_bkg")
		outfile.WriteTObject(mlp_train_bkg, "mlp_train_bkg")
		outfile.Close()

	set_style(mlp_test_sig, kRed)
	set_style(mlp_train_sig, kRed)

	set_style(mlp_test_bkg, kBlue)
	set_style(mlp_train_bkg, kBlue)

	# plot train and test
	canv = TCanvas("train_test", "", 800, 600)
	mlp_test_bkg.SetTitle("; %s; fraction of events" % mva_name)
	mlp_test_bkg.GetYaxis().SetRangeUser(0, mlp_test_bkg.GetMaximum() * 1.8)

	mlp_test_bkg.Draw("hist")
	mlp_test_sig.Draw("same hist")
	mlp_train_sig.Draw("same p")
	mlp_train_bkg.Draw("same p")

	leg = TLegend(0.2, 0.7, 0.5, 0.9)
	leg.AddEntry(mlp_test_sig, "Signal Test", "f")
	leg.AddEntry(mlp_test_bkg, "Background Test", "f")
	leg.AddEntry(mlp_train_sig, "Signal Train", "pl")
	leg.AddEntry(mlp_train_bkg, "Background Train", "pl")
	leg.Draw("same")

	kolmogorov_bkg = mlp_test_bkg.KolmogorovTest(mlp_train_bkg)
	kolmogorov_sig = mlp_test_sig.KolmogorovTest(mlp_train_sig)
	chi2_bkg = mlp_test_bkg.Chi2Test(mlp_train_bkg, "WW CHI2/NDF")
	chi2_sig = mlp_test_sig.Chi2Test(mlp_train_sig, "WW CHI2/NDF")
	PlotStyle.string(0.65, 0.85, "Kolomogorov Bkg: %1.2f" %kolmogorov_bkg, rel=0.7)
	PlotStyle.string(0.65, 0.8, "Kolomogorov Sig: %1.2f" %kolmogorov_sig, rel=0.7)
	PlotStyle.string(0.65, 0.75, "red. #chi^{2} Bkg: %1.2f" %chi2_bkg, rel=0.7)
	PlotStyle.string(0.65, 0.7, "red. #chi^{2} Sig: %1.2f" %chi2_sig, rel=0.7)


	save_canv(canv, input_name, output)

def plot_eff(train_tree, test_tree, class_name, input_name, nbins, min, max, mva_name):
	if class_name == "sig":
		classID = "classID == 0"
	else:
		classID = "classID == 1"

	eff_test = get_eff(train_tree, "test_" + class_name, mva_name, classID, nbins, min, max)
	eff_val = get_eff(test_tree, "val_" + class_name, mva_name, classID, nbins, min, max)

	set_style(eff_test, kBlack)
	set_style(eff_val, kGreen+2)

	canv = TCanvas("%s_eff" % class_name, "", 800, 600)

	eff_test.SetTitle("; %s cut; %s. eff." % (mva_name, class_name))

	eff_test.Draw("hist")
	eff_val.Draw("same hist")

	leg = TLegend(0.7, 0.8, 0.9, 0.9)
	leg.AddEntry(eff_test, "Train", "l")
	leg.AddEntry(eff_val, "Test", "l")
	leg.Draw("same")

	save_canv(canv, input_name)

def plot_roc_curve(train_tree, test_tree, input_name, sig_train, sig_test, mva_name, lumi, output):
	roc_train = get_roc_curve(train_tree, "train", mva_name)
	roc_test = get_roc_curve(test_tree, "test", mva_name)

	set_style(roc_train, kCyan+2)
	set_style(roc_test, kBlack)

	canv = TCanvas("roc", "", 800, 600)

	roc_test.SetTitle("; sig. eff.; bkg. rej.")

	roc_test.Draw("a l")
	roc_train.Draw("same l")

	leg = TLegend(0.2, 0.2, 0.666666, 0.4)
	leg.AddEntry(roc_train, "Train: %s @%s/fb" % (sig_train, lumi), "l")
	leg.AddEntry(roc_test, "Test: %s @%s/fb" % (sig_test, lumi), "l")
	leg.Draw("same")

	save_canv(canv, input_name, output)


def plot_and_get_sig(train_tree, test_tree, input_name, total_sig, total_bkg, nbins, min, max, mva_name, lumi, output):
	sig_train = get_sig(train_tree, "train", mva_name, total_sig, total_bkg, lumi, nbins, min, max)
	sig_test = get_sig(test_tree, "test", mva_name, total_sig, total_bkg, lumi, nbins, min, max)

	set_graph_style(sig_train, kRed+1)
	set_graph_style(sig_test, kBlack)

	sig_test.SetTitle(";%s;significance" % mva_name)

	canv = TCanvas("sig", "", 800, 600)

	sig_test.Draw("a3")
	sig_train.Draw("3")
	sig_test.Draw("lx")
	sig_train.Draw("lx")

	index_max_train = TMath.LocMax(sig_train.GetN(), sig_train.GetY())
	sig_train_max = (sig_train.GetY()[index_max_train], sig_train.GetEY()[index_max_train])
	index_max_test = TMath.LocMax(sig_test.GetN(), sig_test.GetY())
	sig_test_max = (sig_test.GetY()[index_max_test], sig_test.GetEY()[index_max_test])

	leg = TLegend(0.2, 0.75, 0.6, 0.9)
	PlotStyle.legend(leg)
	leg.AddEntry(sig_train, "Train: %.1f #pm %.1f @%s/fb" % (sig_train_max[0], sig_train_max[1], lumi) ,"l")
	leg.AddEntry(sig_test, "Test: %.1f #pm %.1f @%s/fb" % (sig_test_max[0], sig_test_max[1], lumi) ,"l")
	leg.Draw()

	save_canv(canv, input_name, output)

	return sig_train_max, sig_test_max

def evaluate_mlp(train_tree, test_tree, total_sig, total_bkg, input_name, nbins, min, max, mva_name, lumi, output):
	#plot_eff(train_tree, test_tree, "sig", input_name, nbins, min, max, mva_name)
	#plot_eff(train_tree, test_tree, "bkg", input_name, nbins, min, max, mva_name)

	sig_train, sig_test = plot_and_get_sig(train_tree, test_tree, input_name, total_sig, total_bkg, nbins, min, max, mva_name, lumi, output)

	plot_roc_curve(train_tree, test_tree, input_name, "%.1f #pm %.1f" % sig_train, "%.1f #pm %.1f" % sig_test, mva_name, lumi, output)

	if output:
		data_out = os.path.join(output, "data")
		try:
			os.makedirs(data_out)
		except:
			pass

		outfile = open(os.path.join(data_out, input_name + ".txt"), "w")
		outfile.write("%s\n" % input_name)
		outfile.write("sig_train %f %f\n" % sig_train)
		outfile.write("sig_test %f %f\n" % sig_test)
		outfile.close()

###############################

def plot_and_save(hist, input_name, mva_name):
	rho = hist.GetCorrelationFactor()
	canv = TCanvas("corr_" + hist.GetName(), "", 800, 600)
	PlotStyle.canv_2d(canv, hist)

	hist.Draw("colz")
	PlotStyle.string(.03, .03, "#rho = %.2f" % rho)

	save_canv(canv, input_name, "corr_" + input_name + "_" + mva_name)

	canv.SetLogz()
	canv.Update()
	save_canv(canv, input_name + "_log", "corr_" + input_name + "_" + mva_name)

import re
IndexMatch = re.compile("_(\\d)_$") # '_' + digit + '_' + end-of-string

def get_corr_hist(tree, mva_name, variable, cut, type, mva_binning):
	nutple_varname = variable

	# we would not find "jet_pt_1_" in the variables list,
	# so we transform it to "jet_pt[1]" if it matches the
	# pattern
	match = IndexMatch.search(variable)
	if match:
		nutple_varname = "%s[%s]" % (variable[:-3], match.group(1))

	if nutple_varname in Variables.Variables:
		draw_var = "%s:%s" % (mva_name, Variables.conv_unit(nutple_varname))
		# conv_unit returns jet_pt[1] in the above case, transform it back
		draw_var = draw_var.replace(nutple_varname, variable)

		binning = "(%s,%d,%d,%d)" % (Variables.binning(nutple_varname), mva_binning[0], mva_binning[1], mva_binning[2])

		unit = Variables.unit(nutple_varname)
		if unit and unit != "":
			xtitle = "%s [%s]" % (Variables.title(nutple_varname), unit)
		else:
			xtitle = Variables.title(nutple_varname)
	else:
		draw_var = "%s:%s" % (mva_name, variable)
		binning = ""
		xtitle = variable

	hist_name = variable + "_hist_" + type
	draw_cmd = "%s>>%s%s" % (draw_var, hist_name, binning)

	tree.Draw(draw_cmd, "%s * (mc_weight * sf_total * xs_weight)" % cut)
	hist = gDirectory.Get(hist_name)
	hist.SetDirectory(gROOT)

	hist.SetTitle(";%s;%s output" % (xtitle, mva_name))

	for xbin in xrange(hist.GetNbinsX()+2):
		for ybin in xrange(hist.GetNbinsY()+2):
			if hist.GetBinContent(xbin, ybin) < 0:
				hist.SetBinContent(xbin, ybin, 0)

	return hist

def plot_corr(train_tree, test_tree, input_name, mva_name, mva_binning):
	for b in test_tree.GetListOfBranches():
		if b.GetName() == mva_name:
			continue

		hist_sig = get_corr_hist(test_tree, mva_name, b.GetName(), "(classID == 0)", "sig", mva_binning)
		hist_bkg = get_corr_hist(test_tree, mva_name, b.GetName(), "(classID == 1)", "bkg", mva_binning)
		
		plot_and_save(hist_sig, input_name, mva_name)
		plot_and_save(hist_bkg, input_name, mva_name)


###############################

def parse_options():
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument("name", help="the name of the input file", default=None, nargs="?")
	parser.add_argument("--directory", help="directory where the input file is stored", default="output")
	parser.add_argument("--output", help="give a directory where the output will be stored")

	parser.add_argument("-b", "--nbins", help="binning for mlp distribution", type=int, default=50)
	parser.add_argument("--min", help="minimum x-range for mlp distribution", type=float, default=-1)
	parser.add_argument("--max", help="maximum x-range for mlp distribution", type=float, default=1)
	parser.add_argument("-t", "--title", help="x-axis title for mlp plot", default="BDT", dest="mva_name")

	parser.add_argument("-l", "--lumi", help="the luminostity in fb^-1 used to calculate the expected significance", type=float, default=30.)
	parser.add_argument("--corr", help="plot all the correlations", action="store_true", default=False)

	opts = parser.parse_args()

	opts.mva_binning = (opts.nbins, opts.min, opts.max)

	return opts

def main():
	opts = parse_options()

	if not opts.name:
		files = [f for f in os.listdir(opts.directory) if f.endswith(".root")]
		files = [(f, os.path.getmtime(os.path.join(opts.directory, f))) for f in files]
		files.sort(reverse=True, key=itemgetter(1))
		opts.name = files[0][0].replace(".root", "")
		print "No file specified. Using the newest file '{}' instead".format(opts.name)

	train_tree, test_tree, input_file = load_input(opts.name, opts.directory)

	plot_mlp_distribution(train_tree, test_tree, opts.name, opts.nbins, opts.min, opts.max, opts.mva_name, opts.output)

	total_sig = get_total_events([train_tree, test_tree], "classID == 0")
	total_bkg = get_total_events([train_tree, test_tree], "classID == 1")

	evaluate_mlp(train_tree, test_tree, total_sig, total_bkg, opts.name, opts.nbins, opts.min, opts.max, opts.mva_name, opts.lumi, opts.output)

	if opts.corr:
		plot_corr(train_tree, test_tree, opts.name, opts.mva_name, opts.mva_binning)

###############################

if __name__ == '__main__':
	main()
