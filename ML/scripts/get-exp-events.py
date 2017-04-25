#!/usr/bin/env python
import sys
import os

from ROOT import *
gROOT.SetBatch(True)

###############################

SAMPLES = [
	"stop_bWN_200_50_MET100",
	#"stop_bWN_225_75_MET100",
	"stop_bWN_250_100_MET100",
	"stop_bWN_250_130_MET100",
	"stop_bWN_250_160_MET100",
	"stop_bWN_300_150_MET100",
	"stop_bWN_300_180_MET100",
	"stop_bWN_300_210_MET100",
	"stop_bWN_350_200_MET100",
	"stop_bWN_350_230_MET100",
	"stop_bWN_350_260_MET100",
	"stop_bWN_400_250_MET100",
	"stop_bWN_400_280_MET100",
	"stop_bWN_400_310_MET100",
	"stop_bWN_450_300_MET100",
	"stop_bWN_450_330_MET100",
	"stop_bWN_450_360_MET100",
	"stop_bWN_500_350_MET100",
	"stop_bWN_500_380_MET100",
	"stop_bWN_500_410_MET100",
	"stop_bWN_550_400_MET100",
	"stop_bWN_550_430_MET100",
	"stop_bWN_550_460_MET100",
	"stop_bWN_600_450_MET100",
	"stop_bWN_600_480_MET100",
	"stop_bWN_600_510_MET100",
	"stop_bWN_650_500_MET100",
	"stop_bWN_650_530_MET100",
	"stop_bWN_650_560_MET100",
	#"madgraph_ttV",
	#"powheg_singletop",
	#"powheg_ttbar",
	#"sherpa22_Wjets",
	#"sherpa_diboson",
	#"stop_tN_200_12",
	#"stop_tN_200_27",
	#"stop_tN_250_62",
	#"stop_tN_250_77",
	#"stop_tN_300_112",
	#"stop_tN_300_127",
	#"stop_tN_350_150",
	#"stop_tN_350_162",
	#"stop_tN_350_177",
	#"stop_tN_400_175",
	#"stop_tN_400_200",
	#"stop_tN_400_212",
	#"stop_tN_400_227",
	#"stop_tN_450_262",
	#"stop_tN_450_277",
	#"stop_tN_500_312",
	#"stop_tN_500_327",
	#"stop_tN_550_362",
	#"stop_tN_550_377",
	#"stop_tN_600_300",
	#"stop_tN_600_412",
	#"stop_tN_600_427",
	#"stop_tN_650_462",
	#"stop_tN_650_477",
]

###############################

def execute_shell(cmd):
	print cmd
	os.system(cmd)

###############################

def parse_options():
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument("-n", "--name", help="the name of the input xml file")
	parser.add_argument("-t", help="the type of the MVA", dest="mva_name", default="BDT")
	parser.add_argument("-v", "--variables", help="configuration file for the used variables", default="variables")

	parser.add_argument("-l", "--lumi", help="the luminostity in fb^-1 used to calculate the expected significance", type=float, default=30.)
	parser.add_argument("-c", "--cut", help="cut which should be applied at the mva distribution", type=float)

	opts = parser.parse_args()

	return opts

def main():
	opts = parse_options()

	for smp in SAMPLES:
		execute_shell("evaluate-mva-cut.py -n {name} -t {mva_name} -v {variables} -l {lumi} -c {cut} {sample}".format(
			name = opts.name,
			mva_name = opts.mva_name,
			variables = opts.variables,
			lumi = opts.lumi,
			cut = opts.cut,
			sample = smp,
			))


###############################

if __name__ == '__main__':
	main()