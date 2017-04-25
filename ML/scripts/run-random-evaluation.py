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

	parser.add_argument("name", help="the name of the input xml file")
	parser.add_argument("-v", "--variables", help="configuration file for the used variables", default="variables")

	parser.add_argument("-b", "--nbins", help="binning for mlp distribution", type=int, default=50)
	parser.add_argument("--min", help="minimum x-range for mlp distribution", type=float, default=-1.)
	parser.add_argument("--max", help="maximum x-range for mlp distribution", type=float, default=1.)

	parser.add_argument("-l", "--lumi", help="the luminostity in fb^-1 used to calculate the expected significance", type=float, default=30.)

	opts = parser.parse_args()

	return opts

def main():
	opts = parse_options()
	variables = get_var_list("config/{cfg}.py".format(cfg=opts.variables))

	execute_shell("evaluate-mva.py -v {variables} -b {bins} --min {min} --max {max} -l {lumi} {input}".format(
				variables=opts.variables,
				bins=opts.nbins,
				min=opts.min,
				max=opts.max,
				lumi=opts.lumi,
				input=opts.name,
				))

	for var in variables:
		execute_shell("evaluate-mva.py -v {variables} -b {bins} --min {min} --max {max} -l {lumi} -r {random_var} {input}".format(
			variables=opts.variables,
			bins=opts.nbins,
			min=opts.min,
			max=opts.max,
			lumi=opts.lumi,
			random_var=var,
			input=opts.name,
			))
		


###############################

if __name__ == '__main__':
	main()