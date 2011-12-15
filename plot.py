#!/usr/bin/env python
import ROOT
import numpy as np

f1 = ROOT.TFile('data/2011.12.14.15:38.root')
f2 = ROOT.TFile('data/2011.12.14.15:51.root')
f3 = ROOT.TFile('data/2011.12.14.16:03.root')


p1c1 = f1.Get('CHN1')
p1c2 = f1.Get('CHN2')
p1c1.AddFriend(p1c2)
p2c1 = f2.Get('CHN1')
p2c2 = f2.Get('CHN2')
p2c1.AddFriend(p1c2)
p3c1 = f3.Get('CHN1')
p3c2 = f3.Get('CHN2')
p3c1.AddFriend(p3c2)


hists = {}
hists['p1c1amp'] = ROOT.TH1D('p1c1amp','p1c1amp', 500, 0, 500e3)
hists['p1c2amp'] = ROOT.TH1D('p1c2amp','p1c2amp', 500, 0, 500e3)
hists['p1t1minust2'] = ROOT.TH1D('p1t1minust2','p1t1minust2', 1000, -500, 500)
hists['p2c1amp'] = ROOT.TH1D('p2c1amp','p1c1amp', 500, 0, 500e3)
hists['p2c2amp'] = ROOT.TH1D('p2c2amp','p1c2amp', 500, 0, 500e3)
hists['p2t1minust2'] = ROOT.TH1D('p2t1minust2','p2t1minust2', 1000, -500, 500)
hists['p3c1amp'] = ROOT.TH1D('p3c1amp','p1c1amp', 500, 0, 500e3)
hists['p3c2amp'] = ROOT.TH1D('p3c2amp','p1c2amp', 500, 0, 500e3)
hists['p3t1minust2'] = ROOT.TH1D('p3t1minust2','p3t1minust2', 1000, -500, 500)


a1 = np.zeros(1, dtype=float)
t1 = np.zeros(1, dtype=float)
a2 = np.zeros(1, dtype=float)
t2 = np.zeros(1, dtype=float)

p1c1.SetBranchAddress('a', a1)
p1c1.SetBranchAddress('t', t1)
p1c2.SetBranchAddress('a', a2 )
p1c2.SetBranchAddress('t', t2 )
for entry in p1c1:
  #print a1[0], t1[0]
  hists['p1c1amp'].Fill(-1*a1[0])
  hists['p1c2amp'].Fill(-1*a2[0])
  hists['p1t1minust2'].Fill(t1[0]-t2[0])

#___
p2c1.SetBranchAddress('a', a1)
p2c1.SetBranchAddress('t', t1)
p2c2.SetBranchAddress('a', a2 )
p2c2.SetBranchAddress('t', t2 )
for entry in p2c1:
  #print a1[0], t1[0]
  hists['p2c1amp'].Fill(-1*a1[0])
  hists['p2c2amp'].Fill(-1*a2[0])
  hists['p2t1minust2'].Fill(t1[0]-t2[0])

#__
p3c1.SetBranchAddress('a', a1)
p3c1.SetBranchAddress('t', t1)
p3c2.SetBranchAddress('a', a2 )
p3c2.SetBranchAddress('t', t2 )
for entry in p3c1:
  #print a1[0], t1[0]
  hists['p3c1amp'].Fill(-1*a1[0])
  hists['p3c2amp'].Fill(-1*a2[0])
  hists['p3t1minust2'].Fill(t1[0]-t2[0])

fout = ROOT.TFile('outhists.root', 'recreate')
for key in hists.iterkeys():
  hists[key].Write()
  
fout.Close()
