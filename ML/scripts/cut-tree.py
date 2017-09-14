#!/usr/bin/env python
import ROOT
import os
import sys
from glob import glob

"""CUT = "(stxe_trigger) &&  \
(n_jet>=4) &&  \
(jet_pt[0]>50000) && (jet_pt[1]>25000) && (jet_pt[2]>25000) && (jet_pt[3]>25000) && \
(mt>30000) &&  \
(met>300e3) &&  \
(n_bjet>0) && \
(dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) &&  \
!((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (dphi_met_lep<2.5)"
"""

CUT = "(dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && (n_jet>=4) && (n_bjet>0) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>60e3) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (met >120e3)"

VARIABLES = [
	"met",
	"mt",
	"n_bjet",
	"dphi_met_lep",
	"amt2",
	"ht",
	"n_jet",
	"lep_pt",
	"jet_pt",
	"bjet_pt",
	"xs_weight",
	"weight",
	"sf_total",
	"weight_sherpa22_njets",
	"event_number",
	# needed for cut
	"dphi_jet0_ptmiss",
	"dphi_jet1_ptmiss",
	"mT2tauLooseTau_GeV"
]

SRC_FOLDER = "/project/etp5/dhandl/samples/SUSY/Stop1L"
SRC = "/project/etp5/dhandl/samples/SUSY/Stop1L/*/*.root"
SRC_IGN = [
	"/project/etp5/dhandl/samples/SUSY/Stop1L/data1?/*.root", 
	"/project/etp5/dhandl/samples/SUSY/Stop1L/*private/*.root"
	"/project/etp5/dhandl/samples/SUSY/Stop1L/TRUTH/*.root",
	"/project/etp5/dhandl/samples/SUSY/Stop1L/ttbar_radHi/*.root",
	"/project/etp5/dhandl/samples/SUSY/Stop1L/ttbar_radLo/*.root"
]
DST = "/scratch-local/fscheinost/cut_data_mt60_met120/"

def filesize(num):
	for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
		if abs(num) < 1024.0:
			return "%3.1f%sB" % (num, unit)
		num /= 1024.0
	return "%.1fYiB" % num

def main():
	if not os.path.isdir(SRC_FOLDER):
		print "No such folder '{}'".format(src)
		return

	if not os.path.isdir(DST):
		print "No such folder '{}'".format(dest)
		return

	src_files = set(glob(SRC))
	for src_ign in SRC_IGN:
		src_files -= set(glob(src_ign))


	print "Going to copy the following files\nfrom\n\t{src}\nto\n\t{dest}\n(without overwriting existing files)\nand applying the following cut:\n\n{cut}\n\n- {files}" \
		.format(src=SRC_FOLDER, dest=DST, files="\n- ".join([os.path.relpath(f, SRC_FOLDER) for f in src_files]), cut=CUT)

	while True:
		i = raw_input("Are you okay with that? (y|n) ").strip().lower()
		if i == "y":
			break
		elif i == "n":
			return

	for f in src_files:
		fSrc, fDest = f, os.path.join(DST, os.path.relpath(f, SRC_FOLDER))

		if not os.path.exists(os.path.dirname(fDest)):
			os.makedirs(os.path.dirname(fDest))
		print fDest

		if os.path.exists(fDest):
			print "Skipping " + f
			continue

		print "Copying '{}'...".format(f),

		f = ROOT.TFile(fSrc)

		# Get all trees in this file
		for name in set([k.GetName() for k in f.GetListOfKeys() if k.GetClassName() == "TTree"]):
			print "\nDEBUG: Copying " + name
			t = f.Get(name)

			if VARIABLES:
				# disable all branches
				t.SetBranchStatus("*", 0)
				branch_list = [b.GetName() for b in t.GetListOfBranches()]
				for var in VARIABLES:
					if var in branch_list:
						# enable only branches in VARIABLES
						t.SetBranchStatus(var, 1)

			# Open destination file for this tree. This is important as otherwise the tree would get written to
			# memory by default when doing CopyTree
			fCopy = ROOT.TFile(fDest, "RECREATE")
			fCopy.cd()

			tCopy = t.CopyTree(CUT)
			tCopy.AutoSave()

		print "OK Saved {}".format(filesize(os.stat(fSrc).st_size - os.stat(fDest).st_size))

	cutInfo = os.path.join(DST, "cut.txt")
	if os.path.exists(cutInfo):
		while True:
			i = raw_input("'{}' exists. Should it be overwritten? (y|n) ".format(cutInfo)).strip().lower()
			if i == "y":
				break
			elif i == "n":
				return

	with open(cutInfo, "w") as f:
		f.write(CUT)

	with open(os.path.join(DST, "variables.txt"), "w") as f:
		f.write("\n".join(VARIABLES))


if __name__ == "__main__":
	main()