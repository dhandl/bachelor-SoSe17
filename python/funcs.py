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

def lepEta_abs(c):
    lepEta = c.GetLeaf('lep_eta').GetValue(0)
    return abs(lepEta)

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
    return 1000*(sqrt(ht))/(met*met)


def lep_pt_over_jet1_pt(c):                                                      #Lepton Pt und Jet Pt Vergleiche?
    lepPt = c.GetLeaf('lep_pt').GetValue(0) *0.001
    jetPt = c.GetLeaf('jet_pt').GetValue(0) *0.001
    return lepPt/jetPt

def lep_pt_over_jet2_pt(c):
    lepPt = c.GetLeaf('lep_pt').GetValue(0) *0.001
    jetPt = c.GetLeaf('jet_pt').GetValue(1) *0.001
    return lepPt/jetPt

def HT(c):
    njet = c.GetLeaf('n_jet').GetValue()
    ht = 0.
    for i in range(int(njet)):
        jetpt = c.GetLeaf('jet_pt').GetValue(i) *0.001 
        ht += jetpt
    return ht
    
    
def CT1(c):                                                                       #CMS Variable, kombiniert HT und MET
    met = c.GetLeaf('met').GetValue() *0.001
    njet = c.GetLeaf('n_jet').GetValue()
    ht = 0.
    for i in range(int(njet)):
        jetpt = c.GetLeaf('jet_pt').GetValue(i) *0.001 
        ht += jetpt
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

def CT2_alt(c):                                                                        #CMS Variable, kombiniert ISR-Jet-Pt und MET
    met = c.GetLeaf('met').GetValue() *0.001
    jet1Pt = c.GetLeaf('jet_pt').GetValue(0) *0.001
    CT2 = 0.
    if met < (jet1Pt-50):
        CT2 = met
    if met > (jet1Pt-50):
        CT2 = (jet1Pt -50)
    return CT2

def CT2_alt2(c):                                                                        #CMS Variable, kombiniert ISR-Jet-Pt und MET
    met = c.GetLeaf('met').GetValue() *0.001
    jet1Pt = c.GetLeaf('jet_pt').GetValue(0) *0.001
    CT2 = 0.
    if met < (jet1Pt-75):
        CT2 = met
    if met > (jet1Pt-75):
        CT2 = (jet1Pt -75)
    return CT2

def R1(c):
    eratio = c.GetLeaf('lepJet1_energy_ratio').GetValue()
    ptratio = c.GetLeaf('lepPt_over_met').GetValue()
    R1 = 0.
    if eratio < (ptratio):
        R1 = eratio
    if eratio > (ptratio):
        R1 = (ptratio)
    return R1

def A1(c):
    WRap = c.GetLeaf('WRapidity1').GetValue()
    lepEta = c.GetLeaf('lepEta_abs').GetValue()
    A1 = 0.
    if WRap < (lepEta):
        A1 = WRap
    if WRap > (lepEta):
        A1 = (lepEta)
    return A1

def L1(c):
    Lp = c.GetLeaf('Lp').GetValue()
    wovermet = c.GetLeaf('wPt_over_met').GetValue()
    L1 = 0.
    if Lp > (wovermet-0.5):
        L1 = Lp
    if Lp < (wovermet-0.5):
        L1 = (wovermet-0.5)
    return L1

def Ldphi(c):
    dphimetlep = c.GetLeaf('dphi_met_lep').GetValue()
    dphilepjet = c.GetLeaf('dphi_lep_jet1').GetValue()
    dphilepjet = pi - dphilepjet
    Ldphi = 0
    if dphilepjet > dphimetlep:
        Ldphi = dphimetlep
    else:
        Ldphi = dphilepjet
    return Ldphi

def LdphiMed(c):
    dphimetlep = c.GetLeaf('dphi_met_lep').GetValue()
    dphilepjet = c.GetLeaf('dphi_lep_jet1').GetValue()
    dphilepjet = pi - dphilepjet
    Ldphi = (dphimetlep+dphilepjet)/2
    return Ldphi

def LdphiMax(c):
    dphimetlep = c.GetLeaf('dphi_met_lep').GetValue()
    dphilepjet = c.GetLeaf('dphi_lep_jet1').GetValue()
    dphilepjet = pi - dphilepjet
    Ldphi = 0
    if dphilepjet > dphimetlep:
        Ldphi = dphilepjet
    else:
        Ldphi = dphimetlep
    return Ldphi
    
def lep_jet1_energy_ratio(c):                                                         #Warum eigentlich nicht die Energie verwenden?
    lepE = c.GetLeaf('lep_e').GetValue(0) *0.001
    jetE = c.GetLeaf('jet_e').GetValue(0) *0.001
    return lepE/jetE

def lep_jet2_energy_ratio(c):                                                         
    lepE = c.GetLeaf('lep_e').GetValue(0) *0.001
    jetE = c.GetLeaf('jet_e').GetValue(1) *0.001
    return lepE/jetE

def sqrt_lepPt_over_met(c):
    met = c.GetLeaf('met').GetValue() *0.001
    lepPt = c.GetLeaf('lep_pt').GetValue(0) *0.001
    return sqrt(lepPt)/met

