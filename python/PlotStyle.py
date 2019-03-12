import os
from ROOT import *

gROOT.SetBatch(True)

# this style is initialized below
Style = TStyle("SWup","Modified ATLAS style")

TitleEvents = "Events"
TitleNorm = "Event fraction"

TotalSM = "Total SM"
DataMCRatio = "Data / SM"


YMaxFactorLin = 1.3
YMaxFactorLog = 10

ChannelString = {
	'mu': "Muon channel",
	'el': "Electron channel",
}

LineSpacing = 0.05

FirstLine = 0.87
SecondLine = FirstLine - LineSpacing
ThirdLine = SecondLine - LineSpacing
FourthLine = ThirdLine - LineSpacing
FifthLine = FourthLine - LineSpacing
SixthLine = FifthLine - LineSpacing

Colors = [
	kBlack,
	kRed,
	kBlue,
	kGreen+1,
	kOrange,

	kGray+3,
	kRed-3,
	kBlue-3,
	kGreen-6,
	kOrange-3,

	kGray,
	kMagenta+2,
	kCyan,
	kSpring+10,
	kOrange+10,

	kViolet-3,
	kOrange-9,
	kTeal+3,
	kPink+10,
]

Left = 0.18

OBJECTS = []

def legend(leg, font_size=0.05):
	leg.SetFillStyle(0)
	leg.SetFillColorAlpha(0, 0.01)
	leg.SetLineColorAlpha(0, 0.01)
	leg.SetBorderSize(1)
	leg.SetTextFont(42)
	leg.SetTextSize(font_size)

def single_hist(hist):
	hist.SetLineColor(kBlack)
	hist.SetLineWidth(3)
	hist.SetFillColor(kGray)

def comp_hist(hist, color=None):
	hist.SetLineWidth(3)
	if color is not None:
		hist.SetLineColor(color)

def stack_hist(hist, color):
	hist.SetLineColor(kBlack)
	hist.SetLineWidth(1)
	hist.SetFillColor(color)

def overlay_hist(hist, color):
	hist.SetLineColor(color)
	hist.SetLineWidth(3)
	hist.SetLineStyle(9)

def data_hist(hist):
	hist.SetMarkerStyle(20)
	hist.SetMarkerSize(1.2)
	hist.SetMarkerColor(kBlack)
	hist.SetLineColor(kBlack)
	hist.SetLineWidth(2)

def mc_total_hist(hist):
	hist.SetMarkerSize(0)
	hist.SetLineColor(kRed)
	hist.SetLineWidth(2)
	hist.SetFillColor(kBlack)
	hist.SetFillStyle(3004)

def ratio_ref(hist, stat_only=True):
	hist.SetMarkerSize(0)
	hist.SetFillColor(kBlack)
	hist.SetFillStyle(3004)

def profile(prof):
	prof.SetMarkerStyle(21)

	prof.SetMarkerColor(kBlack)
	prof.SetLineColor(kBlack)

	prof.SetMarkerSize(1.5)
	prof.SetLineWidth(2)

def ratio_line(line):
	line.SetLineColor(kBlack)
	line.SetLineWidth(1)
	line.SetLineStyle(kDashed)

def ratio_line_total(line):
	line.SetLineColor(kRed)
	line.SetLineWidth(3)

def marker_line(line):
	line.SetLineColor(kBlue)
	line.SetLineWidth(3)

def color_line(line, color, width=3):
	line.SetLineColor(color)
	line.SetLineWidth(3)

def get_color(index, total):
	if index < len(Colors):
		return Colors[index]
	return kBlack

	gStyle.SetPalette(kRainBow)
	if total == 1:
		return kBlack
	n_colors = gStyle.GetNumberOfColors()
	return gStyle.GetColorPalette(index * ((n_colors - 1) / (total-1)))


def atlas(text, x=0.19, y=FirstLine, text_offset=0.13, rel=.8):
	atl_str = TLatex(x, y, "ATLAS")
	atl_str.SetNDC()
	atl_str.SetName("atlas_str")
	atl_str.SetTextFont(72)
	atl_str.SetTextSize(rel * atl_str.GetTextSize())

	atl_str.Draw("same")
	global OBJECTS
	OBJECTS.append(atl_str)

	if text:
		add_str = TLatex(x+text_offset, y, text)
		add_str.SetNDC()
		add_str.SetName("atlas_add_str")
		add_str.SetTextSize(rel * add_str.GetTextSize())
		OBJECTS.append(add_str)
		add_str.Draw("same")

def simulation(x=0.19, y=SecondLine):
	sim_str = TLatex(x, y, "simulation")
	sim_str.SetNDC()
	sim_str.SetName("sim_str")
	sim_str.SetTextSize(.8 * sim_str.GetTextSize())

	sim_str.Draw("same")
	global OBJECTS
	OBJECTS.append(sim_str)

def _get_nice_lumi_unit(lumi_fb):
	if lumi_fb > 0.5:
		return lumi_fb, "fb"
	
	lumi_pb = lumi_fb * 1e3
	if lumi_pb > 0.5:
		return lumi_pb, "pb"

	lumi_nb = lumi_pb * 1e3
	return lumi_nb, "nb"


def sqrts_lumi(sqrts, lumi_fb, x=0.36, y=SecondLine, rel=.8):
	lumi_val, lumi_unit = _get_nice_lumi_unit(lumi_fb)

	sl_str = TLatex(x, y, "#sqrt{s} = %d TeV, %.1f %s^{-1}" % (sqrts, lumi_val, lumi_unit))
	sl_str.SetNDC()
	sl_str.SetName("sl_str")
	sl_str.SetTextSize(rel * sl_str.GetTextSize())

	sl_str.Draw("same")
	global OBJECTS
	OBJECTS.append(sl_str)

