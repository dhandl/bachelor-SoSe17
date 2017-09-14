#!/usr/bin/env/ python

import ROOT
import os, copy, sys
import math

_orig_argv = sys.argv[:]
sys.argv = [_orig_argv[0]]

sys.argv = _orig_argv

def getVarList(f):
  var = []
  data = None
  with open(f, "r") as inFile:
    data = inFile.read().splitlines()
  for line in data:
    var.append(line)
  return var

def getVarFromTree(t, var, i=0):
  x = t.GetLeaf(var).GetValue(i)
  return x

def getVarIndex(varStr):
  if "[" and "]" in varStr:
    first = varStr.index("[")
    second = varStr.index("]")
    i = int(varStr[first+1:second])
    var = varStr[:first]
  else:
    var = varStr
    i = 0
  return var, i      

def parse_options():
  import argparse

  parser = argparse.ArgumentParser()
  parser.add_argument("inFile", default="test.root", help="The .root file you want to transform into .dat", type=str)
  parser.add_argument("-v", help=".txt file with variables")
  parser.add_argument("-t", help="Name of the TTree object in the .root file", type=str)
  parser.add_argument("-o", default=str(parser.parse_args().inFile).split(".root")[0]+".dat", help="Name of the output file", type=str)

  opts = parser.parse_args()

  if not opts.v:
    print "No variables file given!"
    sys.exit(1)
  if not opts.inFile:
    print "No input file given"
    sys.exit(1)

  return opts

def main():
  opts = parse_options()

  inFile = opts.inFile
  var = opts.v
  out = opts.o
  t = opts.t

  if not os.path.exists(var):
    print "ERROR: Could not find %s!"%(var)
    sys.exit(1)

  print "Going to transform %s into .dat format!"%(inFile)

  variables = getVarList(var)
  print "Variables to transform:"+" ".join(v for v in variables)
  
  f = ROOT.TFile(inFile)
  tree = f.Get(t)
  n = int(tree.GetEntries())
  outFile = open(out, "w") 

  outFile.writelines(" ".join(v for v in variables) + "\n")
  print "Going to loop over %i events!"%int(n)
  for i in xrange(n):
    if i%1000==0:
      print "At event %i of %i total events!"%(i,n)
    tree.GetEntry(i)
    value = []
    for v in variables:
      j,k = getVarIndex(v)
      value.append(getVarFromTree(tree,j,k))
    outFile.writelines(" ".join(str(val) for val in value) + "\n")

  outFile.close()  

if __name__ == '__main__':
  main()


