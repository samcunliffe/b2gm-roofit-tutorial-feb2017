#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Belle II Hands-on analysis tutorials.  February 2017.
Enough RooFit to be dangerous

Part 2) Multidimensional fitting and data visualisation

"""

__author__ = "Sam Cunliffe"
__email__ = "samuel.cunliffe@pnnl.gov"

import ROOT as r

# turns off popup plots
r.gROOT.SetBatch(True)

# independent variables
x = r.RooRealVar('x', 'x', -1.0, 1.0)
y = r.RooRealVar('y', 'y', -1.0, 1.0)

# model in x
wx = r.RooRealVar('wx', '#sigma_{x}', 0.1, 0.001, 0.5)
mx = r.RooRealVar('mx', '#sigma_{x}', 0.0)
gsx = r.RooGaussian('gsx', 'Gaussian model in x', x, mx, wx)

# model in y
ky = r.RooRealVar('ky', 'k_{y}', -2, -5, -0.1)
exy = r.RooExponential('exy', 'Exponential model in y', y, ky)

# combine
pdf = r.RooProdPdf('pdf', 'simple 2D pdf', gsx, exy)

# 2D plot of the model
canvas = r.TCanvas()
hpdf = pdf.createHistogram('x,y',50,50)
hpdf.Draw('surf')
hpdf.SetStats(0)
canvas.SaveAs('2D-pdf-pre-fit.pdf')

# generate some data
import time
st = time.time()
toydata = pdf.generate(r.RooArgSet(x, y), 100000)
print(time.time() - st, 'sec')

# plot the data
hds = toydata.createHistogram(x,y,50,50) # this will create a 'regular' TH2D
hds.Draw('lego')
hpdf.SetStats(0)
canvas.SaveAs('2D-data.pdf')

# fit
pdf.fitTo(toydata)

# check fitted projections
xfr = x.frame() # RooPlots -- will be projections
yfr = y.frame()
xfr.SetTitle('Fitted projection in x')
yfr.SetTitle('Fitted projection in y')
toydata.plotOn(xfr)
toydata.plotOn(yfr)
pdf.plotOn(xfr)
pdf.plotOn(yfr)

yfr.Draw()
canvas.SaveAs('post-fit-y-proj-2.pdf')

xfr.Draw()
canvas.SaveAs('post-fit-x-proj-2.pdf')
