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

# Create histogram

hmva = TH1F("hmva","Test",100,0,1)
hmva2 = TH1F("hmva2","Test",100,0,1)
hmva2.SetLineColor(kRed)

N = tree.GetEntries()

# Loop through tree
for evt in tree:
	# Fill evt/row into variables_ptr to give them to the Reader
	for var in variables_ptr:
		if not var.startswith("?"):
			variables_ptr[var][0] = getattr(evt, var)

	if evt.classID == 0:
		out = reader.EvaluateMVA(analysis_name)
		hmva.Fill(out)
	else:
		hmva2.Fill(reader.EvaluateMVA(analysis_name))

hmva2.DrawNormalized()
hmva.DrawNormalized("same")
raw_input()