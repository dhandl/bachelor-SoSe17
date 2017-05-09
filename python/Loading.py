#!/usr/bin/env python
from ROOT import *
import re
from array import array
from collections import namedtuple
import math
import os

#############################

def load_input(input_name, directory="output"):
	fileName = directory + "/" + input_name + ".root"
	f = TFile.Open(fileName)

	train_tree = f.Get("output/TrainTree")
	test_tree = f.Get("output/TestTree")

	return train_tree, test_tree, f

def load_tree(input_list, selection):
	src_chain = TChain()

	for name, smp in input_list.iteritems():
		src_chain.Add(smp)
	
	print "copy tree"
	tree = src_chain.CopyTree(selection)

	return tree


#############################

Var = namedtuple("Var", "name type")

def parse_var(var):
	if "$" in var: 
		parts = var.split("$", 1)
		name = parts[0].strip()
		vtype = parts[1].strip()
	else:
		name = var
		vtype = 'F'

	return Var(name, vtype)

def load_var_list(file_name, add_vars=None, rm_vars=None):
	infile = open(file_name)

	all_variables = []
	variables = []

	for line in infile:
		line = line.strip()
		if line == "" or line.startswith("#"):
			continue

		all_variables.append(parse_var(line))

	if add_vars:
		for entry in add_vars:
			var = parse_var(entry)

			if var.name not in [v.name for v in all_variables]:
				all_variables.append(var)

	if rm_vars:
		var_names_to_remove = []
		for entry in rm_vars:
			var = parse_var(entry)
			var_names_to_remove.append(var.name)

		for i, var in enumerate(all_variables):
			if var.name not in var_names_to_remove:
				variables.append(var)
	else:
		variables = all_variables

	return variables


VAR_INDEX_PATTERN = re.compile("(\\w+)\\[(\\d+)\\]")

def get_var_index(var_name):
	var_index = var_name
	match = VAR_INDEX_PATTERN.match(var_name)
	if match:
		container_name = match.groups()[0]
		container_index = int(match.groups()[1])
		var_index = (container_name, container_index)
	return var_index	

def set_variables_reader(variables, reader):
	var_store = {}

	for entry in variables:
		isSpectator = False
		var_name = entry[0]
		if var_name.startswith("?"):
			isSpectator = True
			var_name = var_name[1:]

		if ":=" in var_name:
			tmva_name, var_name = map(lambda s: s.strip(), var_name.split(":="))

		var_index = get_var_index(var_name)

		store = array('f', [0.])

		if isSpectator:
			reader.AddSpectator(var_name, store)
		else:
			reader.AddVariable(var_name, store)

		var_store[var_index] = store

	return var_store

def create_reader(variables, directory, name):
	reader = TMVA.Reader()

	var_store = set_variables_reader(variables, reader)

	file_name = os.path.join(directory, "weights", name + ".weights.xml")
	print "load weights from ", file_name
	reader.BookMVA(name.split("_")[-1], file_name)

	return reader, var_store

#############################

def get_mlp_dist(tree, hist_name, mva_name, cut, nbins, min, max, norm=False):
	hist = TH1F(hist_name, "", nbins, min, max)

	tree.Draw("%s>>%s" % (mva_name, hist_name), "(%s) * (mc_weight * sf_total * xs_weight)" % cut)

	if norm:
		hist.Scale(1. / hist.Integral())

	return hist

def get_total_events(trees, cut, weights = "mc_weight * sf_total * xs_weight"):
	h = TH1F("hxs", "", 1, 0, 2)

	for t in trees:
		t.Draw("1>>+hxs", "(%s) * (%s)" % (cut, weights))

	total_events = h.Integral()
	del h

	return total_events

def load_mlp(tree, prefix, mva_name, nbins, min, max, norm=False):
	sig = get_mlp_dist(tree, prefix + "_mlp_sig", mva_name, "classID == 0", nbins, min, max, norm)
	bkg = get_mlp_dist(tree, prefix + "_mlp_bkg", mva_name, "classID == 1", nbins, min, max, norm)

	return sig, bkg

def get_eff(tree, prefix, mva_name, classID_cut, nbins, min, max):
	hist = get_mlp_dist(tree, prefix + "_mlp", mva_name, classID_cut, nbins, min, max)
	return get_eff_hist(hist, prefix, nbins, min, max)


def get_eff_hist(hist, prefix, nbins, min, max):
	total = hist.Integral()

	eff = TH1F("eff_" + prefix, "", nbins, min, max)
	for bin in xrange(1, hist.GetNbinsX()):
		cut = hist.Integral(bin, hist.GetNbinsX())
		eff.SetBinContent(bin, cut/total)

	return eff

def get_roc_curve(tree, prefix, mva_name):
	sig = get_mlp_dist(tree, prefix + "_mlp_sig", mva_name, "classID == 0", 10000, -1, 2)
	bkg = get_mlp_dist(tree, prefix + "_mlp_bkg", mva_name, "classID == 1", 10000, -1, 2)
	return get_roc_curve_hist(sig, bkg)


