#!/usr/bin/env python
import sys
import os

from ROOT import *
gROOT.SetBatch(True)

###############################

def get_var_list(file_name):
	infile = open(file_name)

	variables = []

	for line in infile:
		line = line.strip()
		if line == "" or line.startswith("#") or line.startswith("?"):
			continue

		if "$" in line: 
			parts = line.split("$", 1)
			name = parts[0].strip()
		else:
			name = line

		variables.append(name)

	return variables

def execute_shell(cmd):
	print cmd
	os.system(cmd)

###############################

def parse_options():
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument("-s", "--samples", help="configuration file for the input samples", default="samples")
	parser.add_argument("-v", "--variables", help="configuration file for the used variables", default="variables")
	parser.add_argument("--settings", help="configuration file for the training settings", default="mlp_settings")
	parser.add_argument("-n", "--name", help="specfiy a detailed name for the output")
	
	parser.add_argument("-k", help="used for k-fold -- sum of test and training sets", default=2)
	parser.add_argument("-i", help="used for k-fold -- number of iteration for k-fold", default=1)	

	parser.add_argument("--eval", help="use this to enable the evaluation of the N-1 trainings", action="store_true")
	parser.add_argument("--compare", help="compare the results in one plot", action="store_true")
	parser.add_argument("-t", help="name of the MVA method used", default="BDT", dest="mva_name")

	opts = parser.parse_args()

	return opts

def main():
	opts = parse_options()
	variables = get_var_list("config/{cfg}.py".format(cfg=opts.variables))


	list_for_comparison = ""
	dir_name = opts.settings
	for var in variables:
		output_name = opts.settings + "_rm_var_" + var
		if opts.name:
			output_name = opts.name + "_rm_var_" + var
			dir_name = opts.name


		if opts.eval:
			execute_shell("evaluate-mva.py {xml_name} -v {variables} --rm-var {rm_var} --directory {directory}".format(
				xml_name = output_name + "_" + opts.mva_name,
				variables = opts.variables,
				rm_var = var,
				directory = dir_name + "_" + opts.mva_name,
				))
		elif opts.compare:
			list_for_comparison += output_name + ":" + opts.mva_name + " "
		else:
			execute_shell("./batch-submit.sh {submit_name} -n {name} -s {samples} -v {variables} --settings {settings} -k {k_fold} -i {iteration} --rm-var {rm_var}".format(
				submit_name = "training_" + output_name,
				name = output_name,
				samples = opts.samples,
				variables = opts.variables,
				settings = opts.settings,
				k_fold = opts.k,
				iteration = opts.i,
				rm_var = var,
				))

	if opts.compare:
		execute_shell("compare-training-results.py {input_list} -n comparison_n_minus_1".format(
			input_list = list_for_comparison
			))
			



###############################

if __name__ == '__main__':
	main()