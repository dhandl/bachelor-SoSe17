#!/usr/bin/env python
#----------------------------------------------------------------------
# File: train.py
# Description: example of classification with TMVA
# Created: 01-Jun-2013 INFN SOS 2013, Vietri sul Mare, Italy, HBP
#          01-Mar-2017 DESY 2017 Statistics School, Hamburg, Germany
#----------------------------------------------------------------------
import os, sys, re
from ROOT import TFile, TMVA, TCut
#----------------------------------------------------------------------
def getTree(filename, treename='Analysis'):
    hfile = TFile(filename)
    if not hfile.IsOpen():
        sys.exit("** can't open file %s" % filename)

    tree = hfile.Get(treename)
    if tree == None:
        sys.exit("** can't find tree %s" % treename)
    return (hfile, tree)
#----------------------------------------------------------------------
def formatOptions(options):
    from string import joinfields, strip, split
    options = joinfields(map(strip, split(strip(options), '\n')), ':')
    return options
#----------------------------------------------------------------------
def main():
    print "\n", "="*80
    print "\tDESY 2017 - classification with TMVA"
    print "="*80

    # summary root file
    summaryFilename = 'TMVA.root'

    # results directory
    resultsDir = 'results'
    os.system('mkdir -p %s' % resultsDir)
    
    #------------------------------------------------------------------
    # get signal file and associated Root tree
    sigFilename = "../public/ntuple_HZZ4L.root"
    sigFile, sigTree = getTree(sigFilename)

    # get background file and associated Root tree
    bkgFilename = "../public/ntuple_ZZ4L.root"
    bkgFile, bkgTree = getTree(bkgFilename)

    #------------------------------------------------------------------
    # create a factory for booking machine learning methods
    #------------------------------------------------------------------
    outputFile = TFile("TMVA.root", "recreate")
    options = '''
    !V
    Color
    !Silent
    DrawProgressBar
    AnalysisType=Classification
    Transformations=I;D
    '''
    factory = TMVA.Factory("Z1massZ2mass", outputFile, formatOptions(options))

    #------------------------------------------------------------------    
    # set up data set for training and testing
    #------------------------------------------------------------------
    dataLoader  = TMVA.DataLoader(resultsDir)
    
    # define variables to be used
    dataLoader.AddVariable("Z1mass", 'D')
    dataLoader.AddVariable("Z2mass", 'D')

    # define from which trees data are to be taken
    # from and the global weights to be assigned to
    # the training data
    sigWeight = 1.0
    dataLoader.AddSignalTree(sigTree, sigWeight)
    dataLoader.SetSignalWeightExpression("weight")
    
    bkgWeight = 1.0
    dataLoader.AddBackgroundTree(bkgTree, bkgWeight)
    dataLoader.SetBackgroundWeightExpression("weight")
    
    # you can apply cuts, if needed
    cut = TCut("")    
    options = '''
    SplitMode=Random
    NormMode=EqualNumEvents
    nTrain_Signal=2500
    nTest_Signal=2500
    nTrain_Background=2500
    nTest_Background=2500
    !V 
    '''
    dataLoader.PrepareTrainingAndTestTree(cut, # signal cut
                                          cut, # background cut
                                          formatOptions(options))

    #------------------------------------------------------------------    
    # ok, almost done, define machine learning methods to be run
    #------------------------------------------------------------------
    
    options = '''
    !H
    !V
    VarTransform=None
    '''
    factory.BookMethod( dataLoader,
                        TMVA.Types.kFisher,
                        "Fisher",
                        formatOptions(options))
    
    options = '''
    !H
    !V
    BoostType=AdaBoost
    NTrees=200
    nEventsMin=100
    nCuts=50
    '''
    factory.BookMethod( dataLoader,
                        TMVA.Types.kBDT,
                        "BDT",
                        formatOptions(options))


    options = '''
    !H
    !V
    NCycles=500
    VarTransform=N
    HiddenLayers=5
    TrainingMethod=BFGS
    '''
    factory.BookMethod( dataLoader,
                        TMVA.Types.kMLP,
                        "MLP",
                        formatOptions(options))    

    #------------------------------------------------------------------
    # ok, let's go!
    #------------------------------------------------------------------    
    factory.TrainAllMethods()  
    factory.TestAllMethods()
    factory.EvaluateAllMethods()
    
    outputFile.Close()
#----------------------------------------------------------------------
try:
    main()
except KeyboardInterrupt:
    print "\nciao"