def jet1Pt_over_met(c):
    met = c.GetLeaf('met').GetValue() *0.001
    jet1Pt = c.GetLeaf('jet_pt').GetValue(0) *0.001
    return jet1Pt/met


def mt_over_dphiMetLep(c):
    mt = c.GetLeaf('mt').GetValue() *0.001
    dphiMetLep = c.GetLeaf('dphi_met_lep').GetValue()
    if dphiMetLep == 0:
        return 10000
    else:
        return mt/dphiMetLep

def mt_square_over_dphiMetLep(c):
    mt = c.GetLeaf('mt').GetValue() *0.001
    dphiMetLep = c.GetLeaf('dphi_met_lep').GetValue()
    if dphiMetLep == 0:
        return 10000
    else:
        return (mt*mt)/dphiMetLep


def met_over_sqrt_lepPt_softjetPt_alt(c):                                     #Variationen der Met ueber Ht Variablen
    met = c.GetLeaf('met').GetValue() *0.001
    njet = c.GetLeaf('n_jet').GetValue()
    lepPt = c.GetLeaf('lep_pt').GetValue(0) *0.001
    ht = 0.
    for i in range(int(njet)):
        jetpt = c.GetLeaf('jet_pt').GetValue(i) *0.001 
        if jetpt < 100:
            ht += jetpt 
    ht += lepPt
    return met/sqrt(ht)  

def mt_over_met(c):
    met = c.GetLeaf('met').GetValue() *0.001
    mt = c.GetLeaf('mt').GetValue() *0.001
    return mt/met
    
    
def dR_jet23(c):
    jet2Phi = c.GetLeaf('jet_phi').GetValue(1)
    njet = c.GetLeaf('n_jet').GetValue()
    if int(njet) >= 3:
        jet3Phi = c.GetLeaf('jet_phi').GetValue(2)
        dphi = abs(jet2Phi - jet3Phi)
        if dphi > pi:
            dphi = 2*pi - dphi
        jet2Eta = c.GetLeaf('jet_eta').GetValue(1)
        jet3Eta = c.GetLeaf('jet_eta').GetValue(2)
        deta = abs(jet2Eta - jet3Eta)
        dR = sqrt(deta*deta + dphi*dphi)
        return dR 
    else:
        return (-1)
    
def bjet_discr(c):
    b_high = -1
    njet = c.GetLeaf('n_jet').GetValue()
    for i in range(int(njet)):
        jet_disc = c.GetLeaf('jet_mv2c10').GetValue(i)
        if jet_disc > b_high:
            b_high = jet_disc
    return b_high



def wPt_over_met(c):
    met = c.GetLeaf('met').GetValue() *0.001
    wPt = c.GetLeaf('pt_W').GetValue() 
    return wPt/met


def jet12_energy_ratio(c):
    jet1E = c.GetLeaf('jet_e').GetValue(0) *0.001
    jet2E = c.GetLeaf('jet_e').GetValue(1) *0.001
    return jet1E/jet2E

def Ejet2_Elep_added(c):
    lepE = c.GetLeaf('lep_e').GetValue(0) *0.001
    jetE = c.GetLeaf('jet_e').GetValue(1) *0.001
    return lepE+jetE

def Ejet2Elep_over_Ejet1Met(c):
    lepE = c.GetLeaf('lep_e').GetValue(0) *0.001
    jet1E = c.GetLeaf('jet_e').GetValue(0) *0.001
    jet2E = c.GetLeaf('jet_e').GetValue(1) *0.001
    met = c.GetLeaf('met').GetValue() *0.001
    return (lepE*jet2E)/(jet1E*met)


def jet12_invmass(c):
    m_two = 0.
    sumVec = 0.
    jet1 = ROOT.TLorentzVector()
    jet2 = ROOT.TLorentzVector()
    jet1.SetPtEtaPhiE(c.GetLeaf('jet_pt').GetValue(0) *0.001, c.GetLeaf('jet_eta').GetValue(0), c.GetLeaf('jet_phi').GetValue(0), c.GetLeaf('jet_e').GetValue(0) *0.001)
    jet2.SetPtEtaPhiE(c.GetLeaf('jet_pt').GetValue(1) *0.001, c.GetLeaf('jet_eta').GetValue(1), c.GetLeaf('jet_phi').GetValue(1), c.GetLeaf('jet_e').GetValue(1) *0.001)
    sumVec = jet1 + jet2
    m_two = sumVec.M()
    return m_two

def Lp(c):
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    MetX = c.GetLeaf('met_x').GetValue() *0.001
    MetY = c.GetLeaf('met_y').GetValue() *0.001
    WPx = lepVec.Px() + MetX
    WPy = lepVec.Py() + MetY
    Lp = (lepVec.Px()*WPx + lepVec.Py()*WPy)/(WPx**2 + WPy**2)
    return Lp
    
    
    

