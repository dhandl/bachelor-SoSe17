#!/usr/bin/env python
import sys
import os

_orig_argv = sys.argv[:]
sys.argv = [_orig_argv[0]]

import ROOT
ROOT.gROOT.Macro("$ROOTCOREDIR/scripts/load_packages.C")
from ROOT import *

sys.argv = _orig_argv

from math import sqrt

import SWup.SampleTools as Smp
import SWup.HistTools as HT
import SWup.PlotStyle as PS
from SWup.ext.tabulate import tabulate

from SWup.PlotConfig import *

FORMATS = [
	"plain",
	"simple",
	"grid",
	"pipe",
	"orgtbl",
	"rst",
	"mediawiki",
	"latex",
	"latex_booktabs",
]

TITLE_FMT = "yield for {lumi}/fb"
HEADER_NO_TITLE = ["el", "mu", "total"]

###################################

def get_mc_events(sample, cut_weight):
	cut = "!!(%s)" % cut_weight # make sure that the weight is 1 or 0, and not a float
	hist = HT.draw_hist(sample, "1", cut_weight=cut, hist_name="mcevt_" + sample.get_id(), binning="1,0,2", weighted=False)

	# We need to actually use Integral() here (and make sure
	# that the weight for each event is 1), because just calling
	# hist.GetEntries() leads to wrong results. A bit of testing
	# results in the guess, that 
	# hist.GetEntries() = integral + 2*(number of TTree::Draw() calls)
	# For samples like W+jets this results in much too large numbers
	# while the offset for very simple samples with just one dataset
	# is "only" 2.
	# Why does this happen? I don't know.
	n = hist.Integral(0, hist.GetNbinsX()+1)

	return int(n), 0

def get_sample_yields(opts, sample, cut_name, weight=None):
	_getter = Smp.cross_section
	if not weight:
		cut_weight = "%s * (%s)" % (opts.weight, cut_name)
	else:
		cut_weight = "%s * (%s)" % (weight, cut_name)

	if opts.mc_events:
		_getter = get_mc_events
		cut_weight = "(abs(%s) > 0) * (%s)" % (opts.weight, cut_name)

		# CROSS CHECK without sf_total!

	if not opts.only_total:
		xs_el, err_el = _getter(sample, "%s * (n_el > 0)" % cut_weight)
		xs_mu, err_mu = _getter(sample, "%s * (n_mu > 0)" % cut_weight)
	else:
		xs_el, err_el = _getter(sample, "%s * 1" % cut_weight)
		xs_mu, err_mu = 0,0

	xs_el *= opts.lumi
	xs_mu *= opts.lumi
	err_el *= opts.lumi
	err_mu *= opts.lumi

	if hasattr(sample, "scale_factor") and sample.scale_factor and opts.sf:
		err_el = sqrt((sample.scale_factor[0]*err_el)**2 + (sample.scale_factor[1]*xs_el)**2)
		err_mu = sqrt((sample.scale_factor[0]*err_mu)**2 + (sample.scale_factor[1]*xs_mu)**2)

		xs_el *= sample.scale_factor[0]
		xs_mu *= sample.scale_factor[0]

	return xs_el, err_el, xs_mu, err_mu

def get_bkg_yields(opts, backgrounds):
	table = []
	yield_list = []

	total_el = 0.
	total_el_err2 = 0.
	total_mu = 0.
	total_mu_err2 = 0.
	total_bkg2 = 0.
	total_bkg2_err2 = 0.

	for bkg in backgrounds:
		cut_weight = opts.cut
		if hasattr(bkg, "cut") and bkg.cut:
			cut_weight = "(%s) * (%s)" % (opts.cut, bkg.cut)

		#print "point 1 cut_weight: %s" % cut_weight

		n_el, err_el, n_mu, err_mu = get_sample_yields(opts, bkg, cut_weight)

		#print "point 2 sample_yields, n_el:%f, n_mu:%f" % (n_el, n_mu)

		total_el += n_el
		total_el_err2 += err_el**2
		total_mu += n_mu
		total_mu_err2 += err_mu**2

		n_bkg = n_el + n_mu
		err_bkg = sqrt(err_el**2 + err_mu**2)

		title = bkg.title if bkg.title else bkg.name
		table.append([
			title,
			opts.entry_fmt.format(val=n_el, err=err_el),
			opts.entry_fmt.format(val=n_mu, err=err_mu),
			opts.entry_fmt.format(val=n_bkg, err=err_bkg),
		])

		yield_list.append([bkg.title, n_bkg])

		if opts.weight2:
			n_el2, err_el2, n_mu2, err_mu2 = get_sample_yields(opts, bkg, cut_weight, opts.weight2)
			n_bkg2 = n_el2 + n_mu2
			err_bkg2 = sqrt(err_el2**2 + err_mu2**2)
			total_bkg2 += n_bkg2
			total_bkg2_err2 += err_bkg2**2
			table[-1].append(opts.entry_fmt.format(val=n_bkg2, err=err_bkg2))
			yield_list[-1].append(n_bkg2)

	if not opts.no_total:
		total_bkg = total_el + total_mu
		total_bkg_err2 = total_el_err2 + total_mu_err2
		table.append([
			"Total SM",
			opts.entry_fmt.format(val=total_el, err=sqrt(total_el_err2)),
			opts.entry_fmt.format(val=total_mu, err=sqrt(total_mu_err2)),
			opts.entry_fmt.format(val=total_bkg, err=sqrt(total_bkg_err2)),
		])
		if opts.weight2:
			table[-1].append(opts.entry_fmt.format(val=total_bkg2, err=sqrt(total_bkg2_err2)))

	return table, yield_list

