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

#DIRECTORY = "/lustre/boerner/swup/stop1l-xaod/export/default_moriond17/"
DIRECTORY = "/project/etp5/dhandl/samples/SUSY/Stop1L/AnalysisChallenge2018/skimmed/"

#PRESELECTION = "(dphi_jet0_ptmiss > 0.4) && (dphi_jet1_ptmiss > 0.4) && (n_jet>=4) && (n_bjet>0) && (jet_pt[0]>50e3) && (jet_pt[1]>25e3) && (jet_pt[2]>25e3) && (jet_pt[3]>25e3) && (mt>30e3) && !((mT2tauLooseTau_GeV > -0.5) && (mT2tauLooseTau_GeV < 80)) && (met>230e3)"
PRESELECTION = "(n_jet>=4) && (n_bjet>0)"


#WEIGHT = "xs_weight * weight * sf_total"
WEIGHT = "event_weight"


###############################

def save_events(name, input_name, events, err):
  #input_name = input_name.replace("_MET100", "")
  directory = "/project/etp5/dhandl/MachineLearning/output/exp_events/"  + name + "/"
  if not os.path.exists(directory):
    os.makedirs(directory)
  file = open(directory + input_name + ".txt", 'w')
  print directory + input_name + ".txt"
  file.write(str(events) +  "+/-" +  str(err))
  file.close()

###############################


def parse_options():
  import argparse
  parser = argparse.ArgumentParser()

  parser.add_argument("-n", "--name", help="the name of the input xml file")
  parser.add_argument("-t", help="the type of the MVA", dest="mva_name", default="BDT")
  parser.add_argument("-v", "--variables", help="configuration file for the used variables", default="variables")

  parser.add_argument("-l", "--lumi", help="the luminostity in fb^-1 used to calculate the expected significance", type=float, default=30.)
  parser.add_argument("-c", "--cut", help="cut which should be applied at the mva distribution", type=float)

  parser.add_argument("input", help="input sample which should be evaluated")

  parser.add_argument("--directory", help="specify a directory, if you prefer some special naming scheme", default="output")

  opts = parser.parse_args()

  return opts

def main():
  opts = parse_options()

  sample = {
    opts.input: DIRECTORY + "/" + opts.input + "*.root/" + "bkgs_Nom"
  }

  tree = load_tree(sample, PRESELECTION)

  variables = load_var_list("config/{cfg}.py".format(cfg=opts.variables))
  reader, var_store = create_reader(variables, opts.directory, opts.name + "_" + opts.mva_name)

  events, err = evaluate_mva_cut(opts.input, tree, opts.mva_name, reader, var_store, opts.cut, opts.lumi)
  save_events(opts.name, opts.input, events, err)

###############################

if __name__ == '__main__':
  main()