def WVector1(c):
    from scipy.optimize import minimize
    dphi = c.GetLeaf('dphi_met_lep').GetValue()
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    M_W = 80.4
    neuVec = ROOT.TLorentzVector()
    pt_miss = c.GetLeaf('met').GetValue() *0.001
    MetX = c.GetLeaf('met_x').GetValue() *0.001
    MetY = c.GetLeaf('met_y').GetValue() *0.001

    Pxl = lepVec.Px()
    Pyl = lepVec.Py()
    Pzl = lepVec.Pz()
    Ptl = lepVec.Pt()
    mt2 = 2 * (Ptl*pt_miss - Pxl*MetX - Pyl*MetY)
    if mt2<0:
        mt2 = 0
    mt = sqrt(mt2)
    El = sqrt(Ptl**2+Pzl**2)
    
    if mt < M_W:
        mu = 0.5 * M_W * M_W + Pxl*MetX + Pyl*MetY
        p_nu_z_1 = (mu*Pzl)/(Ptl*Ptl) + sqrt( ((mu**2)*(Pzl**2))/(Ptl**4) - (El*El*pt_miss*pt_miss - mu*mu)/(Ptl*Ptl) ) 
        p_nu_z_2 = (mu*Pzl)/(Ptl*Ptl) - sqrt( ((mu**2)*(Pzl**2))/(Ptl**4) - (El*El*pt_miss*pt_miss - mu*mu)/(Ptl*Ptl) )
        neuVec.SetPx(MetX)
        neuVec.SetPy(MetY)
    else:
        #p_nu_y_1 = ((M_W*M_W*Pyl + 2*Pxl*Pyl*p_nu_x)/(2*Pxl*Pxl) + (M_W*Ptl*sqrt(M_W*M_W + 4*Pxl*p_nu_x))/(2*Pxl*Pxl))
        #p_nu_y_2 = ((M_W*M_W*Pyl + 2*Pxl*Pyl*p_nu_x)/(2*Pxl*Pxl) - (M_W*Ptl*sqrt(M_W*M_W + 4*Pxl*p_nu_x))/(2*Pxl*Pxl))
        
        def deltaPlus(x):
            delta = sqrt((x[0] - MetX)**2 + (((M_W*M_W*Pyl + 2*Pxl*Pyl*x[0])/(2*Pxl*Pxl) + (M_W*Ptl*sqrt(x[1]))/(2*Pxl*Pxl)) - MetY)**2)
            return delta
        def deltaMinus(x):
            delta = sqrt((x[0] - MetX)**2 + (((M_W*M_W*Pyl + 2*Pxl*Pyl*x[0])/(2*Pxl*Pxl) - (M_W*Ptl*sqrt(x[1]))/(2*Pxl*Pxl)) - MetY)**2)
            return delta
        
        cons = ({'type': 'eq', 'fun': lambda x:  M_W*M_W + 4*Pxl*x[0] - x[1]})
        
        x0 = [0.,6464.16]
        bnds = ((None,None),(0,None))
        
        resPlus = minimize(deltaPlus, x0, method='SLSQP',bounds=bnds, constraints=cons, tol=1e-8)
        resMinus = minimize(deltaMinus, x0, method='SLSQP',bounds=bnds, constraints=cons, tol=1e-8)
        
        deltaPlus1 = deltaPlus(resPlus.x)
        deltaMinus1 = deltaMinus(resMinus.x)
        
        if deltaPlus1 > deltaMinus1:
            p_nu_x = resMinus.x[0]
            p_nu_y = ((M_W*M_W*Pyl + 2*Pxl*Pyl*p_nu_x)/(2*Pxl*Pxl) - (M_W*Ptl*sqrt(M_W*M_W + 4*Pxl*p_nu_x))/(2*Pxl*Pxl))
        else:
            p_nu_x = resPlus.x[0]
            p_nu_y = ((M_W*M_W*Pyl + 2*Pxl*Pyl*p_nu_x)/(2*Pxl*Pxl) + (M_W*Ptl*sqrt(M_W*M_W + 4*Pxl*p_nu_x))/(2*Pxl*Pxl))
            
        p_nu_t = sqrt(p_nu_x*p_nu_x + p_nu_y*p_nu_y)
        mu = 0.5 * M_W * M_W + Pxl*p_nu_x + Pyl*p_nu_y
        p_nu_z_1 = (mu*Pzl)/(Ptl*Ptl)
        p_nu_z_2 = (mu*Pzl)/(Ptl*Ptl)
        neuVec.SetPx(p_nu_x)
        neuVec.SetPy(p_nu_y)
    
    if abs(p_nu_z_1)>abs(p_nu_z_2):
        neuVec.SetPz(p_nu_z_2)
    else:
        neuVec.SetPz(p_nu_z_1)
    
    
    neuVec.SetE(sqrt(neuVec.Px()*neuVec.Px() + neuVec.Py()*neuVec.Py() + neuVec.Pz()*neuVec.Pz()))
    
    WVec = ROOT.TLorentzVector()
    WVec = lepVec + neuVec
    
    return WVec

