def getSeparation(B1, S1):
    ## keeping TMVA definition
    ##  <s2> = (1/2) Int_-oo..+oo { (S^2(x) - B^2(x))/(S(x) + B(x)) dx }
    sep = 0

    S = S1.Clone("S")
    S.Scale(1./S.Integral())
    B = B1.Clone("B")
    B.Scale(1./B.Integral())

    ## sanity checks: signal and background histograms must have same number of bins and same limits
    if S.GetNbinsX() != B.GetNbinsX() or S.GetNbinsX() <= 0 :
        print "signal and bkg samples with different number of bins: S(" + str( S.GetNbinsX() )+ ") B(" + str( B.GetNbinsX() ) + ")"
        return 0

    if S.GetXaxis().GetXmin() != B.GetXaxis().GetXmin() or S.GetXaxis().GetXmax() != B.GetXaxis().GetXmax() or S.GetXaxis().GetXmax() <= S.GetXaxis().GetXmin() :
        print "Edges of histos are not right: Smin(" + str(S.GetXaxis().GetXmin()) + ")  Bmin(" + str( B.GetXaxis().GetXmin() ) + " ) "\
            " Smax(" + str( S.GetXaxis().GetXmax()) + ")  Bmax(" + str(B.GetXaxis().GetXmax())
        return 0

    nstep = S.GetNbinsX()
    intBin = (S.GetXaxis().GetXmax() - S.GetXaxis().GetXmin())/nstep;
    nS = S.GetSumOfWeights()*intBin
    nB = B.GetSumOfWeights()*intBin

    if nS > 0 and nB > 0 :
        for bin in range(0,nstep) :
            s = S.GetBinContent( bin )/nS
            b = B.GetBinContent( bin )/nB
            if s+b>0 : sep +=  0.5*(s - b)*(s - b)/(s + b)
            pass
        sep *= intBin
    else : print "histos with 0 entries: Snb(" + str(nS) + ") Bnb("+ str(nB) + ")"; sep = 0
    return sep


