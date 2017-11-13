how to use this TMVA optimisation code:
- specify the input samples in "config/samples.py" (the exported samples from the SWup code can be used without problems, other ntuples may need some changes in the code)
- in "config/variables.py" all interesting variables can be definied which will then be used in the training
--> it's also possible to add here spectators
--> it's important to add the sf_total, xs and mc weight that the scaling can be applied in the training
- in "config/mlp_settings.py" the settings for a mlp can be defined

--> general remark: one can always add new files in the config directory and specify the used samples/variables/settings file via command line
(for the command line options, one can check the different files and see what is already possible, and add missing features)
--> otherwise: one can use specific input files and add/remove variables and settings also via command line

to run the optimisation, call:
- run-training.py 
this should work out of the box, if one uses the same configuration files as mentioned above, otherwise several changes can be done on the command line


for the evaluation of the trained BDT, there are two options
1) plot-training-results.py
- this runs directly on the output files of TMVA (which is very fast) and produce significance plots, the MLP distribution and the roc curves for test and train sample
2) evaluate-mva.py
- this runs on the exported files from SWup
--> possibility to check other signals, other backgrounds...
- produce the same plots as plot-training-results, but without the split into test and train tree
(can be relativly small depending on the size of the studied samples)


more advanced scripts (will be described later in more detail):
- evaluate-kfold (as the name says, it is meant to evaluate the kfold training, is really slow)
- for N-1 tests: run-nminus1-training.py and run-random-evaluation.py
- for exp number of events as needed for HistFitter limits: evaluate-mva-cut.py, get-exp-events.py
- direct comparison of different trainings: compare-training-results (the sorting is performed by finding the setup with the lowest difference between train and test area under roc curve)