def WVector2(c):
    from scipy.optimize import minimize
    dphi = c.GetLeaf('dphi_met_lep').GetValue()
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    M_W = 80.4
    neuVec = ROOT.TLorentzVector()
    pt_miss = c.GetLeaf('met').GetValue() *0.001
    MetX = c.GetLeaf('met_x').GetValue() *0.001
    MetY = c.GetLeaf('met_y').GetValue() *0.001

    Pxl = lepVec.Px()
    Pyl = lepVec.Py()
    Pzl = lepVec.Pz()
    Ptl = lepVec.Pt()
    mt2 = 2 * (Ptl*pt_miss - Pxl*MetX - Pyl*MetY)
    if mt2<0:
        mt2 = 0
    mt = sqrt(mt2)
    El = sqrt(Ptl**2+Pzl**2)
    
    if mt < M_W:
        mu = 0.5 * M_W * M_W + Pxl*MetX + Pyl*MetY
        p_nu_z_1 = (mu*Pzl)/(Ptl*Ptl) + sqrt( (mu*mu*Pzl*Pzl)/(Ptl*Ptl*Ptl*Ptl) - (El*El*pt_miss*pt_miss - mu*mu)/(Ptl*Ptl) ) 
        p_nu_z_2 = (mu*Pzl)/(Ptl*Ptl) - sqrt( (mu*mu*Pzl*Pzl)/(Ptl*Ptl*Ptl*Ptl) - (El*El*pt_miss*pt_miss - mu*mu)/(Ptl*Ptl) )
        neuVec.SetPx(MetX)
        neuVec.SetPy(MetY)
    else:
        #p_nu_y_1 = ((M_W*M_W*Pyl + 2*Pxl*Pyl*p_nu_x)/(2*Pxl*Pxl) + (M_W*Ptl*sqrt(M_W*M_W + 4*Pxl*p_nu_x))/(2*Pxl*Pxl))
        #p_nu_y_2 = ((M_W*M_W*Pyl + 2*Pxl*Pyl*p_nu_x)/(2*Pxl*Pxl) - (M_W*Ptl*sqrt(M_W*M_W + 4*Pxl*p_nu_x))/(2*Pxl*Pxl))
        
        def deltaPlus(x):
            delta = sqrt((x[0] - MetX)**2 + (((M_W*M_W*Pyl + 2*Pxl*Pyl*x[0])/(2*Pxl*Pxl) + (M_W*Ptl*sqrt(x[1]))/(2*Pxl*Pxl)) - MetY)**2)
            return delta
        def deltaMinus(x):
            delta = sqrt((x[0] - MetX)**2 + (((M_W*M_W*Pyl + 2*Pxl*Pyl*x[0])/(2*Pxl*Pxl) - (M_W*Ptl*sqrt(x[1]))/(2*Pxl*Pxl)) - MetY)**2)
            return delta
        
        cons = ({'type': 'eq', 'fun': lambda x:  M_W*M_W + 4*Pxl*x[0] - x[1]})
        
        x0 = [0.,6464.16]
        bnds = ((None,None),(0,None))
        
        resPlus = minimize(deltaPlus, x0, method='SLSQP',bounds=bnds, constraints=cons, tol=1e-8)
        resMinus = minimize(deltaMinus, x0, method='SLSQP',bounds=bnds, constraints=cons, tol=1e-8)
        
        deltaPlus1 = deltaPlus(resPlus.x)
        deltaMinus1 = deltaMinus(resMinus.x)
        
        if deltaPlus1 > deltaMinus1:
            p_nu_x = resMinus.x[0]
            p_nu_y = ((M_W*M_W*Pyl + 2*Pxl*Pyl*p_nu_x)/(2*Pxl*Pxl) - (M_W*Ptl*sqrt(M_W*M_W + 4*Pxl*p_nu_x))/(2*Pxl*Pxl))
        else:
            p_nu_x = resPlus.x[0]
            p_nu_y = ((M_W*M_W*Pyl + 2*Pxl*Pyl*p_nu_x)/(2*Pxl*Pxl) + (M_W*Ptl*sqrt(M_W*M_W + 4*Pxl*p_nu_x))/(2*Pxl*Pxl))
            
        p_nu_t = sqrt(p_nu_x*p_nu_x + p_nu_y*p_nu_y)
        mu = 0.5 * M_W * M_W + Pxl*p_nu_x + Pyl*p_nu_y
        p_nu_z_1 = (mu*Pzl)/(Ptl*Ptl)
        p_nu_z_2 = (mu*Pzl)/(Ptl*Ptl)
        neuVec.SetPx(p_nu_x)
        neuVec.SetPy(p_nu_y)
    
    if abs(p_nu_z_1)<abs(p_nu_z_2):
        neuVec.SetPz(p_nu_z_2)
    else:
        neuVec.SetPz(p_nu_z_1)
    
    
    neuVec.SetE(sqrt(neuVec.Px()*neuVec.Px() + neuVec.Py()*neuVec.Py() + neuVec.Pz()*neuVec.Pz()))
    
    WVec = ROOT.TLorentzVector()
    WVec = lepVec + neuVec
    
    return WVec

def NuE1(c):
    WVec = WVector1(c)
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    NuVec = WVec - lepVec
    return NuVec.E()

def NuEta1(c):
    WVec = WVector1(c)
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    NuVec = WVec - lepVec
    return abs(NuVec.Eta())

def WEnergy1(c):
    WVec = WVector1(c)
    return WVec.E()

