from ROOT import *
import config
import os
from array import array

# Config (==> argparse in the future)
analysis_name = "MLP"
sample_conf = "samples"
variables_conf = "variables"

# Filenames
filename = "/filer/z-sv-pool01/f/Felix.Scheinost/bachelor-SoSe17/ML/output/2017-05-09_13-35_samples_MLP_variables_k2_i1.root"
weight_file = os.path.join(os.path.dirname(filename), "weights", os.path.basename(filename).replace(".root", "_" + analysis_name + ".weights.xml"))

# Prepare reader
reader = TMVA.Reader()

variables = config.load_var_list(variables_conf)
variables_ptr = {}
for var in variables:
	# TODO: Don't assume datatype
	if var.name.startswith("?"):
		name = var.name.replace("?", "")
		variables_ptr[var.name] = array("f", [0])
		reader.AddSpectator(name, variables_ptr[var.name])
	else:
		variables_ptr[var.name] = array("f", [0])
		reader.AddVariable(var.name, variables_ptr[var.name])

reader.BookMVA(analysis_name, weight_file)

# Get Test tree
f = TFile(filename)
tree = f.Get("output/TestTree")


# save MLP response for all events
sigEvts, bkgEvts = [], []

for evt in tree:
	# Fill evt/row into variables_ptr to give them to the Reader
	for var in variables_ptr:
		if not var.startswith("?"):
			variables_ptr[var][0] = getattr(evt, var)


	if evt.classID == 0:
		sigEvts.append(reader.EvaluateMVA(analysis_name))
	else:
		bkgEvts.append(reader.EvaluateMVA(analysis_name))

sigEvts.sort()
bkgEvts.sort()

# calculate sigEff if we were to cut at this event
for i in xrange(len(sigEvts)):
	# sigEff = TP/ALL_SIG = num_this_and_higher_output/len(sigEvts)
	# = (len(sigEvts) - i) / len(sigEvts) = 1 - i/len(sigEvts)
	sigEvts[i] = (sigEvts[i], 1 - float(i)/len(sigEvts))

# Create histogram
nBins = 1000
hmva = TH2F("hmva","Test",nBins,0,1, nBins, 0, 1)
#hmva.SetMarkerStyle(21)

for i in xrange(nBins):
	# Looking to fill i'th bin -> find out bin value -> signal efficiency we are looking to calculate corresponding background rejection
	signalEfficiency = float(i)/nBins
	print "Looking for cut for signalEfficiency of " + str(signalEfficiency)

	# search for cut to achieve this signal efficiency
	for i in xrange(len(sigEvts)):
		cut, thisSigEff = sigEvts[i]
		nSig = len(sigEvts) - i
		if thisSigEff < signalEfficiency:
			print "Found cut " + str(cut)
			break

	if not cut:
		print "Error found no cut"
		continue

	for i in xrange(len(bkgEvts)):
		if bkgEvts[i] > cut:
			backgroundRej = float(i)/len(bkgEvts)

			print "This cut classifies {} of {} signal events as signal and {} of {} background events as background".format(nSig, len(sigEvts), i, len(bkgEvts))
			print "background rej " + str(backgroundRej)
			break

	hmva.Fill(signalEfficiency, backgroundRej)



hmva.Draw()
raw_input()