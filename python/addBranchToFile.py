#!/usr/bin/env python

import ROOT
import os
import sys
from array import array
from math import *

#Hier Funktionen reinpasten
def CT2_30(c):                                                                        #CMS Variable, kombiniert ISR-Jet-Pt und MET
    met = c.GetLeaf('met').GetValue() *0.001
    jet1Pt = c.GetLeaf('jet_pt').GetValue(0) *0.001
    CT2 = 0.
    if met <= (jet1Pt-30):
        CT2 = met
    if met > (jet1Pt-30):
        CT2 = (jet1Pt -30)
    return CT2

def CT2_40(c):                                                                        #CMS Variable, kombiniert ISR-Jet-Pt und MET
    met = c.GetLeaf('met').GetValue() *0.001
    jet1Pt = c.GetLeaf('jet_pt').GetValue(0) *0.001
    CT2 = 0.
    if met <= (jet1Pt-40):
        CT2 = met
    if met > (jet1Pt-40):
        CT2 = (jet1Pt -40)
    return CT2

def CT2_50(c):                                                                        #CMS Variable, kombiniert ISR-Jet-Pt und MET
    met = c.GetLeaf('met').GetValue() *0.001
    jet1Pt = c.GetLeaf('jet_pt').GetValue(0) *0.001
    CT2 = 0.
    if met <= (jet1Pt-50):
        CT2 = met
    if met > (jet1Pt-50):
        CT2 = (jet1Pt -50)
    return CT2

def CT2_60(c):                                                                        #CMS Variable, kombiniert ISR-Jet-Pt und MET
    met = c.GetLeaf('met').GetValue() *0.001
    jet1Pt = c.GetLeaf('jet_pt').GetValue(0) *0.001
    CT2 = 0.
    if met <= (jet1Pt-60):
        CT2 = met
    if met > (jet1Pt-60):
        CT2 = (jet1Pt -60)
    return CT2

def CT2_70(c):                                                                        #CMS Variable, kombiniert ISR-Jet-Pt und MET
    met = c.GetLeaf('met').GetValue() *0.001
    jet1Pt = c.GetLeaf('jet_pt').GetValue(0) *0.001
    CT2 = 0.
    if met <= (jet1Pt-70):
        CT2 = met
    if met > (jet1Pt-70):
        CT2 = (jet1Pt -70)
    return CT2




NEW_VAR = [
           ###Generation 1### 
           #{"name":"met_over_sqrt_lepPt_softjetPt", "array":array("f", [0]), "dataType":"F", "varFunc":met_over_squareroot_lepPt_softjetPt},
           #{"name":"CT1", "array":array("f", [0]), "dataType":"F", "varFunc":CT1}, 
           #{"name":"CT2", "array":array("f", [0]), "dataType":"F", "varFunc":CT2},
           #{"name":"squareroot_lepPt_softjetPt_over_met", "array":array("f", [0]), "dataType":"F", "varFunc":squareroot_lepPt_softjetPt_over_met},
           #{"name":"met_over_lepPt_softjetPt", "array":array("f", [0]), "dataType":"F", "varFunc":met_over_lepPt_softjetPt}, 
           #{"name":"dphi_lep_jet1", "array":array("f", [0]), "dataType":"F", "varFunc":dphi_lep_jet1}, 
           #{"name":"dphi_jet12", "array":array("f", [0]), "dataType":"F", "varFunc":dphi_jet12},
           ###Generation 2###
           #{"name":"lepJet1_energy_ratio", "array":array("f", [0]), "dataType":"F", "varFunc":lep_jet1_energy_ratio},
           #{"name":"mt_over_dphiMetLep", "array":array("f", [0]), "dataType":"F", "varFunc":mt_over_dphiMetLep},
           #{"name":"sqrtLepPt_over_met", "array":array("f", [0]), "dataType":"F", "varFunc":sqrt_lepPt_over_met},
           ###Generation 3###
           #{"name":"CT1_alt", "array":array("f", [0]), "dataType":"F", "varFunc":CT1_alt},
           #{"name":"wPt_over_met", "array":array("f", [0]), "dataType":"F", "varFunc":wPt_over_met},
           #{"name":"Lp", "array":array("f", [0]), "dataType":"F", "varFunc":Lp},
           #{"name":"WEnergy1", "array":array("f", [0]), "dataType":"F", "varFunc":WEnergy1},
           #{"name":"WRapidity1", "array":array("f", [0]), "dataType":"F", "varFunc":WRapidity1},
           #{"name":"W_Lepton_angle_Wrestingframe1", "array":array("f", [0]), "dataType":"F", "varFunc":W_resting_Lepton_angle1},
           #{"name":"WJet2_angle_jet1boost1", "array":array("f", [0]), "dataType":"F", "varFunc":WJet2_jet1boost_angle1},
           #{"name":"W_Nu_angle_Wrestingframe1", "array":array("f", [0]), "dataType":"F", "varFunc":W_Nu_resting_angle1},
           ###Generation 4###
           #{"name":"Cos_W_resting_Lepton_angle1", "array":array("f", [0]), "dataType":"F", "varFunc":Cos_W_resting_Lepton_angle1},
           #{"name":"lepEta_abs", "array":array("f", [0]), "dataType":"F", "varFunc":lepEta_abs},
           #{"name":"LP_abs", "array":array("f", [0]), "dataType":"F", "varFunc":LP_abs},
           ###Generation 5###
           #{"name":"HT", "array":array("f", [0]), "dataType":"F", "varFunc":HT},
           ###Generation 6###
           #{"name":"Ldphi", "array":array("f", [0]), "dataType":"F", "varFunc":Ldphi},
           ###Generation 7###
           {"name":"CT2_30", "array":array("f", [0]), "dataType":"F", "varFunc":CT2_30},
           {"name":"CT2_40", "array":array("f", [0]), "dataType":"F", "varFunc":CT2_40},
           {"name":"CT2_50", "array":array("f", [0]), "dataType":"F", "varFunc":CT2_50},
           {"name":"CT2_60", "array":array("f", [0]), "dataType":"F", "varFunc":CT2_60},
           {"name":"CT2_70", "array":array("f", [0]), "dataType":"F", "varFunc":CT2_70},
           
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