def WEta_abs1(c):
    WVec = WVector1(c)
    return abs(WVec.Eta())

def WEnergy2(c):
    WVec = WVector2(c)
    return WVec.E()*0.001

def WEta_abs2(c):
    WVec = WVector2(c)
    return abs(WVec.Eta())

def WMass1(c):
    WVec = WVector1(c)
    return WVec.M()

def WMass2(c):
    WVec = WVector2(c)
    return WVec.M()

def WRapidity1(c):
    WVec = WVector1(c)
    return abs(WVec.Rapidity())

def WRapidity2(c):
    WVec = WVector2(c)
    return abs(WVec.Rapidity())

def WLepton_angle1(c):
    WVec = WVector1(c)
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    betaX = (lepVec.Px())/(lepVec.E()) - (WVec.Px())/(WVec.E())
    betaY = (lepVec.Py())/(lepVec.E()) - (WVec.Py())/(WVec.E())
    betaZ = (lepVec.Pz())/(lepVec.E()) - (WVec.Pz())/(WVec.E())
    lepVec.Boost(betaX,betaY,betaZ)
    angle = lepVec.Angle(WVec.Vect())
    return angle
    
    
def WLepton_angle_Q1(c):
    angle = abs(WLepton_angle1(c))
    Q = c.GetLeaf('lep_charge').GetValue(0)
    return Q * angle
    
            
def W_resting_Lepton_angle1(c):
    WVec = WVector1(c)
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    betaX = -((WVec.Px())/(WVec.E()))
    betaY = -((WVec.Py())/(WVec.E()))
    betaZ = -((WVec.Pz())/(WVec.E()))
    lepVec.Boost(betaX,betaY,betaZ)
    angle = lepVec.Angle(WVec.Vect())
    return angle 

def W_resting_Lepton_angle2(c):
    WVec = WVector2(c)
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    betaX = -((WVec.Px())/(WVec.E()))
    betaY = -((WVec.Py())/(WVec.E()))
    betaZ = -((WVec.Pz())/(WVec.E()))
    lepVec.Boost(betaX,betaY,betaZ)
    angle = lepVec.Angle(WVec.Vect())
    return angle    
   
def W_resting_Lepton_deta1(c):
    WVec = WVector1(c)
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    betaX = -((WVec.Px())/(WVec.E()))
    betaY = -((WVec.Py())/(WVec.E()))
    betaZ = -((WVec.Pz())/(WVec.E()))
    lepVec.Boost(betaX,betaY,betaZ)
    angle = abs(lepVec.Eta() - WVec.Eta())
    return angle   

def W_resting_Lepton_dphi1(c):
    WVec = WVector1(c)
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    betaX = -((WVec.Px())/(WVec.E()))
    betaY = -((WVec.Py())/(WVec.E()))
    betaZ = -((WVec.Pz())/(WVec.E()))
    lepVec.Boost(betaX,betaY,betaZ)
    dphi = abs(lepVec.Phi() - WVec.Phi())
    if dphi > pi:
        dphi = 2*pi - dphi
    return dphi

def Lepton_Eta_in_Wresting1(c):
    WVec = WVector1(c)
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    betaX = -((WVec.Px())/(WVec.E()))
    betaY = -((WVec.Py())/(WVec.E()))
    betaZ = -((WVec.Pz())/(WVec.E()))
    lepVec.Boost(betaX,betaY,betaZ)
    angle = abs(lepVec.Eta())
    return angle   
    
   
def Cos_W_resting_Lepton_angle1(c):
    WVec = WVector1(c)
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    betaX = -((WVec.Px())/(WVec.E()))
    betaY = -((WVec.Py())/(WVec.E()))
    betaZ = -((WVec.Pz())/(WVec.E()))
    lepVec.Boost(betaX,betaY,betaZ)
    angle = lepVec.Angle(WVec.Vect())
    return cos(angle)

def W_resting_Lepton_angle_Q1(c):
    angle = abs(W_resting_Lepton_angle1(c))
    Q = c.GetLeaf('lep_charge').GetValue(0)
    return Q * angle    

def WP_test(c):
    WVec = WVector1(c)    
    betaX = -((WVec.Px())/(WVec.E()))
    betaY = -((WVec.Py())/(WVec.E()))
    betaZ = -((WVec.Pz())/(WVec.E()))
    WVec.Boost(betaX,betaY,betaZ)
    return (abs(WVec.Px()) + abs(WVec.Py()) + abs(WVec.Pz()))

def mymt(c):
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    MetX = c.GetLeaf('met_x').GetValue() *0.001
    MetY = c.GetLeaf('met_y').GetValue() *0.001
    pt_miss = c.GetLeaf('met').GetValue() *0.001
    Pxl = lepVec.Px()
    Pyl = lepVec.Py()
    Pzl = lepVec.Pz()
    Ptl = lepVec.Pt()
    mt2 = 2 * (Ptl*pt_miss - Pxl*MetX - Pyl*MetY)
    if mt2<0:
        mt2 = 0
    mt = sqrt(mt2)
    return mt

def mymet(c):
    MetX = c.GetLeaf('met_x').GetValue() *0.001
    MetY = c.GetLeaf('met_y').GetValue() *0.001
    return sqrt((MetX**2) + (MetY**2))
    

