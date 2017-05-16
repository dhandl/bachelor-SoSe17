from ROOT import TMVA
from collections import namedtuple

"""
All MVAs should be configured here
The config package provides a method GetAnalysis(name) to get a specific entry
"""

Analysis = namedtuple("Analysis", "type name options")

# Just splits the string and strips each line. 
# This way the opts have the same format (array of one option string) as extra_opts and rm_opts
def _opts(opts_string):
	return [opt.strip() for opt in opts_string.split("\n") if opt.strip()]

analyses = [
	Analysis(TMVA.Types.kMLP, "MLP", 
		[
			"V",
			"!UseRegulator",
			"NeuronType=tanh",
			"VarTransform=N",
			"NCycles=600",
			"HiddenLayers=N+5",
			"TestRate=5",
			"ConvergenceTests=5"
		]
	)
]
