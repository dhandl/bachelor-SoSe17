#include <iostream>
#include "TTree.h"
#include "TFile.h"

#define ADDBRANCH

#define FAST

int main() {

  TString oldtreename = "powheg_ttbar_Nom";

  //TFile* oldfile = new TFile("/project/etp3/dhandl/samples/TOPQ1/mc15c/v1/TOPQ1_ttbar_PWGHWGpp_AF2_nonallhad.root","READ");
  TFile* oldfile = new TFile("/afs/cern.ch/work/d/dhandl/public/Stop1L/default_moriond17/powheg_ttbar/mc15_13TeV.407012.PowhegPythiaEvtGen_P2012CT10_ttbarMET200_hdamp172p5_nonAH.DAOD_SUSY5.root","READ");  
  
  TTree* oldtree = (TTree*)oldfile->Get(oldtreename);

  Float_t lep_pt;
  Float_t met;
  Float_t jet1_pt;
  
  oldtree->SetBranchAddress("lep_pt[0]", &lep_pt);
  oldtree->SetBranchAddress("met", &ttbar_eta);
  oldtree->SetBranchAddress("jet_pt[0]", &jet1_pt);

  //TFile* newfile = new TFile("/project/etp3/dhandl/samples/TOPQ1/mc15c/v1/TOPQ1_ttbar_PWGHWGpp_AF2_nonallhad_addRapidity.root", "RECREATE");
  TFile* newfile = new TFile("ttbar_test.root","RECREATE");

#ifdef ADDBRANCH
  TTree* newtree = oldtree->CloneTree(0); // Don't fill yet (0 entries)

  std::cout << newtree->GetEntries() << std::endl;

  Float_t sum_pt;
  newtree->Branch("sum_pt", &sum_pt, "sum_pt/F");

  // now fill (newtree is connected to oldtree)
  for (int i=0; i<oldtree->GetEntries(); i++) {
    if (i%100000 == 0) {
      std::cout << i << "/" << oldtree->GetEntries() << std::endl;
    }
    oldtree->GetEntry(i);
    sum_pt = lep_pt + met + jet1_pt;
    //TLorentzVector* t1 = new TLorentzVector();
    //t1.SetPtEtaPhiM(ttbar_pt, ttbar_eta, ttbar_phi, ttbar_m)
    //std::cout << "Pseudorapidity:" << f << t1.PseudoRapidity() << std::endl;
    //std::cout << "Rapidity:" << f << t1.Rapidity() << std::endl;
    //ttbar_y = t1.Rapidity()
    newtree->Fill();
  }
#else
# ifdef FAST
  TTree* newtree = oldtree->CloneTree(-1, "fast");
# else
  TTree* newtree = oldtree->CloneTree();
# endif
#endif

  newfile->Write();
  newfile->Close();
  oldfile->Close();
}

