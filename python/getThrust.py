import ROOT
import funcs
import numpy as np
import os

MacroPath = os.environ["PYTHONPATH"]
ROOT.gROOT.SetMacroPath(ROOT.gROOT.GetMacroPath()+":"+MacroPath+":")
ROOT.gROOT.ProcessLine(".L root/Thrust.C+")

def getThrust(c):
  jets = funcs.getJets(c)
  for j in jets:
    px = funcs.px(j)
    py = funcs.py(j)
    j.update({"px":px, "py":py})
  t = ROOT.Thrust(len(jets), np.array([i["px"] for i in jets]), np.array([k["py"] for k in jets]))
  return t.thrust(), t.thrustPhi() 

def getThrustLepHemi(c):
  jets = funcs.getJetsLepMet(c)
  for j in jets:
    px = funcs.px(j)
    py = funcs.py(j)
    j.update({"px":px, "py":py})  
  t = ROOT.Thrust(len(jets), np.array([i["px"] for i in jets]), np.array([k["py"] for k in jets]))
  return t.thrust(), t.thrustPhi()

