import ROOT
from math import *

def px(obj):
  return obj['pt'] * cos(obj['phi'])

def py(obj):
  return obj['pt'] * sin(obj['phi'])

def pz(obj):
  return obj['pt'] * sinh(obj['eta'])

def psquare(x, y, z):
  return (x * x) + (y * y) + (z * z)

def getYieldFromChain(c, cutString = "(1)", lumi = "10000.", weight = "weight * xs_weight * sf_total * weight_sherpa22_njets", returnError=True):
  h = ROOT.TH1D('h_tmp', 'h_tmp', 1,0,2)
  h.Sumw2()
  c.Draw("1>>h_tmp", "("+lumi+"*"+weight+")*("+cutString+")", 'goff')
  res = h.GetBinContent(1)
  resErr = h.GetBinError(1)
  del h
  if returnError:
    return res, resErr
  return res

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

def getJetsLepMet(c):
  if c=="branches":return ['n_jet','jet_pt','jet_eta', 'jet_phi']
  nJet = int(getVarValue(c, 'n_jet'))
  jets=[]
  lep = getObjDict(c, 'lep_', ['pt','eta','phi'], 0)
  met = c.GetLeaf('met').GetValue()
  met_phi = c.GetLeaf('met_phi').GetValue()
  etmiss = {'pt':met, 'phi':met_phi}
  jets.append(etmiss)
  jets.append(lep)
  for i in range(nJet):
    jet = getObjDict(c, 'jet_', ['pt','eta', 'phi'], i)
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

def dphi_jet12(c):
    jet1Phi = c.GetLeaf('jet_phi').GetValue(0)
    jet2Phi = c.GetLeaf('jet_phi').GetValue(1)
    dphi = abs(jet1Phi - jet2Phi)
    if dphi > pi:
        dphi = 2*pi - dphi
    return dphi

def deta_jet12(c):                                                  #sinnvoll eta und deltaR anzuschauen?
    jet1Eta = c.GetLeaf('jet_eta').GetValue(0)
    jet2Eta = c.GetLeaf('jet_eta').GetValue(1)
    deta = abs(jet1Eta - jet2Eta)
    return deta

def dR_jet12(c):
    jet1Phi = c.GetLeaf('jet_phi').GetValue(0)
    jet2Phi = c.GetLeaf('jet_phi').GetValue(1)
    dphi = abs(jet1Phi - jet2Phi)
    if dphi > pi:
        dphi = 2*pi - dphi
    jet1Eta = c.GetLeaf('jet_eta').GetValue(0)
    jet2Eta = c.GetLeaf('jet_eta').GetValue(1)
    deta = abs(jet1Eta - jet2Eta)
    dR = sqrt(deta*deta + dphi*dphi)
    return dR

def dphi_lep_jet1(c):                                               #Winkel zwischen Lepton und anzunehmendem ISR-jet sinnvoll?
    lepPhi = c.GetLeaf('lep_phi').GetValue(0)
    jet1Phi = c.GetLeaf('jet_phi').GetValue(0)
    dphi = abs(lepPhi - jet1Phi)
    if dphi > pi:
        dphi = 2*pi - dphi
    return dphi

def deta_lep_jet1(c):
    lepEta = c.GetLeaf('lep_eta').GetValue(0)
    jet1Eta = c.GetLeaf('jet_eta').GetValue(0)
    deta = abs(lepEta - jet1Eta)
    return deta

def dR_lep_jet1(c):
    lepPhi = c.GetLeaf('lep_phi').GetValue(0)
    jet1Phi = c.GetLeaf('jet_phi').GetValue(0)
    dphi = abs(lepPhi - jet1Phi)
    if dphi > pi:
        dphi = 2*pi - dphi
    lepEta = c.GetLeaf('lep_eta').GetValue(0)
    jet1Eta = c.GetLeaf('jet_eta').GetValue(0)
    deta = abs(lepEta - jet1Eta)
    dR = sqrt(deta*deta + dphi*dphi)
    return dR

def dphi_lep_jet2(c):                                               #Winkel zwischen Lepton und anzunehmendem b-jet sinnvoll?
    lepPhi = c.GetLeaf('lep_phi').GetValue(0)
    jet2Phi = c.GetLeaf('jet_phi').GetValue(1)
    dphi = abs(lepPhi - jet2Phi)
    if dphi > pi:
        dphi = 2*pi - dphi
    return dphi

def deta_lep_jet2(c):
    lepEta = c.GetLeaf('lep_eta').GetValue(0)
    jet2Eta = c.GetLeaf('jet_eta').GetValue(1)
    deta = abs(lepEta - jet2Eta)
    return deta

def dR_lep_jet2(c):
    lepPhi = c.GetLeaf('lep_phi').GetValue(0)
    jet2Phi = c.GetLeaf('jet_phi').GetValue(1)
    dphi = abs(lepPhi - jet2Phi)
    if dphi > pi:
        dphi = 2*pi - dphi
    lepEta = c.GetLeaf('lep_eta').GetValue(0)
    jet2Eta = c.GetLeaf('jet_eta').GetValue(1)
    deta = abs(lepEta - jet2Eta)
    dR = sqrt(deta*deta + dphi*dphi)
    return dR

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
     

def met_over_squareroot_ht(c):
    met = c.GetLeaf('met').GetValue() *0.001
    njet = c.GetLeaf('n_jet').GetValue()
    ht = 0.
    for i in range(1, int(njet)):
        jetpt = c.GetLeaf('jet_pt').GetValue(i) *0.001 
        ht += jetpt   
    return met/(sqrt(ht))

def met_over_ht(c):
    met = c.GetLeaf('met').GetValue() *0.001
    njet = c.GetLeaf('n_jet').GetValue()
    ht = 0.
    for i in range(1, int(njet)):
        jetpt = c.GetLeaf('jet_pt').GetValue(i) *0.001 
        ht += jetpt   
    return met/(ht)

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

def squareroot_lepPt_softjetPt_over_met_square(c):                                     #Andersherum?
    met = c.GetLeaf('met').GetValue() *0.001
    njet = c.GetLeaf('n_jet').GetValue()
    lepPt = c.GetLeaf('lep_pt').GetValue(0) *0.001
    ht = 0.
    for i in range(1, int(njet)):
        jetpt = c.GetLeaf('jet_pt').GetValue(i) *0.001 
        ht += jetpt 
    ht += lepPt
    return (sqrt(ht))/(met*met)


def lep_pt_over_jet1_pt(c):                                                      #Lepton Pt und Jet Pt Vergleiche?
    lepPt = c.GetLeaf('lep_pt').GetValue(0) *0.001
    jetPt = c.GetLeaf('jet_pt').GetValue(0) *0.001
    return lepPt/jetPt

def lep_pt_over_jet2_pt(c):
    lepPt = c.GetLeaf('lep_pt').GetValue(0) *0.001
    jetPt = c.GetLeaf('jet_pt').GetValue(1) *0.001
    return lepPt/jetPt
    
    
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
    
    
def lep_jet1_energy_ratio(c):                                                         #Warum eigentlich nicht die Energie verwenden?
    lepE = c.GetLeaf('lep_e').GetValue(0) *0.001
    jetE = c.GetLeaf('jet_e').GetValue(0) *0.001
    return lepE/jetE

def lep_jet2_energy_ratio(c):                                                         
    lepE = c.GetLeaf('lep_e').GetValue(0) *0.001
    jetE = c.GetLeaf('jet_e').GetValue(1) *0.001
    return lepE/jetE
    
    
    
    
    
    
    
    
    