def get_roc_curve_hist(hist_sig, hist_bkg):
	total_sig = hist_sig.Integral()
	total_bkg = hist_bkg.Integral()

	roc = TGraph()
	pt = 0
	for bin in xrange(1, hist_sig.GetNbinsX()):
		cut_sig = hist_sig.Integral(bin, hist_sig.GetNbinsX())
		cut_bkg = hist_bkg.Integral(bin, hist_bkg.GetNbinsX())

		roc.SetPoint(pt, cut_sig/total_sig, 1 - cut_bkg/total_bkg)
		pt += 1

	return roc

def get_sig_RooStats(sig_xs, bkg_xs, lumi, bUncert):
	return RooStats.NumberCountingUtils.BinomialExpZ(lumi*sig_xs, lumi*bkg_xs, bUncert)

def get_sig(tree, prefix, mva_name, total_sig, total_bkg, lumi, nbins=50, min=-1, max=1):
	sig_mlp_dist = get_mlp_dist(tree, prefix + "_mlp_sig", mva_name, "classID == 0", nbins, min, max)
	bkg_mlp_dist = get_mlp_dist(tree, prefix + "_mlp_bkg", mva_name, "classID == 1", nbins, min, max)
	return get_sig_hist(sig_mlp_dist, bkg_mlp_dist, total_sig, total_bkg, lumi)


def get_sig_hist(sig_mlp_dist, bkg_mlp_dist, total_sig, total_bkg, lumi):
	total_sig_err = Double()
	total_sig_hist = sig_mlp_dist.IntegralAndError(0, sig_mlp_dist.GetNbinsX()+1, total_sig_err)
	total_bkg_err = Double()
	total_bkg_hist = bkg_mlp_dist.IntegralAndError(0, bkg_mlp_dist.GetNbinsX()+1, total_bkg_err)

	result = TGraphErrors()
	pt = 0

	for bin in xrange(1, sig_mlp_dist.GetNbinsX()):
		cut_sig_err = Double()
		cut_sig = sig_mlp_dist.IntegralAndError(bin, sig_mlp_dist.GetNbinsX(), cut_sig_err)
		cut_bkg_err = Double()
		cut_bkg = bkg_mlp_dist.IntegralAndError(bin, bkg_mlp_dist.GetNbinsX(), cut_bkg_err)

		eff_sig = cut_sig / total_sig_hist
		eff_bkg = cut_bkg / total_bkg_hist

		err_sig = cut_sig_err / total_sig_hist
		err_bkg = cut_bkg_err / total_bkg_hist

		if eff_sig == 0 or eff_bkg == 0:
			Z = 0
			Zerr = 0
		elif err_sig / eff_sig > 0.75 or err_bkg / eff_bkg > 0.75:
			Z = 0
			Zerr = 0
		else:
			Z = get_sig_RooStats(eff_sig * total_sig, eff_bkg * total_bkg, lumi*1000, 0.25)

			Zplus_sig = get_sig_RooStats((eff_sig + err_sig) * total_sig, eff_bkg * total_bkg, lumi*1000, 0.25)
			Zmins_sig = get_sig_RooStats((eff_sig - err_sig) * total_sig, eff_bkg * total_bkg, lumi*1000, 0.25)
			Zplus_bkg = get_sig_RooStats(eff_sig * total_sig, (eff_bkg + err_bkg) * total_bkg, lumi*1000, 0.25)
			Zmins_bkg = get_sig_RooStats(eff_sig * total_sig, (eff_bkg - err_bkg) * total_bkg, lumi*1000, 0.25)

			Zerr_sig = abs(Zplus_sig - Zmins_sig) / 2
			Zerr_bkg = abs(Zplus_bkg - Zmins_bkg) / 2
			Zerr = math.sqrt(Zerr_sig**2 + Zerr_bkg**2)

		result.SetPoint(pt, sig_mlp_dist.GetBinLowEdge(bin), Z)
		result.SetPointError(pt, 0, Zerr)
		pt += 1

	return result

def get_max_sig_error(tree, prefix, mva_name, total_sig, total_bkg, lumi, nbins=50, min=-1, max=1):
	sig = get_sig(tree, prefix, mva_name, total_sig, total_bkg, lumi, nbins, min, max)
	index_max = TMath.LocMax(sig.GetN(), sig.GetY())
	return "%.1f #pm %.1f" % (sig.GetY()[index_max], sig.GetEY()[index_max])

def get_max_sig(tree, prefix, mva_name, total_sig, total_bkg, lumi, nbins=50, min=-1, max=1):
	result = get_sig(tree, prefix, mva_name, total_sig, total_bkg, lumi, nbins, min, max)
	return TMath.MaxElement(result.GetN(), result.GetY())

def get_max_sig_hist(sig_mlp_dist, sig_bkg_dist, total_sig, total_bkg, lumi):
	result = get_sig_hist(sig_mlp_dist, sig_bkg_dist, total_sig, total_bkg, lumi)
	return TMath.MaxElement(result.GetN(), result.GetY())

def get_area(tree, prefix, mva_name):
	roc = get_roc_curve(tree, prefix, mva_name)
	area = roc.Integral()
	return area
