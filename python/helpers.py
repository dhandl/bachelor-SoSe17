
import ROOT
from math import sqrt

def TGraphAsymmErrorsDivide(graph1, graph2):
  graph3 = graph1.Clone() 
  nEntries = graph1.GetN()
  for i in range(nEntries):
    y1 = graph1.GetY()[i]
    y2 = graph2.GetY()[i]
    e1p = graph1.GetErrorYhigh(i)
    e1m = graph1.GetErrorYlow(i)
    e2p = graph2.GetErrorYhigh(i)
    e2m = graph2.GetErrorYlow(i)
    x1 = graph1.GetX()[i]
    if(y2 > 0.):
      graph3.SetPoint(i, x1, y1/y2)
      e1max = ROOT.TMath.Max(ROOT.TMath.Max(e1p/y2, -e1m/y2), 0.)
      e1min = ROOT.TMath.Min(ROOT.TMath.Min(e1p/y2, -e1m/y2), 0.)
      e2max = ROOT.TMath.Max(ROOT.TMath.Max(-e2p*y1/(y2*y2), e2m*y1/(y2*y2)), 0.)
      e2min = ROOT.TMath.Min(ROOT.TMath.Min(-e2p*y1/(y2*y2), e2m*y1/(y2*y2)), 0.)
      graph3.SetPointEYhigh(i, sqrt(e1max*e1max+e2max*e2max))
      graph3.SetPointEYlow(i, sqrt(e1min*e1min+e2min*e2min))
  return graph3

def ATLASLabelRatioPad(x,y,text,color=1):
  l = ROOT.TLatex()
  l.SetNDC();
  l.SetTextFont(72);
  l.SetTextColor(color);
  delx = 0.08*696*ROOT.gPad.GetWh()/(472*ROOT.gPad.GetWw());
  l.DrawLatex(x,y,"ATLAS");
  if True:
    p = ROOT.TLatex();
    p.SetNDC();
    p.SetTextFont(42);
    p.SetTextColor(color);
    p.DrawLatex(x+delx,y,text);

def ATLASLumiLabelRatioPad(x,y,lumi="78",color=1):
  l = ROOT.TLatex()
  l.SetNDC();
  l.SetTextFont(42);
  l.SetTextSize(0.045);
  l.SetTextColor(color);
  dely = 0.05*472*ROOT.gPad.GetWh()/(506*ROOT.gPad.GetWw());
  label="#sqrt{s}=13 TeV, #intL dt = " + lumi + " fb^{-1}"
  l.DrawLatex(x,y-dely,label);
                     

