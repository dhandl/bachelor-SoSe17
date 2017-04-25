#!/usr/bin/env python
import sys
import os

from ROOT import *
gROOT.SetBatch(True)

import PlotStyle
from Style import *
from Loading import *

###############################
def get_sig_from_tuple(tup):
    return tup[2]

def compare_results(tree_test, tree_train, lumi, mva_names, out_name, total_sig_events, total_bkg_events, max_lines):
	roc_dict = {}
	for name, tree in tree_test.iteritems():
		mva_name = mva_names[name]
		roc = get_roc_curve(tree, name, mva_name)
		roc_dict[name] = roc

	rocs = roc_dict.values()

	canv = TCanvas("comparison_roc", "", 800, 600)
	leg = TLegend(0.17, 0.17, 0.62, 0.6)
	PlotStyle.legend(leg)

	sortedRocs = []
	for name, roc in roc_dict.iteritems():
		max_sig = get_max_sig(tree_test[name], name, mva_names[name], total_sig_events[name], total_bkg_events[name], lumi)
		max_sig_train = get_max_sig(tree_train[name], name, mva_names[name], total_sig_events[name], total_bkg_events[name], lumi)
		#sig_diff = abs(max_sig - max_sig_train)
		area_test = get_area(tree_test[name], name, mva_names[name])
		area_train = get_area(tree_train[name], name, mva_names[name])
		diff_area = abs(area_test - area_train)
		print name, area_test, area_train, diff_area, max_sig, max_sig_train

		max_sig_error_string = get_max_sig_error(tree_test[name], name, mva_names[name], total_sig_events[name], total_bkg_events[name], lumi)
		sortedRocs.append((roc, name, diff_area, max_sig_error_string))

	sortedRocs.sort(key=get_sig_from_tuple)		
	
	if max_lines > len(sortedRocs):
		max_lines = len(sortedRocs)

	set_graph_style(sortedRocs[0][0], get_color(0, max_lines))
	sortedRocs[0][0].SetTitle("; sig. eff.; bkg. rej.")

	sortedRocs[0][0].Draw("a l")
	leg.AddEntry(sortedRocs[0][0], "%s: %s %s/fb" % (sortedRocs[0][1], sortedRocs[0][3], lumi), "l")

	index = 1
	for r in sortedRocs[1:max_lines]:
		set_graph_style(r[0], get_color(index, max_lines))

		r[0].Draw("same l")
		leg.AddEntry(r[0], "%s: %s %s/fb" % (r[1], r[3], lumi), "l")
		index += 1	

	leg.Draw()

	save_canv(canv, out_name)	 


###############################

def parse_options():
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument("-l", "--lumi", help="the luminostity in fb^-1 used to calculate the expected significance", type=float, default=30.)
	parser.add_argument("-m", "--max-lines", dest="max_lines", type=int, default=10, help="the number of lines and signficances given in the plot (only the best results are shown when more were analysed)") 
	parser.add_argument("-n", "--name", help="name for the output plot")
	parser.add_argument("input_files", help="name of the input files", nargs="+")

	opts = parser.parse_args()

	print opts.input_files

	for inp in opts.input_files:
		if ":" not in inp:
			print "Error: an input file is given without the method name: ", inp
			sys.exit(0)

	return opts

def main():
	opts = parse_options()

	tree_test = {}
	tree_train = {}
	total_sig_events = {}
	total_bkg_events = {}
	mva_names = {}
	_input_file_list = []
	output_name = ""
	for inp in opts.input_files:
		inp_name, mva_name = inp.split(":")
		train_tree, test_tree, input_file = load_input(inp_name)
		_input_file_list.append(input_file)
		tree_test[inp_name] = test_tree
		tree_train[inp_name] = train_tree
				
		total_sig_events[inp_name] = get_total_events([train_tree, test_tree], "classID == 0")
		total_bkg_events[inp_name] = get_total_events([train_tree, test_tree], "classID == 1")

		if output_name == "":
			output_name += inp_name
		else:
			output_name += "_" + inp_name
		mva_names[inp_name] = mva_name

	if opts.name:
		output_name = opts.name

	compare_results(tree_test, tree_train, opts.lumi, mva_names, output_name, total_sig_events, total_bkg_events, opts.max_lines)


###############################

if __name__ == '__main__':
	main()
