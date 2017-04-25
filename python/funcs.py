import ROOT
from math import *

def getVarValue(c, var, n=0):
  varNameHisto = var
  leaf = c.GetAlias(varNameHisto)
  if leaf!='':
    try:
      return c.GetLeaf(leaf).GetValue(n)
    except:
      raise Exception("Unsuccessful getVarValue for leaf %s and index %i"%(leaf, n))
  else:
    l = c.GetLeaf(var)
    if l:return l.GetValue(n)
    return float('nan')

def getObjDict(c, prefix, variables, i=0):
  variable = {}
  for var in variables:
    variable.update({var:c.GetLeaf(prefix+var).GetValue(i)})
  return variable
#  return var: c.GetLeaf(prefix+var).GetValue(i) for var in variables
  
def getJets(c):
  addJetVars =  ['e', 'mv2c10', 'loosebad', 'tightbad', 'Jvt', 'truthLabel', 'HadronConeExclTruthLabelID', 'killedByPhoton']
  if c=="branches":return ['n_jet','jet_pt','jet_eta', 'jet_phi'] + ['jet_'+x for x in addJetVars]
  nJet = int(getVarValue(c, 'n_jet'))
  jets=[]
  for i in range(nJet):
    jet = getObjDict(c, 'jet_', ['pt','eta', 'phi'], i)
    jet.update(getObjDict(c, 'jet_', addJetVars, i))
    jets.append(jet)
  return jets

def getWeight(c, lumi=36500.):
  w = c.GetLeaf('weight').GetValue()
  xs_w = c.GetLeaf('xs_weight').GetValue()
  sf = c.GetLeaf('sf_total').GetValue()
  nj_w = c.GetLeaf('weight_sherpa22_njets').GetValue()
  return lumi * w * xs_w * sf * nj_w

def getLp(c):
  lepPt = c.GetLeaf('lep_pt').GetValue(0)
  lepPhi = c.GetLeaf('lep_phi').GetValue(0)
  metPt = c.GetLeaf('met').GetValue()
  metPhi = c.GetLeaf('met_phi').GetValue()
  Lp = (lepPt/sqrt(lepPt**2+metPt**2+2*lepPt*metPt*cos(lepPhi-metPhi)))*((lepPt+metPt*cos(lepPhi-metPhi))/sqrt(lepPt**2+metPt**2+2*lepPt*metPt*cos(lepPhi-metPhi)))
  return Lp


def mThree(c):
  m_three = 0.
  sumVec = 0.
  jet1 = ROOT.TLorentzVector()
  jet2 = ROOT.TLorentzVector()
  jet3 = ROOT.TLorentzVector()
  maxJ = ROOT.TLorentzVector() 
  n_jet = int(getVarValue(c, 'n_jet'))
  jets = getJets(c)
  for i in xrange(n_jet):
    for j in xrange(i+1, n_jet):
      for k in xrange(j+1, n_jet):
        jet1.SetPtEtaPhiE(jets[i]['pt'], jets[i]['eta'], jets[i]['phi'], jets[i]['e'])
        jet2.SetPtEtaPhiE(jets[j]['pt'], jets[j]['eta'], jets[j]['phi'], jets[j]['e'])
        jet3.SetPtEtaPhiE(jets[k]['pt'], jets[k]['eta'], jets[k]['phi'], jets[k]['e'])
        temp = (jet1+jet2+jet3).Pt()
        if( temp > sumVec ):
          sumVec = temp
          maxJ = jet1 + jet2 + jet3
  m_three = maxJ.M()
  return m_three*0.001 