def sqrts(sqrts, x=0.19, y=SecondLine, rel=.8):
	sl_str = TLatex(x, y, "#sqrt{s} = %d TeV" % (sqrts))
	sl_str.SetNDC()
	sl_str.SetName("sl_str")
	sl_str.SetTextSize(rel * sl_str.GetTextSize())

	sl_str.Draw("same")
	global OBJECTS
	OBJECTS.append(sl_str)

def string(x, y, text, rel=0.8, font=None):
	obj = TLatex(x, y, text)
	obj.SetNDC()
	if rel:
		obj.SetTextSize(rel * obj.GetTextSize())
	if font:
		obj.SetTextFont(font)

	obj.Draw("same")

	global OBJECTS
	OBJECTS.append(obj)

def canv_2d(canv, hist=None):
	canv.SetLeftMargin(0.15)
	canv.SetRightMargin(0.15)

	if hist:
		hist.GetYaxis().SetTitleOffset(1.1)
		hist.GetZaxis().SetTitleOffset(.8)
		hist.SetContour(999)


def _get_max(hist, b0, b1):
	maxVal = None
	maxBin = None

	for b in xrange(int(b0), int(b1)+1):
		val = hist.GetBinContent(b)

		if maxVal == None or val > maxVal:
			maxVal = val
			maxBin = b
	
	return maxVal, maxBin

def get_legend_xpos(hists):
	WIDTH = .34
	LEFT_POS = .2
	CENTER_POS = .4
	RIGHT_POS = .6

	nbins = hists[0].GetNbinsX()
	centerbin = hists[0].GetNbinsX() / 2.

	lefts = 0
	rights = 0

	for h in hists:
		maxVal = h.GetMaximum()
		maxBin = h.GetMaximumBin()

		isLeft = maxBin < centerbin

		otherMax, otherBin = _get_max(h, isLeft and centerbin or 0, isLeft and nbins or centerbin)

		if otherMax < 0.7 * maxVal:
			if isLeft:
				lefts += 1
			else:
				rights += 1
		# else: assume ~flat distribution -> no impact on legend position

	if lefts > 0 and rights > 0:
		return CENTER_POS, CENTER_POS+WIDTH
	elif rights > 0:
		return LEFT_POS, LEFT_POS+WIDTH
	else: # either left > 0 or all flat
		return RIGHT_POS, RIGHT_POS+WIDTH

def get_legend_xpos_name(hists):
	WIDTH = .34
	LEFT_POS = .2
	CENTER_POS = .4
	RIGHT_POS = .6

	nbins = hists[0].GetNbinsX()
	centerbin = hists[0].GetNbinsX() / 2.

	lefts = 0
	rights = 0

	for h in hists:
		maxVal = h.GetMaximum()
		maxBin = h.GetMaximumBin()

		isLeft = maxBin < centerbin

		otherMax, otherBin = _get_max(h, isLeft and centerbin or 0, isLeft and nbins or centerbin)

		if otherMax < 0.7 * maxVal:
			if isLeft:
				lefts += 1
			else:
				rights += 1
		# else: assume ~flat distribution -> no impact on legend position

	if lefts > 0 and rights > 0:
		return "center"
	elif rights > 0:
		return "left"
	else: # either left > 0 or all flat
		return "right"

def _init_style():
	global Style
	# use plain black on white colors
	Style.SetOptStat(0)
	_icol=0
	Style.SetFrameBorderMode(_icol)
	Style.SetCanvasBorderMode(_icol)
	Style.SetPadBorderMode(_icol) 
	Style.SetPadColor(_icol)
	Style.SetCanvasColor(_icol)
	Style.SetStatColor(_icol)
	Style.SetPaperSize(20,26)
	Style.SetPadTopMargin(0.06)
	Style.SetPadRightMargin(0.05)
	Style.SetPadBottomMargin(0.16)
	Style.SetPadLeftMargin(0.16)
	Style.SetFrameFillColor(_icol)

	_font=42
	_tsize=0.06
	Style.SetTextFont(_font)
	Style.SetTextSize(_tsize)
	Style.SetLabelFont(_font, "x")
	Style.SetTitleFont(_font, "x")
	Style.SetLabelFont(_font, "y")
	Style.SetTitleFont(_font, "y")
	Style.SetLabelFont(_font, "z")
	Style.SetTitleFont(_font, "z")
	Style.SetLabelSize(_tsize, "x")
	Style.SetTitleSize(_tsize, "x")
	Style.SetLabelSize(_tsize, "y")
	Style.SetTitleSize(_tsize, "y")
	Style.SetLabelSize(_tsize, "z")
	Style.SetTitleSize(_tsize, "z")
	Style.SetMarkerStyle(20)
	Style.SetMarkerSize(1.2)
	Style.SetHistLineWidth(2)
	Style.SetLineStyleString(2, "[12 12]")
	Style.SetEndErrorSize(0.)
	Style.SetOptTitle(0)
	Style.SetOptFit(0)
	Style.SetPadTickX(1)
	Style.SetPadTickY(1)

	Style.SetTitleXOffset(1.2)
	Style.SetTitleYOffset(1.3)

	Style.SetPalette(51)

	TGaxis.SetMaxDigits(4)

	gROOT.SetStyle("SWup")
	gROOT.ForceStyle()

_init_style()

if os.getenv("SWUP_VLQ_MODE"):
	TotalSM = "Total pred."
	DataMCRatio = "Data / pred."


	def ratio_ref(hist, stat_only=True):
		hist.SetMarkerSize(0)
		hist.SetFillColor(stat_only and kGray+1 or TColor.GetColor("#A4B89E"))
		hist.SetFillStyle(1001)