#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Belle II Hands-on analysis tutorials.  February 2017.
Enough RooFit to be dangerous

Part 1a) A very simple 1D toy fit of mBC

"""

__author__ = "Sam Cunliffe"
__email__ = "samuel.cunliffe@pnnl.gov"

import ROOT as r

# turns off popup plots
r.gROOT.SetBatch(True)

# RooRealVar
print(help(r.RooRealVar))
mBC = r.RooRealVar('mbc', 'm_{BC}', 5.1, 5.3, 'GeV/c^{2}')
plot = mBC.frame() # creates a RooPlot object (set of axes)
plot.Print()

# let's just draw the (empty) axes
canvas = r.TCanvas()
plot.Draw()
canvas.SaveAs('empty-axes-1a.pdf')

# declare parameters and a model
mB0 = r.RooRealVar('mB0', 'm_{B^0}', 5.280, 'GeV/c^{2}')      # the mass of the B0 meson
gB0 = r.RooRealVar('gB0', '#Gamma_{B^0}', 0.007, 0.0, 0.01, 'GeV/c^{2}')   # the width of the B0 meson
crappy_model = r.RooGaussian('crappy_model', 'simple model', mBC, mB0, gB0)

# always plot the model and look at it before fitting
crappy_model.plotOn(plot)
plot.SetTitle("Overly simplistic model")
canvas.cd()
plot.Draw()
canvas.SaveAs('simple-model-1a.pdf')

# generate a toy MC dataset
dataset = crappy_model.generate(r.RooArgSet(mBC), 1000) # returns a RooDataSet
dataset.Print()

# always plot the data and look at it before fitting
plot.SetTitle("Toy data with the model from which it was generated")
dataset.plotOn(plot)
plot.Draw()
canvas.SaveAs('something-wrong-1a.pdf')

plot.Print() # you'll have to read this to get the pdf name
plot.setInvisible('crappy_model_Norm[mbc]')
crappy_model.plotOn(plot) # normalisation will be fixed
plot.Print()
plot.Draw()
canvas.SaveAs('pre-fit-1a.pdf')

# perform the fit
crappy_model.fitTo(dataset)
crappy_model.plotOn(plot, r.RooFit.LineColor(r.kRed))
plot.Draw()
canvas.SaveAs('post-fit-1a.pdf')
