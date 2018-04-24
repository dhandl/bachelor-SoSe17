#!/usr/bin/env python

import ROOT
import os
import sys
from array import array
from math import *



def dphi_jet12(c):
    jet1Phi = c.GetLeaf('jet_phi').GetValue(0)
    jet2Phi = c.GetLeaf('jet_phi').GetValue(1)
    dphi = abs(jet1Phi - jet2Phi)
    if dphi > pi:
        dphi = 2*pi - dphi
    return dphi

def dphi_lep_jet1(c):                                               #Winkel zwischen Lepton und anzunehmendem ISR-jet sinnvoll?
    lepPhi = c.GetLeaf('lep_phi').GetValue(0)
    jet1Phi = c.GetLeaf('jet_phi').GetValue(0)
    dphi = abs(lepPhi - jet1Phi)
    if dphi > pi:
        dphi = 2*pi - dphi
    return dphi

def met_over_squareroot_lepPt_softjetPt(c):                                     #Variationen der Met ueber Ht Variablen
    met = c.GetLeaf('met').GetValue() *0.001
    njet = c.GetLeaf('n_jet').GetValue()
    lepPt = c.GetLeaf('lep_pt').GetValue(0) *0.001
    ht = 0.
    for i in range(1, int(njet)):
        jetpt = c.GetLeaf('jet_pt').GetValue(i) *0.001 
        ht += jetpt 
    ht += lepPt
    return met/(sqrt(ht))

def met_over_lepPt_softjetPt(c):                                     #Variationen der Met ueber Ht Variablen
    met = c.GetLeaf('met').GetValue() *0.001
    njet = c.GetLeaf('n_jet').GetValue()
    lepPt = c.GetLeaf('lep_pt').GetValue(0) *0.001
    ht = 0.
    for i in range(1, int(njet)):
        jetpt = c.GetLeaf('jet_pt').GetValue(i) *0.001 
        ht += jetpt 
    ht += lepPt
    return met/ht

def CT1(c):                                                                       #CMS Variable, kombiniert HT und MET
    met = c.GetLeaf('met').GetValue() *0.001
    ht = c.GetLeaf('ht').GetValue() *0.001
    CT1 = 0.
    if met < (ht-100):
        CT1 = met
    if met > (ht-100):
        CT1 = (ht -100)
    return CT1
    
    
def CT2(c):                                                                        #CMS Variable, kombiniert ISR-Jet-Pt und MET
    met = c.GetLeaf('met').GetValue() *0.001
    jet1Pt = c.GetLeaf('jet_pt').GetValue(0) *0.001
    CT2 = 0.
    if met < (jet1Pt-25):
        CT2 = met
    if met > (jet1Pt-25):
        CT2 = (jet1Pt -25)
    return CT2

def squareroot_lepPt_softjetPt_over_met(c):                                     #Andersherum?
    met = c.GetLeaf('met').GetValue() *0.001
    njet = c.GetLeaf('n_jet').GetValue()
    lepPt = c.GetLeaf('lep_pt').GetValue(0) *0.001
    ht = 0.
    for i in range(1, int(njet)):
        jetpt = c.GetLeaf('jet_pt').GetValue(i) *0.001 
        ht += jetpt 
    ht += lepPt
    return (sqrt(ht))/met


NEW_VAR = [
           {"name":"met_over_sqrt_lepPt_softjetPt", "array":array("f", [0]), "dataType":"F", "varFunc":met_over_squareroot_lepPt_softjetPt},
           {"name":"CT1", "array":array("f", [0]), "dataType":"F", "varFunc":CT1}, 
           {"name":"CT2", "array":array("f", [0]), "dataType":"F", "varFunc":CT2},
           {"name":"squareroot_lepPt_softjetPt_over_met", "array":array("f", [0]), "dataType":"F", "varFunc":squareroot_lepPt_softjetPt_over_met},
           {"name":"met_over_lepPt_softjetPt", "array":array("f", [0]), "dataType":"F", "varFunc":met_over_lepPt_softjetPt}, 
           {"name":"dphi_lep_jet1", "array":array("f", [0]), "dataType":"F", "varFunc":dphi_lep_jet1}, 
           {"name":"dphi_jet12", "array":array("f", [0]), "dataType":"F", "varFunc":dphi_jet12},
         #  {"name":"myNeufVariable", "array":array("f", [0]), "dataType":"F", "varFunc":calcMyVar},
]

def filesize(num):
  for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
    if abs(num) < 1024.0:
      return "%3.1f%sB" % (num, unit)
    num /= 1024.0
  return "%.1fYiB" % num

def main():
  print "Usage: addBranchToFile.py <source directory>"
  src = sys.argv[1]

  if not os.path.isdir(src):
    print "No such folder '{}'".format(src)
    return

  # going to check whether EventWeight will be applied
  for v in NEW_VAR:
    if v["name"] is "EventWeight":
      lumi = float(raw_input("Going to apply total event weight!\nPlease set int. luminosity(pb^-1): "))

  # get all .root files in all subdirectories of <src>
  inFiles = [os.path.relpath(os.path.join(d, f), src) for (d, _, files) in os.walk(src) for f in files if f.endswith("root")] 

  for f in inFiles:
    fSrc= os.path.join(src, f)

    f = ROOT.TFile(fSrc, "UPDATE")

    # Get all trees in this file
    for name in set([k.GetName() for k in f.GetListOfKeys() if k.GetClassName() == "TTree"]):
      print "\nDEBUG: Copying " + name
      t = f.Get(name)

      for v in NEW_VAR:
        v["branch"] = t.Branch(v["name"], v["array"], v["name"]+"/"+v["dataType"])

      n = t.GetEntries()
      for i in xrange(n):
        if (i%10000 == 0):
          print "At %i-th event of %i total events in sample %s!"%(i,n,name)
        t.GetEntry(i)
        assert (v.has_key('varString') or v.has_key('varFunc')), "Error: Did not specify 'varString' or 'varFunc' for variable %s" % repr(v)
        assert not (v.has_key('varString') and v.has_key('varFunc')), "Error: Specified both 'varString' and 'varFunc' for variable %s" % repr(v)
        for v in NEW_VAR:
          varValue = getVarValue(t, v['varString']) if v.has_key('varString') else v['varFunc'](t)
          if v["name"] is "EventWeight":
            varValue = lumi * varValue
          v["array"][0] = varValue
          v["branch"].Fill()

      t.Write()
      #f.Write()
      f.Close()

    print "OK Saved {}".format(filesize(os.stat(fSrc).st_size))

  varInfo = os.path.join(src, "new_var_vol1.txt")
  if os.path.exists(varInfo):
    while True:
      i = raw_input("'{}' exists. Should it be overwritten? (y|n) ".format(varInfo)).strip().lower()
      if i == "y":
        break
      elif i == "n":
        return

  with open(varInfo, "w") as f:
    for v in NEW_VAR:
      f.write(v["name"])

if __name__ == "__main__":
  main()