def get_data_yields(opts, data_samples, cut):
	sum_el = 0
	sum_mu = 0

	if type(data_samples) != list:
		data_samples = [data_samples]

	cut_weight = "%s * (%s)" % (opts.weight, cut)

	for smp in data_samples:
		if not opts.only_total:
			n_el, err_el = Smp.cross_section(smp, "%s * (n_el > 0)" % cut_weight)
			n_mu, err_mu = Smp.cross_section(smp, "%s * (n_mu > 0)" % cut_weight)
		else:
			n_el, err_el = Smp.cross_section(smp, "%s * 1" % cut_weight)
			n_mu, err_mu = 0,0

		sum_el += n_el
		sum_mu += n_mu

	return sum_el, sum_mu

def print_yieldtable_events(opts):
	if not opts.lumi:
		print "Error: Can't print events without a given luminosity (-l/--lumi)"
		sys.exit(1)

	header = [TITLE_FMT.format(cut=opts.cut, lumi=opts.lumi*1e-3)] + HEADER_NO_TITLE

	table, yield_list = get_bkg_yields(opts)

	sig_cut = opts.cut
	if opts.no_sig_cut:
		sig_cut = "1"

	n_el, err_el, n_mu, err_mu = get_sample_yields(opts, opts.signal, sig_cut)
	n_sig = n_el + n_mu
	err_sig = sqrt(err_el**2 + err_mu**2)

	title = opts.signal.title if opts.signal.title else opts.signal.name
	table.append([
		title,
		opts.entry_fmt.format(val=n_el, err=err_el),
		opts.entry_fmt.format(val=n_mu, err=err_mu),
		opts.entry_fmt.format(val=n_sig, err=err_sig),
	])
	yield_list.append(["signal", n_sig])

	output = tabulate(table, headers=header, tablefmt=opts.format)
	if "latex" in opts.format:
		output = output.replace("+/-", "$\\pm$")
	print output

	return yield_list

def get_color(title, config):
	if title == "signal":
		return kWhite
	elif title == "others":
		return kGray+1

	for smp in config['stack']:
		if smp.title == title:
			return smp.color

	print "Warning: color for sample '%s' not found" % title
	return kBlack

def plot_pie_chart(opts, config, yields):
	from array import array

	yields.sort(key=lambda y: y[1], reverse=True)

	if config.get("auto-others", False):
		short_yields = yields[0:3]
		short_yields.append([
			"others",
			sum([y[1] for y in yields[3:]])
		])

		yields = short_yields

	entries = array('f', [])
	colors = array('i', [])

	for title, total in yields:
		entries.append(total)
		colors.append(get_color(title, config))

	total = sum(entries)

	pie = TPie("pie", "", len(entries), entries, colors)
	for i, entry in enumerate(yields):
		title, num = entry

		if title == "signal":
			title = opts.signal.title if opts.signal.title else opts.signal.name
		label = "%s (%.1f%%)" % (title, round(num/total*100, 1))
		pie.SetEntryLabel(i, label)
		pie.SetEntryLineWidth(i, 2)

	leg = pie.MakeLegend(0.56, .98, .98, .98-.24)
	PS.legend(leg)

	pie.SetLabelFormat("") # -> no labels
	pie.SetRadius(.375)
	pie.SetX(1.0 - .62)
	pie.SetY(.38)
	#pie.SetLabelsOffset(.02)

	canv = TCanvas("canv", "", 800, 800)
	pie.Draw("<")
	leg.Draw("same")

	ytop = 0.94
	PS.atlas("Work in progress", x=.02, y=ytop, text_offset=0.16)
	PS.sqrts_lumi(13, opts.lumi/1e3, x=0.02, y=ytop-PS.LineSpacing)

	if opts.title:
		PS.string(x=.02, y=ytop-2*PS.LineSpacing, text=opts.title)

	HT.save_canv(canv, opts.output, opts.pie)

