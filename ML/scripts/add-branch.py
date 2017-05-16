from ROOT import *
import argparse
import os

def tfile(path):
	if not os.path.isfile(path):
		raise argparse.ArgumentTypeError("No such file '{}'".format(path)) 
	return TFile(path)

def parse_options():
  parser = argparse.ArgumentParser()

  parser.add_argument("input_files", metavar="FILE", help="path to an input file", nargs="+", type=tfile)
  parser.add_argument("--tree")
    
  return opts

def main():
	opts = parse_options()

if __name__ == "__main__":
	main()