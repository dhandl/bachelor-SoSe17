#!/usr/bin/env python
from ROOT import *

#############################

def eval_event(tree, reader, var_store, mva_name, random_var=None, random_var_hist=None):
	for var in var_store.keys():
		if type(var) == str: # this is the easy case (-;
			var_store[var][0] = getattr(tree, var)
		else:
			array_name, index = var
			array = getattr(tree, array_name)
			var_store[var][0] = array[index]
			
	if random_var:
		var_store[random_var][0] = random_var_hist.GetRandom()

	return reader.EvaluateMVA(mva_name)

def evaluate_mva(name, tree, mva_name, reader, var_store, nbins, nmin, nmax, random_var=None, random_var_hist=None):
	hist = TH1F(mva_name + "_" + name, "", nbins, nmin, nmax)

	for i in xrange(tree.GetEntries()):
		tree.GetEntry(i)

		mlp = eval_event(tree, reader, var_store, mva_name, random_var, random_var_hist)

		hist.Fill(mlp, tree.weight * tree.sf_total * tree.xs_weight)

	return hist

def evaluate_mva_cut(name, tree, mva_name, reader, var_store, cut, lumi):
	hist = TH1F("dummy_" + name + mva_name, "", 1, 0, 2)
	for i in xrange(tree.GetEntries()):
		tree.GetEntry(i)
		mlp = eval_event(tree, reader, var_store, mva_name)

		if mlp >= cut:
			hist.Fill(1, tree.weight * tree.sf_total * tree.xs_weight * lumi * 1000)

	return hist.GetBinContent(1), hist.GetBinError(1)


def evaluate_mva_k_fold(name, tree, mva_name, reader_list, var_store_list, nbins, nmin, nmax, k_fold):
	hist = TH1F(mva_name + "_" + name, "", nbins, nmin, nmax)

	for i in xrange(tree.GetEntries()):
		tree.GetEntry(i)

		mlp = 0
		for iteration in xrange(0, k_fold):
			mlp += eval_event(tree, reader_list[iteration], var_store_list[iteration], mva_name)
		mlp /= (1.0 * k_fold)

		hist.Fill(mlp, tree.weight * tree.sf_total * tree.xs_weight)

	return hist

def evaluate_mva_k_fold_test_train(name, tree, mva_name, reader_list, var_store_list, nbins, nmin, nmax, k_fold):
	test = TH1F("test_" + mva_name + "_" + name, "", nbins, nmin, nmax)
	train = TH1F("train_" + mva_name + "_" + name, "", nbins, nmin, nmax)

	for i in xrange(tree.GetEntries()):
		tree.GetEntry(i)

		mlp_test = 0
		mlp_train = 0
		for iteration in xrange(k_fold):
			mlp = eval_event(tree, reader_list[iteration], var_store_list[iteration], mva_name)

			if tree.event_number % k_fold == iteration:
				mlp_test = mlp
			else:
				mlp_train += mlp

		mlp_train /= (1.0 * (k_fold-1.0))

		test.Fill(mlp_test, tree.weight * tree.sf_total * tree.xs_weight)
		train.Fill(mlp_train, tree.weight * tree.sf_total * tree.xs_weight)

	return test, train
