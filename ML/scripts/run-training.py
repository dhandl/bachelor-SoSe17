#!/usr/bin/env python
import sys
import os
import re
from datetime import datetime
from array import array

from collections import namedtuple

from ROOT import *
from Loading import *

Var = namedtuple("Var", "name type")
Sample = namedtuple("Sample", "name tree")

###############################

def create_factory(file_name, name, batch):
	outfile = TFile(file_name, "recreate")
	optString = "!V:!Silent"
	if batch:
		optString += ":!Color:!DrawProgressBar"

	factory = TMVA.Factory(name, outfile, optString)

	return factory, outfile

def set_variables(variables, factory):
	for entry in variables:
		isSpectator = False
		name = entry[0]
		if name.startswith("?"):
			isSpectator = True
			name = name[1:]
		vtype = entry[1]

		if isSpectator:
			factory.AddSpectator(name)
		else:
			factory.AddVariable(name, vtype)

def setup_training(mva_type, mva_name, mva_settings, sample_info, factory, k, i):
	sigCut = sample_info.get("SignalCut", "1.0")
	bkgCut = sample_info.get("BkgCut", "1.0")
	sigCut = TCut(sigCut + " * (" + sample_info['Preselection'] + ")")
	bkgCut = TCut(bkgCut + " * (" + sample_info['Preselection'] + ")")

	train_cut = TCut("(event_number % " + str(k) +  ") != " + str(i))
	test_cut = TCut("(event_number % " + str(k) + ") == " + str(i))

	for entry in sample_info['Signal']:
		print "adding: ", entry.name
		weight = 1.0
		factory.AddTree(entry.tree, "Signal", weight, train_cut, TMVA.Types.kTraining)
		factory.AddTree(entry.tree, "Signal", weight, test_cut, TMVA.Types.kTesting)

	for entry in sample_info['Backgrounds']:
		print "adding: ", entry.name
		weight = 1.0
		factory.AddTree(entry.tree, "Background", weight, train_cut, TMVA.Types.kTraining)
		factory.AddTree(entry.tree, "Background", weight, test_cut, TMVA.Types.kTesting)

	factory.SetWeightExpression(sample_info['Weight'])
	factory.PrepareTrainingAndTestTree(sigCut, bkgCut, "NormMode=NumEvents:!V")

	mva_settings = ":".join(mva_settings) # join the list of settings into a string
	factory.BookMethod(getattr(TMVA.Types, mva_type), mva_name, mva_settings)

def train(factory):
	factory.TrainAllMethods()
	factory.TestAllMethods()
	factory.EvaluateAllMethods()


###############################


def get_opt_id(opt):
	opt_id = opt.replace("!", "") # remove intital !
	if "=" in opt_id:
		opt_id = opt_id.split("=")[0] # take everything in front of =

	return opt_id

def get_setting_index(settings, id):
	for i, opt in enumerate(settings):
		if id == get_opt_id(opt):
			return i

	return -1

def load_mva_settings(file_name, extra_opts, removed_opts):
	infile = open(file_name)

	mtype = "kMLP"
	mname = "MLP"
	msettings = []
	for line in infile:
		line = line.strip()
		if line == "" or line.startswith("#"):
			continue

		if "TYPE" in line:
			parts = line.split(":", 1)
			mtype = parts[1].strip()
		elif "NAME" in line:
			parts = line.split(":", 1)
			mname = parts[1].strip()
		else:
			if ":" in line:
				print "Warning: check the MVA settings", line
			msettings.append(line)

	if extra_opts:
		for opt in extra_opts:
			opt_id = get_opt_id(opt)

			index = get_setting_index(msettings, opt_id)
			if index >= 0:
				del msettings[index]
			msettings.append(opt)

	if removed_opts:
		for opt in removed_opts:
			opt_id = get_opt_id(opt)

			index = get_setting_index(msettings, opt_id)
			if index >= 0:
				del msettings[index]

	return mtype, mname, msettings

def _load_chain(filenames, treename, print_files=False):
	chain = TChain(treename)
	for name in filenames:
		chain.Add(name)

	if print_files:
		for filename in chain.GetListOfFiles():
			print filename.GetTitle()

	return chain

def load_samples(file_name, preselection=None):
	env = {}

	env['load_chain'] = _load_chain
	env['Sample'] = Sample

	execfile(file_name, env)
	if preselection:
		env['Preselection'] = preselection
	return env


###############################

def parse_options():
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument("-n", "--name", help="the name of the output file")
	parser.add_argument("--directory", help="directory where the output is stored")

	parser.add_argument("-s", "--samples", help="configuration file for the input samples", default="samples")
	parser.add_argument("--presel", help="specify a different preselection than in samples.py -- WARNING: will not be propagated through other scrips")
	parser.add_argument("-v", "--variables", help="configuration file for the used variables", default="variables")
	parser.add_argument("--settings", help="configuration file for the training settings", default="mlp_settings")
	parser.add_argument("-m", "--mva-opt", help="additional mva option", action="append", dest="mva_opts")
	parser.add_argument("--rm-mva-opt", help="remove mva option", action="append", dest="rm_mva_opts")

	parser.add_argument("-k", help="used for k-fold -- sum of test and training sets", default=2)
	parser.add_argument("-i", help="used for k-fold -- number of iteration for k-fold", default=1)	

	parser.add_argument("-b", "--batch", help="set to batch mode", action="store_true")

	parser.add_argument("--add-var", help="add an additional variable", action="append")
	parser.add_argument("--rm-var", help="remove a variable", action="append")

	opts = parser.parse_args()


	if not os.path.exists("output"):
		os.makedirs("output")
	if not opts.name:
		opts.name =  datetime.now().strftime("%Y-%m-%d_%H-%M_") + "{smp}_{sett}_{vars}".format(smp=opts.samples, sett=opts.settings, vars=opts.variables) + "_k%d_i%d" % (opts.k, opts.i)
	
	opts.output = "output/" + opts.name + ".root"
	if opts.directory:
		opts.output = os.path.join(opts.directory, opts.name + ".root")
		

	return opts

def main():
	opts = parse_options()

	# load the different configuration files
	variables = load_var_list("config/{cfg}.py".format(cfg=opts.variables), opts.add_var, opts.rm_var)

	mva_type, mva_name, mva_settings = load_mva_settings("config/{cfg}.py".format(cfg=opts.settings), opts.mva_opts, opts.rm_mva_opts)
	presel = None
	if opts.presel:
		presel = opts.presel
	sample_info = load_samples("config/{cfg}.py".format(cfg=opts.samples), preselection=presel)
	print sample_info['Preselection']

	# prepare TMVA and run training
	factory, outfile = create_factory(opts.output, opts.name, opts.batch)
	set_variables(variables, factory)
	setup_training(mva_type, mva_name, mva_settings, sample_info, factory, opts.k, opts.i)
	train(factory)

	outfile.Close()

###############################

if __name__ == '__main__':
	main()
