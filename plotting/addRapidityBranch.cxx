#include <iostream>
#include "TTree.h"
#include "TFile.h"

#define ADDBRANCH

#define FAST

int main() {

  TString oldtreename = "truth";

  //TFile* oldfile = new TFile("/project/etp3/dhandl/samples/TOPQ1/mc15c/v1/TOPQ1_ttbar_PWGHWGpp_AF2_nonallhad.root","READ");
  TFile* oldfile = new TFile("../AnalysisTop-2.4.6/output.root","READ");  
  
  TTree* oldtree = (TTree*)oldfile->Get(oldtreename);

  Float_t ttbar_pt;
  Float_t ttbar_eta;
  Float_t ttbar_phi;
  Float_t ttbar_m;
  
  oldtree->SetBranchAddress("MC_ttbar_beforeFSR_pt", &ttbar_pt);
  oldtree->SetBranchAddress("MC_ttbar_beforeFSR_eta", &ttbar_eta);
  oldtree->SetBranchAddress("MC_ttbar_beforeFSR_phi", &ttbar_phi);
  oldtree->SetBranchAddress("MC_ttbar_beforeFSR_m", &ttbar_m);

  //TFile* newfile = new TFile("/project/etp3/dhandl/samples/TOPQ1/mc15c/v1/TOPQ1_ttbar_PWGHWGpp_AF2_nonallhad_addRapidity.root", "RECREATE");
  TFile* newfile = new TFile("../AnalysisTop-2.4.6/output_addBranch.root","RECREATE");

#ifdef ADDBRANCH
  TTree* newtree = oldtree->CloneTree(0); // Don't fill yet (0 entries)

  std::cout << newtree->GetEntries() << std::endl;

  Float_t ttbar_y;
  newtree->Branch("MC_ttbar_beforeFSR_y", &ttbar_y, "MC_ttbar_beforeFSR_y/F");

  // now fill (newtree is connected to oldtree)
  for (int i=0; i<oldtree->GetEntries(); i++) {
    if (i%100000 == 0) {
      std::cout << i << "/" << oldtree->GetEntries() << std::endl;
    }
    oldtree->GetEntry(i);
    TLorentzVector* t1 = new TLorentzVector();
    t1.SetPtEtaPhiM(ttbar_pt, ttbar_eta, ttbar_phi, ttbar_m)
    std::cout << "Pseudorapidity:" << f << t1.PseudoRapidity() << std::endl;
    std::cout << "Rapidity:" << f << t1.Rapidity() << std::endl;
    ttbar_y = t1.Rapidity()
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

