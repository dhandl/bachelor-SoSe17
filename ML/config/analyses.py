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
      "H",
      "!V",
      "NeuronType=tanh",
      "VarTransform=N",
      "NCycles=600",
      "HiddenLayers=N+5",
      #"LearningRate=1",
      #"DecayRate=0.001",
			#"!H",
      #"!V",
      #"EstimatorType=CE",
      #"NeuronInputType=sqsum",
      #"TrainingMethod=BP",
      #"BPMode=batch",
      #"BatchSize=128"
      "TestRate=5",
			#"ConvergenceTests=10",
      #"ConvergenceImprove=1e-5",
      #"CreateMVAPdfs=True",
      #"CalculateErrors=True",
      "!UseRegulator",
      "Sampling=0.75",
      #"SamplingEpoch=1",
      "SamplingImportance=0.75"
		]
	),
  #Analysis(TMVA.Types.kBDT, "BDT",
  #  [
  #  '!H','!V',
  #  'NTrees=850',
  #  'MinNodeSize=2.5%',
  #  'MaxDepth=3',
  #  'BoostType=AdaBoost',
  #  'AdaBoostBeta=0.5',
  #  'UseBaggedBoost',
  #  'BaggedSampleFraction=0.5',
  #  'SeparationType=GiniIndex',
  #  'nCuts=20'
  #  ]
  #),
  Analysis(TMVA.Types.kBDT, "BDT",
    [
    "H","!V",
    "NTrees=500",
    "MinNodeSize=2.5%",
    "BoostType=Grad",
    "Shrinkage=0.1",
    "UseBaggedGrad=True",
    "BaggedSampleFraction=0.5",
    "nCuts=20",
    "MaxDepth=2",
    "DoBoostMonitor=True",
    "NegWeightTreatment=Pray"
    ]
  ),
  Analysis(TMVA.Types.kCuts, "Cuts",
    [
    "!H",
    "!V",
    "VarTransform=None",
    "FitMethod=GA",
    "EffSel",
    #"SampleSize=200000",
    "VarProp=NotEnforced",
    "CutRangeMin=-1",
    "CutRangeMax=-1"
    ]
  ),
  Analysis(TMVA.Types.kLikelihood, "Likelihood",
    [
    "H",
    "!V",
    "TransformOutput",
    "PDFInterpol=Spline2",
    "NSmoothSig[0]=20",
    "NSmoothBkg[0]=20",
    "NSmoothBkg[1]=10",
    "NSmooth=1",
    "NAvEvtPerBin=50"
    ]
  ),
  Analysis(TMVA.Types.kFisher, "Fisher",
    [
    "H",
    "!V",
    "Fisher",
    "VarTransform=None",
    "CreateMVAPdfs",
    "PDFInterpolMVAPdf=Spline2",
    "NbinsMVAPdf=50",
    "NsmoothMVAPdf=10"
    ]
  ),
  Analysis(TMVA.Types.kDNN, "DNN",
    [
      "!H",
      "V",
      "ErrorStrategy=CROSSENTROPY",
      "VarTransform=None",
      "WeightInitialization=XAVIERUNIFORM",
      "Layout=TANH|20,LINEAR",
      "TrainingStrategy=LearningRate=1e-1,ConvergenceSteps=50,TestRepetitions=5,Regularization=NONE"
      #|LearningRate=1e-2,Momentum=0.5,Repetitions=1,ConvergenceSteps=300,BatchSize=30,TestRepetitions=7,WeightDecay=0.001,Regularization=L2,DropConfig=0.0+0.1+0.1+0.1,DropRepetitions=1|LearningRate=1e-2,Momentum=0.3,Repetitions=1,ConvergenceSteps=300,BatchSize=40,TestRepetitions=7,WeightDecay=0.0001,Regularization=L2|LearningRate=1e-3,Momentum=0.1,Repetitions=1,ConvergenceSteps=200,BatchSize=70,TestRepetitions=7,WeightDecay=0.0001,Regularization=NONE",
      #TrainingStrategy: "LearningRate=1e-1,Momentum=0.3,Repetitions=3,ConvergenceSteps=50,BatchSize=30,TestRepetitions=7,WeightDecay=0.0,Renormalize=L2,DropConfig=0.0,DropRepetitions=5|LearningRate=1e-4,Momentum=0.3,Repetitions=3,ConvergenceSteps=50,BatchSize=20,TestRepetitions=7,WeightDecay=0.001,Renormalize=L2,DropConfig=0.0+0.5+0.5,DropRepetitions=5,Multithreading=True"
    ]
  )
]