def get_sample_breakdown(samples):
	sub_samples = []
	for sample in samples:
		for i in xrange(sample.hist.size()):
			new_data = SH.SampleHandler()
			new_hist = SH.SampleHandler()

			new_data.add(sample.data.at(i))
			new_hist.add(sample.hist.at(i))

			color = kBlack
			if "color" in sample:
				color = sample.color

			sub_samples.append(Sample(
				data=new_data,
				hist=new_hist,
				name=Smp.get_mc_name(sample.hist.at(i)),
				config=sample.config,
				syst=sample.syst,
				title=None, #sample.title,
				color=color,
				scale_factor=sample.scale_factor,
				cut = sample.cut,
			))

	return sub_samples

###################################

def fix_latex(text):
	Replacements = {
		'+/-': '$\\pm$',
		'\\#': '\\',
		'\\{': '{',
		'\\}': '}',
	}

	for pattern, repl in Replacements.iteritems():
		text = text.replace(pattern, repl)

	MathExpressions = {
		't\\bar{t}': "$t\\bar{t}$",
		'\\nu': '$\\nu$', 
		'\\mu': '$\\mu$', 
		'\\tau': '$\\tau$',
		'W+jets': "$W$+jets",
		"Total SM": "\\midrule Total SM",
	}

	for pattern, repl in MathExpressions.iteritems():
		text = text.replace(pattern, repl)


	return text

def print_to_file(file_name, content):
	with open(file_name, 'w') as out:
		out.write(content)

def print_txt(file_name, table, header):
	print_to_file(file_name, tabulate(table, headers=header, tablefmt="simple"))

def print_tex(file_name, table, header):
	content = fix_latex(tabulate(table, headers=header, tablefmt="latex_booktabs"))
	print_to_file(file_name, content)

def parse_options():
	import argparse

	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--config", help="the configuration which will be used for all samples (when not overwritten for a sample)")
	parser.add_argument("--syst", help="systematic")
	parser.add_argument("--tree", default="ntuple", help="Output tree to use")

	parser.add_argument("-p", "--plotcfg", dest="configfile", help="The configuration file to use")
	parser.add_argument("-n", "--cut", default="1.0", help="The cut to use, default: preselection")
	parser.add_argument("-l", "--lumi", type=float, help="Print expected events for this luminosity [in pb]")
	parser.add_argument("-b", "--bkg", dest="samples", action="append", help="Background samples (if not provided, the samples from the plotcfg are used)")
	parser.add_argument("-s", "--signal", help="A signal sample in the form [config:]signal[:title]")
	
	parser.add_argument("--data", action="store_true", help="Show data yields")
	parser.add_argument("--mc-events", action="store_true", help="Output MC events, unweighted")
	parser.add_argument("--sample-breakdown", action="store_true", help="Breakdown MC samples to datasets")
	parser.add_argument("--only-total", action="store_true", help="Don't show individual channels, only total")
	parser.add_argument("--sf", action="store_true", help="Enabling that scale factors are used")

	parser.add_argument("-f", "--format", choices=FORMATS, default="simple", help="The table format")
	parser.add_argument("-F", "--output-file", default="", help="Dump output into a file")

	parser.add_argument("-o", "--output", default="plots/", help="Output directory for pie chart plot")
	parser.add_argument("--pie", help="Create a pie chart of the yields. Usage: --pie <plotname>")

	parser.add_argument("-w", "--weight", default="weight * sf_total * xe_trigger", help="Per event weight")
	parser.add_argument("-W", "--weight2", default="", help="Alternative weight to be shown in an additional column")

	parser.add_argument("--no-total", action="store_true")

	parser.add_argument("--title")

	parser.add_argument("--txt", help="Output file for plain text version of table")
	parser.add_argument("--tex", help="Output file for LaTeX version of table")
	
	opts = parser.parse_args()
	opts.workDir = os.getenv("WorkDir")

	if opts.samples:
		Smp.load_all_samples(opts)

	# load the signal tree with the correct config file
	if opts.signal:
		opts.signal = Smp.load_sample_opts(opts, opts.signal)

	if opts.data:
		opts.lumi = 0
		if opts.mc_events:
			print "Error: Won't print data yields compared to MC events (would be senseless)."
			sys.exit(1)
	else:
		if not opts.lumi and not opts.mc_events:
			print "Error: No lumi given (and --data not enabled)."
			sys.exit(1)

	if opts.pie and not opts.configfile:
		print "Error: Cannot plot pie-chart without plot config (-p/--plotcfg missing)."
		sys.exit(1)

	if opts.configfile and opts.samples and len(opts.samples) > 0:
		print "Warning: Using background samples from plot config file"

	if not opts.configfile and (not opts.samples or len(opts.samples) == 0):
		print "Error: No backgrounds specified, please provide either --bkg or --plotcfg."
		sys.exit(1)

	if opts.mc_events:
		opts.lumi = 1

	opts.data_fmt = "{val:.0f}"
	opts.entry_fmt = "{val:.2f} +/- {err:.2f}"
	if opts.mc_events:
		opts.entry_fmt = "{val:.0f}"

	return opts

