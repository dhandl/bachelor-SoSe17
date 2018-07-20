#!/usr/bin/env python
import os
from datetime import datetime
from ROOT import *
import config

###############################

def create_factory(file_name, name, directory, batch):
  outfile = TFile(file_name, "recreate")

  optString = "!V:!Silent"
  if batch:
    optString += ":!Color:!DrawProgressBar"

  factory = TMVA.Factory(name, outfile, optString)

  # recent TMVA releases requires a dataLoader!
  loader = TMVA.DataLoader(directory)

  return factory, outfile, loader


def set_variables(variables, loader):
  for entry in variables:
    isSpectator = False
    name = entry[0]
    if name.startswith("?"):
      isSpectator = True
      name = name[1:]

    vtype = entry[1]

    if isSpectator:
      loader.AddSpectator(name)
    else:
      loader.AddVariable(name, vtype)


def setup_training(mva_type, mva_name, mva_settings, sample_info, factory, loader, k, i):
  sigCut = getattr(sample_info, "SignalCut", "1.0")
  bkgCut = getattr(sample_info, "BkgCut", "1.0")
  sigCut = TCut(sigCut + " * (" + sample_info.Preselection + ")")
  bkgCut = TCut(bkgCut + " * (" + sample_info.Preselection + ")")

  train_cut = TCut("((event_number % " + str(k) +  ") != " + str(i) + ") && (" + sample_info.Preselection + ")")
  test_cut = TCut("((event_number % " + str(k) + ") == " + str(i) + ") && (" + sample_info.Preselection + ")")

  for entry in sample_info.Signal:
    print "adding: ", entry.name
    weight = 1.0
    loader.AddTree(entry.tree, "Signal", weight, train_cut, TMVA.Types.kTraining)
    loader.AddTree(entry.tree, "Signal", weight, test_cut, TMVA.Types.kTesting)

  for entry in sample_info.Background:
    print "adding: ", entry.name
    weight = 1.0
    loader.AddTree(entry.tree, "Background", weight, train_cut, TMVA.Types.kTraining)
    loader.AddTree(entry.tree, "Background", weight, test_cut, TMVA.Types.kTesting)

  loader.SetWeightExpression(sample_info.Weight)
  #loader.PrepareTrainingAndTestTree(sigCut, bkgCut, "nTrain_Signal=25000:nTrain_Background=25000:NormMode=NumEvents:!V")
  loader.PrepareTrainingAndTestTree(sigCut, bkgCut, "NormMode=NumEvents:!V")

  factory.BookMethod(loader, mva_type, mva_name, mva_settings)


def train(factory):
  factory.TrainAllMethods()
  factory.TestAllMethods()
  factory.EvaluateAllMethods()


def parse_options():
  import argparse
  parser = argparse.ArgumentParser()

  parser.add_argument("-n", "--name", help="the name of the output file")
  parser.add_argument("--directory", help="directory where the output is stored", default="output")

  parser.add_argument("--analysis", help="name of the analysis to run (see config/analyses.py)", default="MLP")
  parser.add_argument("-s", "--samples", help="configuration file for the input samples", default="samples")
  parser.add_argument("-v", "--variables", help="configuration file for the used variables", default="variables")

  parser.add_argument("--presel", help="specify a different preselection than in samples.py -- WARNING: will not be propagated through other scrips")
  parser.add_argument("-m", "--mva-opt", help="additional mva option", action="append", dest="mva_opts", default=[])
  parser.add_argument("--rm-mva-opt", help="remove mva option", action="append", dest="rm_mva_opts", default=[])

  parser.add_argument("-k", help="used for k-fold -- sum of test and training sets", default=2)
  parser.add_argument("-i", help="used for k-fold -- number of iteration for k-fold", default=1)  

  parser.add_argument("-b", "--batch", help="set to batch mode", action="store_true")

  parser.add_argument("--add-var", help="add an additional variable", action="append", default=[])
  parser.add_argument("--rm-var", help="remove a variable", action="append", default=[])

  opts = parser.parse_args()

  if not os.path.exists(opts.directory):
    os.makedirs(opts.directory)

  if not opts.name:
    opts.name =  datetime.now().strftime("%Y-%m-%d_%H-%M_") + "{smp}_{sett}_{vars}".format(smp=opts.samples, sett=opts.analysis, vars=opts.variables) + "_k%d_i%d" % (opts.k, opts.i)
  
  opts.output = "output/" + opts.name + ".root"
  if opts.directory:
    opts.output = os.path.join(opts.directory, opts.name + ".root")
    
  return opts

def main():
  opts = parse_options()

  # load the different configuration files
  variables = config.load_var_list(opts.variables, opts.add_var, opts.rm_var)

  mva_type, mva_name, mva_settings = config.get_mva(opts.analysis, opts.mva_opts, opts.rm_mva_opts)

  sample_info = getattr(__import__("config." + opts.samples), opts.samples)
  if opts.presel:
    sample_info.Preselection = opts.presel
  print sample_info.Preselection + "\n"

  # prepare TMVA and run training
  factory, outfile, loader = create_factory(opts.output, opts.name, opts.directory, opts.batch)
  set_variables(variables, loader)

  setup_training(mva_type, mva_name, mva_settings, sample_info, factory, loader, opts.k, opts.i)
  train(factory)

  outfile.Close()

###############################

if __name__ == '__main__':
  main()