def WPz1(c):
    WVec = WVector1(c)
    return WVec.Pz()

def WPz2(c):
    WVec = WVector2(c)
    return WVec.Pz()*0.001


def WJet2_jet1boost_angle1(c):
    WVec = WVector1(c)
    jet1Vec = ROOT.TLorentzVector()
    jet1Vec.SetPtEtaPhiE(c.GetLeaf('jet_pt').GetValue(0) *0.001, c.GetLeaf('jet_eta').GetValue(0), c.GetLeaf('jet_phi').GetValue(0), c.GetLeaf('jet_e').GetValue(0) *0.001)
    jet2Vec = ROOT.TLorentzVector()
    jet2Vec.SetPtEtaPhiE(c.GetLeaf('jet_pt').GetValue(1) *0.001, c.GetLeaf('jet_eta').GetValue(1), c.GetLeaf('jet_phi').GetValue(1), c.GetLeaf('jet_e').GetValue(1) *0.001)
    betaX = ((jet1Vec.Px())/(jet1Vec.E()))
    betaY = ((jet1Vec.Py())/(jet1Vec.E()))
    betaZ = ((jet1Vec.Pz())/(jet1Vec.E()))
    WVec.Boost(betaX,betaY,betaZ)
    jet2Vec.Boost(betaX,betaY,betaZ)
    angle = jet2Vec.Angle(WVec.Vect())
    return angle

def Jet2Lep_jet1boost_angle1(c):
    WVec = WVector1(c)
    jet1Vec = ROOT.TLorentzVector()
    jet1Vec.SetPtEtaPhiE(c.GetLeaf('jet_pt').GetValue(0) *0.001, c.GetLeaf('jet_eta').GetValue(0), c.GetLeaf('jet_phi').GetValue(0), c.GetLeaf('jet_e').GetValue(0) *0.001)
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    jet2Vec = ROOT.TLorentzVector()
    jet2Vec.SetPtEtaPhiE(c.GetLeaf('jet_pt').GetValue(1) *0.001, c.GetLeaf('jet_eta').GetValue(1), c.GetLeaf('jet_phi').GetValue(1), c.GetLeaf('jet_e').GetValue(1) *0.001)
    betaX = ((jet1Vec.Px())/(jet1Vec.E()))
    betaY = ((jet1Vec.Py())/(jet1Vec.E()))
    betaZ = ((jet1Vec.Pz())/(jet1Vec.E()))
    lepVec.Boost(betaX,betaY,betaZ)
    jet2Vec.Boost(betaX,betaY,betaZ)
    angle = jet2Vec.Angle(lepVec.Vect())
    return angle


def transMass(c):
    MChi = 430
    MB = 4
    met = c.GetLeaf('met').GetValue() *0.001
    MetX = c.GetLeaf('met_x').GetValue() *0.001
    MetY = c.GetLeaf('met_y').GetValue() *0.001
    BVec = ROOT.TLorentzVector()
    ptmin = 10000
    njet = c.GetLeaf('n_jet').GetValue()
    for i in range(int(njet)):
        jetpt = c.GetLeaf('jet_pt').GetValue(i)*0.001
        if jetpt<ptmin:
            imin = i
    BVec.SetPtEtaPhiE(c.GetLeaf('jet_pt').GetValue(imin) *0.001, c.GetLeaf('jet_eta').GetValue(imin), c.GetLeaf('jet_phi').GetValue(imin), c.GetLeaf('jet_e').GetValue(imin) *0.001)
    LepVec = ROOT.TLorentzVector()
    LepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    ETb = sqrt(MB**2 + BVec.Pt()**2)
    ETChi = sqrt(MChi**2 + met**2)
    ETLep = LepVec.Pt()
    MT2 = MChi**2 + MB**2 + 2*(ETb*ETChi + ETb*ETLep + ETLep*ETChi - MetX*BVec.Px() - MetY*BVec.Py() - MetX*LepVec.Px() - MetY*LepVec.Py() - BVec.Px()*LepVec.Px() - BVec.Py()*LepVec.Py() )
    if MT2 < 0:
        MT2 = 0
    MT = sqrt(MT2)
    return MT


def WRapidity_Q1(c):
    WVec = WVector1(c)
    angle = WVec.Rapidity()
    Q = c.GetLeaf('lep_charge').GetValue(0)
    return Q * angle

def W_Nu_resting_angle1(c):
    WVec = WVector1(c)
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    nuVec = WVec - lepVec
    betaX = -((WVec.Px())/(WVec.E()))
    betaY = -((WVec.Py())/(WVec.E()))
    betaZ = -((WVec.Pz())/(WVec.E()))
    nuVec.Boost(betaX,betaY,betaZ)
    angle = WVec.Angle(nuVec.Vect())
    return angle

def my_wPt_over_met(c):
    WVec = WVector1(c)
    met = c.GetLeaf('met').GetValue() *0.001
    wPt = WVec.Pt() 
    return wPt/met