def main():
	opts = parse_options()

	config = None
	if opts.configfile:
		config = load_config(opts)
		get_lumi(opts, config)
		print "Luminosity is: ",opts.lumi

		if not opts.lumi:
			print "Error: No luminosity information (no dataset in config and no --lumi given)."
			sys.exit(1)


	top_left = opts.title if opts.title else TITLE_FMT.format(cut=opts.cut, lumi=opts.lumi*1e-3)
	header = [opts.title] + HEADER_NO_TITLE

	if config:
		samples = config['stack']
	else:
		samples = opts.samples

	if opts.sample_breakdown:
		samples = get_sample_breakdown(samples)

	table, yield_list = get_bkg_yields(opts, samples)

	if opts.signal:
		n_el, err_el, n_mu, err_mu = get_sample_yields(opts, opts.signal, opts.cut)
		n_sig = n_el + n_mu
		err_sig = sqrt(err_el**2 + err_mu**2)

		table.append([
			opts.signal.title if opts.signal.title else opts.signal.name,
			opts.entry_fmt.format(val=n_el, err=err_el),
			opts.entry_fmt.format(val=n_mu, err=err_mu),
			opts.entry_fmt.format(val=n_sig, err=err_sig),
		])
		yield_list.append(["signal", n_sig])

		if opts.weight2:
			n_el2, err_el2, n_mu2, err_mu2 = get_sample_yields(opts, opts.signal, opts.cut, opts.weight2)
			n_sig2 = n_el2 + n_mu2
			err_sig2 = sqrt(err_el2**2 + err_mu2**2)
			table[-1].append(opts.entry_fmt.format(val=n_sig2, err=err_sig2))
			yield_list[-1].append(n_sig2)

	if opts.data:
		if config.get('data') == 'pseudodata':
			print "Error: --data specified, but config uses pseudodata."
			sys.exit(1)

		n_el, n_mu = get_data_yields(opts, config['data'], opts.cut)

		row = [
			"Data",
			opts.data_fmt.format(val=n_el, err=0),
			opts.data_fmt.format(val=n_mu, err=0),
			opts.data_fmt.format(val=n_el+n_mu, err=0),
		]

		table.append(row)
		if opts.weight2:
			table[-1].append(table[-1][-1])

	if opts.weight2:
		header += ["total (alt weight)"]

	if opts.only_total:
		tab_total = []
		if not opts.weight2:
			for row in table:
				tab_total.append([row[0], row[-1]])
			table = tab_total
			header = [header[0], header[-1]]
		else:
			for row in table:
				tab_total.append([row[0], row[-2], row[-1]])
			table = tab_total
			header = [header[0], header[-2], header[-1]]

	output = tabulate(table, headers=header, tablefmt=opts.format)
	if "latex" in opts.format:
		output = fix_latex(output)
	print output

	if opts.output_file:
		print_to_file(os.path.join(opts.output,opts.output_file), output)
	if opts.txt:
		print_txt(opts.txt, table, header)
	if opts.tex:
		print_tex(opts.tex, table, header)

	if opts.pie and config:
		plot_pie_chart(opts, config, yield_list)

if __name__ == '__main__':
	main()
