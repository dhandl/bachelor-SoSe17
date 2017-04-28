#------------------------------------------------------------------------------
def mkcdf(hist, minbin=1):
    c = [0.0]*(hist.GetNbinsX()-minbin+2)
    j=0
    for ibin in xrange(minbin, hist.GetNbinsX()+1):
        c[j] = c[j-1] + hist.GetBinContent(ibin)
        j += 1
    c[j] = hist.Integral()
    return c

def mkroc(name, hsig, hbkg, lcolor=kBlue, lwidth=2, ndivx=505, ndivy=505):
    from array import array
    csig = mkcdf(hsig)
    cbkg = mkcdf(hbkg)
    npts = len(csig)
    esig = array('d')
    ebkg = array('d')
    for i in xrange(npts):
        esig.append(1 - csig[npts-1-i])
        ebkg.append(1 - cbkg[npts-1-i])
    g = TGraph(npts, ebkg, esig)
    g.SetName(name)
    g.SetLineColor(lcolor)
    g.SetLineWidth(lwidth)

    g.GetXaxis().SetTitle("#font[12]{#epsilon_{b}}")
    g.GetXaxis().SetLimits(0,1)

    g.GetYaxis().SetTitle("#font[12]{#epsilon_{s}}")
    g.GetHistogram().SetAxisRange(0,1, "Y");

    g.GetHistogram().SetNdivisions(ndivx, "X")
    g.GetHistogram().SetNdivisions(ndivy, "Y")
    return g
