#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Belle II Hands-on analysis tutorials.  February 2017.
Enough RooFit to be dangerous

Part 2) Running the minimisation interactively and getting hold of the NLL
(at the minimum)

"""

__author__ = "Sam Cunliffe"
__email__ = "samuel.cunliffe@pnnl.gov"

import ROOT as r

# turns off popup plots
r.gROOT.SetBatch(True)

# a copy of the model from exercise 1b
mBC = r.RooRealVar('B0_mbc', 'm_{MC}', 5.2, 5.29, 'GeV/c^{2}')

# signal model
mB0 = r.RooRealVar('mB0', 'm_{B^0}', 5.280, 5.1, 5.3, 'GeV/c^{2}')      # the mass of the B0 meson
gB0 = r.RooRealVar('gB0', '#Gamma_{B^0}', 0.003, 0.0001, 0.015, 'GeV/c^{2}')   # the width of the B0 meson
alp = r.RooRealVar('alp', '#alpha_{CB}', 1.3, 0.1, 5)
ncb = r.RooRealVar('ncb', 'n_{CB}', 15)
sig = r.RooCBShape('sig', 'signal component', mBC, mB0, gB0, alp, ncb)

# background model
mCt = r.RooRealVar('mCt', 'm_{cutoff}', 5.29, 5.2, 5.3, 'GeV/c^{2}')
crv = r.RooRealVar('crv', 'c_{curvature}', -20, -80, -1)
bkg = r.RooArgusBG('bkg', 'background component', mBC, mCt, crv)

# signal + background
nsg = r.RooRealVar('nsg', 'n_{s}', 7000, 10, 10000)
nbg = r.RooRealVar('nbg', 'n_{b}', 3000, 10, 10000)
pdf = r.RooAddPdf('pdf', 'two component model', r.RooArgList(sig, bkg), r.RooArgList(nsg, nbg))

# get the data in a TTree format
fi = r.TFile('../fitme.root', 'READ')
tr = r.TTree()
fi.GetObject('BtoKstG', tr)

# get the data in RooFit land
rds = r.RooDataSet('data', 'B#rightarrow K^{*}#gamma simulation', tr, r.RooArgSet(mBC))

# create the NLL
nll = pdf.createNLL(rds, r.RooFit.Extended(True))

# create a minimiser instance
minuit = r.RooMinuit(nll)
minuit.setStrategy(2)
#minuit.setVerbose(True)
minuit.migrad()
#minuit.minos()

# call HESSE to calculate the error matrix
minuit.hesse()

# now plot the NLL at the fitted minimum
canvas = r.TCanvas()
nsg_plot = nsg.frame()
nll.plotOn(nsg_plot)
#nsg_plot.SetMaximum(-70000)
nsg_plot.Draw()
canvas.SaveAs('nll.pdf')