def LPQ(c):
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    MetX = c.GetLeaf('met_x').GetValue() *0.001
    MetY = c.GetLeaf('met_y').GetValue() *0.001
    WPx = lepVec.Px() + MetX
    WPy = lepVec.Py() + MetY
    Lp = (lepVec.Px()*WPx + lepVec.Py()*WPy)/(WPx**2 + WPy**2)
    Q = c.GetLeaf('lep_charge').GetValue(0)
    return (-Q)*Lp

def HToverN(c):
    njet = c.GetLeaf('n_jet').GetValue()
    ht = 0.
    for i in range(int(njet)):
        jetpt = c.GetLeaf('jet_pt').GetValue(i) *0.001 
        ht += jetpt
    return ht/(int(njet))

def Jet1PtoverN(c):
    njet = c.GetLeaf('n_jet').GetValue()
    jetpt = c.GetLeaf('jet_pt').GetValue(0) *0.001
    return jetpt/(int(njet))

def Jet2PtoverN(c):
    njet = c.GetLeaf('n_jet').GetValue()
    jetpt = c.GetLeaf('jet_pt').GetValue(1) *0.001
    return jetpt/(int(njet))


def transMassTrueB(c):
    MChi = 380
    MB = 4
    met = c.GetLeaf('met').GetValue() *0.001
    MetX = c.GetLeaf('met_x').GetValue() *0.001
    MetY = c.GetLeaf('met_y').GetValue() *0.001
    BVec = ROOT.TLorentzVector()
    BVec.SetPtEtaPhiE(c.GetLeaf('bjet_pt').GetValue(0) *0.001, c.GetLeaf('bjet_eta').GetValue(0), c.GetLeaf('bjet_phi').GetValue(0), c.GetLeaf('bjet_e').GetValue(0) *0.001)
    LepVec = ROOT.TLorentzVector()
    LepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    ETb = sqrt(MB**2 + BVec.Pt()**2)
    ETChi = sqrt(MChi**2 + met**2)
    ETLep = LepVec.Pt()
    MT2 = MChi**2 + MB**2 + 2*(ETb*ETChi + ETb*ETLep + ETLep*ETChi - MetX*BVec.Px() - MetY*BVec.Py() - MetX*LepVec.Px() - MetY*LepVec.Py() - BVec.Px()*LepVec.Px() - BVec.Py()*LepVec.Py() )
    if MT2 < 0:
        MT2 = 0
    MT = sqrt(MT2)
    return MT    

def jet2_discr(c):
    jet_disc = c.GetLeaf('jet_mv2c10').GetValue(1)
    return jet_disc

def BJetPtoverN(c):
    njet = c.GetLeaf('n_jet').GetValue()
    jetpt = c.GetLeaf('bjet_pt').GetValue(0) *0.001
    return jetpt/(int(njet))




















































