#!/usr/bin/env python
import os
from ROOT import *

def get_color(index, total):
	gStyle.SetPalette(kRainBow)
	if total == 1:
		return kBlack
	n_colors = gStyle.GetNumberOfColors()

	return gStyle.GetColorPalette(index * ((n_colors - 1) / (total-1)))

def set_style(hist, color, norm=False):
	hist.SetLineWidth(3)
	hist.SetLineColor(color)
	hist.SetMarkerColor(color)
	hist.SetFillColorAlpha(color, 0.3)

	if norm:
		hist.Scale(1. / hist.Integral())

def set_graph_style(hist, color):
	hist.SetLineWidth(3)
	hist.SetLineColor(color)
	hist.SetMarkerColor(color)
	hist.SetFillColorAlpha(color, 0.2)

OutputTypes = [
	(".pdf", "pdf/"),
	(".root", "root/"),
]

def save_canv(canv, input_name, directory=False):
	name = input_name + "_" + canv.GetName()

	pre_directory = ""
	if directory:
		pre_directory = directory + "/"

	for ext, sub_path in OutputTypes:
		if not os.path.exists("plots/"  + pre_directory +  sub_path):
			try:
				os.makedirs("plots/" + pre_directory +  sub_path)
			except:
				pass

		canv.SaveAs("plots/" + pre_directory +  sub_path + "/" + name + ext)

	canv.SaveAs("plots/" + pre_directory +  name + ".png")

def remove_negative_entries(hist):
	for bin in xrange(0, hist.GetNbinsX()+2):
		if hist.GetBinContent(bin) < 0:
			hist.SetBinContent(bin, 0)