#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Belle II Hands-on analysis tutorials.  February 2017.
Enough RooFit to be dangerous

Part 1b) Fit of mBC for a simulation sample.

"""

__author__ = "Sam Cunliffe"
__email__ = "samuel.cunliffe@pnnl.gov"

import ROOT as r

# turns off popup plots
r.gROOT.SetBatch(True)

# get the data in a TTree format
fi = r.TFile('../fitme.root', 'READ')
tr = r.TTree()
fi.GetObject('BtoKstG', tr)
# check we have the tree
print(tr.GetEntries())

# get the data in RooFit land
mBC = r.RooRealVar('B0_mbc', 'm_{MC}', 5.2, 5.29, 'GeV/c^{2}')
rds = r.RooDataSet('data', 'B#rightarrow K^{*}#gamma simulation', tr, r.RooArgSet(mBC))

# always draw plot to make sure things look sane -- saves a lot of time debugging
canvas = r.TCanvas()
plot = mBC.frame()
plot.SetTitle('Plot of the data only')
rds.plotOn(plot)
plot.Draw()
canvas.SaveAs('data-1b.pdf')

# signal model
mB0 = r.RooRealVar('mB0', 'm_{B^0}', 5.280, 5.1, 5.3, 'GeV/c^{2}')      # the mass of the B0 meson
gB0 = r.RooRealVar('gB0', '#Gamma_{B^0}', 0.003, 0.0, 0.015, 'GeV/c^{2}')   # the width of the B0 meson
alp = r.RooRealVar('alp', '#alpha_{CB}', 1.3, 0.1, 5)
ncb = r.RooRealVar('ncb', 'n_{CB}', 15)
sig = r.RooCBShape('sig', 'signal component', mBC, mB0, gB0, alp, ncb)

# background model
mCt = r.RooRealVar('mCt', 'm_{cutoff}', 5.29, 5.2, 5.3, 'GeV/c^{2}')
crv = r.RooRealVar('crv', 'c_{curvature}', -20, -80, -1)
bkg = r.RooArgusBG('bkg', 'background component', mBC, mCt, crv)

# combined model
fsb = r.RooRealVar('fsb', 'n_{s}/(n_{s}+n_{b})', 0.7, 0.0, 1.0)
pdf = r.RooAddPdf('pdf', 'two component model', sig, bkg, fsb)
#nsg = r.RooRealVar('nsg', 'n_{s}', 7000, 0, 10000)
#nbg = r.RooRealVar('nbg', 'n_{b}', 3000, 0, 10000)
#pdf = r.RooAddPdf('pdf', 'two component model', r.RooArgList(sig, bkg), r.RooArgList(nsg, nbg))

# a pre-fitting plot
debug = mBC.frame()
debug.SetTitle('A plot without fit for debugging')
rds.plotOn(debug)
bkg.plotOn(debug)
sig.plotOn(debug)
pdf.plotOn(debug, r.RooFit.LineColor(r.kRed))
debug.Draw()
canvas.SaveAs('pre-fit-1b.pdf')

# run the fit - save output as a RooFitResult
rfr = pdf.fitTo(rds, r.RooFit.Save(True), r.RooFit.Strategy(2)) ###, r.RooFit.Extended(True))

# plot fitted otput
plot.SetTitle('Fitted distribution')
pdf.plotOn(plot, r.RooFit.LineColor(r.kRed))
pdf.plotOn(plot, r.RooFit.Components('sig'), r.RooFit.LineColor(r.kGreen))
pdf.plotOn(plot, r.RooFit.Components('bkg'), r.RooFit.LineColor(r.kBlue))
plot.Draw()
canvas.SaveAs('post-fit-1b.pdf')

# figure out paramters access the value in code
rfr.Print()
pars = rfr.floatParsFinal()
pars.Print()
print(pars[0].getVal(), '+/-', pars[0].getError())

# correlations
cor = rfr.correlationHist()
cor.SetStats(0)
cor.SetTitle('Correlation matrix of parameters')
cor.Draw('textcolz')
canvas.SaveAs('correlations.pdf')