def StopVector1(c):
    from scipy.optimize import minimize
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiM(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), 0)
    BVec = ROOT.TLorentzVector()
    BVec.SetPtEtaPhiE(c.GetLeaf('jet_pt').GetValue(1) *0.001, c.GetLeaf('jet_eta').GetValue(1), c.GetLeaf('jet_phi').GetValue(1), c.GetLeaf('jet_e').GetValue(1) *0.001)
    M_Stop = 450
    M_Neutralino = 430
    M_B = BVec.M()
    M = M_Stop**2 - M_B**2 - M_Neutralino**2 - 2*(BVec.Dot(lepVec))
    chiVec = ROOT.TLorentzVector()
    pt_miss = c.GetLeaf('met').GetValue() *0.001
    MetX = c.GetLeaf('met_x').GetValue() *0.001
    MetY = c.GetLeaf('met_y').GetValue() *0.001

    
    ###kombinierte Vierervektoren:
    kombVec = ROOT.TLorentzVector()
    kombVec = lepVec + BVec
    Pxk = kombVec.Px()
    Pyk = kombVec.Py()
    Pzk = kombVec.Pz()
    Pftk = sqrt(kombVec.E()**2 - kombVec.Pz()**2)
    Ek = kombVec.E()
    
    mue = 0.5 * M  + Pxk*MetX + Pyk*MetY
    rad =  (mue*mue*Pzk*Pzk)/(Pftk*Pftk*Pftk*Pftk) - (Ek*Ek*(pt_miss*pt_miss + M_Neutralino**2) - mue*mue)/(Pftk*Pftk) 
    
    if rad > 0:
        mu = 0.5 * M + Pxk*MetX + Pyk*MetY
        p_chi_z_1 = (mu*Pzk)/(Pftk*Pftk) + sqrt( (mu*mu*Pzk*Pzk)/(Pftk*Pftk*Pftk*Pftk) - (Ek*Ek*(pt_miss*pt_miss + M_Neutralino**2) - mu*mu)/(Pftk*Pftk) ) 
        p_chi_z_2 = (mu*Pzk)/(Pftk*Pftk) - sqrt( (mu*mu*Pzk*Pzk)/(Pftk*Pftk*Pftk*Pftk) - (Ek*Ek*(pt_miss*pt_miss + M_Neutralino**2) - mu*mu)/(Pftk*Pftk) )
        chiVec.SetPx(MetX)
        chiVec.SetPy(MetY)
    else:
        #p_chi_y_1 = ((M*Pyk + 2*Pxk*Pyk*p_chi_x)/(2*Pxk*Pxk) + (Pftk*sqrt(M**2 + 4*(Pxk*p_chi_x*M + Pxk*Pxk*(M_Neutralino*M_Neutralino))))/(2*Pxk*Pxk))
        #p_chi_y_2 = ((M*Pyk + 2*Pxk*Pyk*p_chi_x)/(2*Pxk*Pxk) - (Pftk*sqrt(M**2 + 4*(Pxk*p_chi_x*M + Pxk*Pxk*(M_Neutralino*M_Neutralino))))/(2*Pxk*Pxk))
        
        def deltaPlus(x):
            delta = sqrt((x[0] - MetX)**2 + (((M*Pyk + 2*Pxk*Pyk*x[0])/(2*Pxk*Pxk) + (Pftk*sqrt(x[1]))/(2*Pxk*Pxk)) - MetY)**2)
            return delta
        def deltaMinus(x):
            delta = sqrt((x[0] - MetX)**2 + (((M*Pyk + 2*Pxk*Pyk*x[0])/(2*Pxk*Pxk) - (Pftk*sqrt(x[1]))/(2*Pxk*Pxk)) - MetY)**2)
            return delta
        
        cons = ({'type': 'eq', 'fun': lambda x:  M**2 + 4*(Pxk*M*x[0] + Pxk*Pxk*(M_Neutralino*M_Neutralino)) - x[1]})
        
        x0 = [0.,M**2 + 4*Pxk*Pxk*(M_Neutralino*M_Neutralino)]
        bnds = ((None,None),(0,None))
        
        resPlus = minimize(deltaPlus, x0, method='SLSQP',bounds=bnds, constraints=cons, tol=1e-8)
        resMinus = minimize(deltaMinus, x0, method='SLSQP',bounds=bnds, constraints=cons, tol=1e-8)
        
        deltaPlus1 = deltaPlus(resPlus.x)
        deltaMinus1 = deltaMinus(resMinus.x)
        
        
        
        if deltaPlus1 > deltaMinus1:
            p_chi_x = resMinus.x[0]
            y = M**2 + 4*(Pxk*p_chi_x*M + Pxk*Pxk*(M_Neutralino*M_Neutralino))
            if y < 0:
                y = 0
            p_chi_y = ((M*Pyk + 2*Pxk*Pyk*p_chi_x)/(2*Pxk*Pxk) - (Pftk*sqrt(y))/(2*Pxk*Pxk))
        else:
            p_chi_x = resPlus.x[0]
            y = M**2 + 4*(Pxk*p_chi_x*M + Pxk*Pxk*(M_Neutralino*M_Neutralino))
            if y < 0:
                y = 0
            p_chi_y = ((M*Pyk + 2*Pxk*Pyk*p_chi_x)/(2*Pxk*Pxk) + (Pftk*sqrt(y))/(2*Pxk*Pxk))
            
        p_chi_t = sqrt(p_chi_x*p_chi_x + p_chi_y*p_chi_y)
        mu = 0.5 * M + Pxk*p_chi_x + Pyk*p_chi_y
        p_chi_z_1 = (mu*Pzk)/(Pftk*Pftk)
        p_chi_z_2 = (mu*Pzk)/(Pftk*Pftk)
        chiVec.SetPx(p_chi_x)
        chiVec.SetPy(p_chi_y)
    
    if abs(p_chi_z_1)<abs(p_chi_z_2):
        chiVec.SetPz(p_chi_z_2)
    else:
        chiVec.SetPz(p_chi_z_1)
    
    
    chiVec.SetE(sqrt(chiVec.Px()*chiVec.Px() + chiVec.Py()*chiVec.Py() + chiVec.Pz()*chiVec.Pz() + M_Neutralino**2))
    
    StopVec = ROOT.TLorentzVector()
    StopVec = lepVec + chiVec + BVec
    
    return StopVec



def StopEnergy1(c):
    StopVec = StopVector1(c)
    return StopVec.E()*0.001

def StopEta_abs1(c):
    StopVec = StopVector1(c)
    return abs(StopVec.Eta())

def StopRapidity1(c):
    StopVec = StopVector1(c)
    return abs(StopVec.Rapidity())

def StopMass1(c):
    StopVec = StopVector1(c)
    return StopVec.M()

def Stop_resting_Lepton_angle1(c):
    StopVec = StopVector1(c)
    lepVec = ROOT.TLorentzVector()
    lepVec.SetPtEtaPhiE(c.GetLeaf('lep_pt').GetValue(0) *0.001, c.GetLeaf('lep_eta').GetValue(0), c.GetLeaf('lep_phi').GetValue(0), c.GetLeaf('lep_e').GetValue(0) *0.001)
    betaX = -((StopVec.Px())/(StopVec.E()))
    betaY = -((StopVec.Py())/(StopVec.E()))
    betaZ = -((StopVec.Pz())/(StopVec.E()))
    lepVec.Boost(betaX,betaY,betaZ)
    angle = lepVec.Angle(StopVec.Vect())
    return angle 




    
    
    
    