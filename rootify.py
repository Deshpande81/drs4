#!/usr/bin/env python

#from ROOT import *
import numpy as np
import sys
import matplotlib.pyplot as plt
import scipy.signal as sig
from rootpy.tree import Tree, TreeModel
from rootpy.io import open
from rootpy.types import *
import ROOT
import datetime


# define the model
class Event(TreeModel):

    # properties of data 
    date = ULongCol()
    #timefactor = FloatCol()
    #oltfactor = FloatCol()
 
		
    # a collection of pulses
    c1x_val = ROOT.vector("float")
    c1y_val = ROOT.vector("float")
 


class rootifier(object):
  '''
    This class uses the digital pulse processing tools found in the KData software package
    Please email adam.cox@kit.edu for access to KData tools if you wish to use these.
    However, you could also look into using the scipy pulse processing tools. 
  '''
  def __init__(self, outputFile, pause=False):
    self.data = {}
    self.file = open(outputFile,'recreate')
    self.tree = Tree("t", model=Event)
    self.epoch = datetime.datetime(1995, 1, 1)  #jan 1 1995 is ROOT epoch

  def write(self):
    self.file.cd()
    self.tree.write()    

  def close(self):
    self.file.Close()
    
  def handleEvent(self, event):
    #
    # here is where you get each event, which is all four digitized pulses
    # do analysis here, or convert to ROOT file.
    #
    #

    if int(event.event) % 100 == 0:
      print 'event', event.event, event.eventTime

    for chan in event.chanData.iterkeys():
      if event.chanData[chan]['misread'] == True:
        return  #skip this event and go to the next...
        

    try:
      #eventTime = datetime.datetime(event.eventTime)
      tempTime = event.eventTime.split(".")[0]
      eventTime = datetime.datetime.strptime(tempTime,'%Y/%m/%d %H:%M:%S')
      td = eventTime - self.epoch
      self.tree.date = (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6 + int(event.eventTime.split(".")[1])*10**-3
    except:
      print event.eventTime, "is bad"
      pass

    for chan in event.chanData.iterkeys(): 
      if chan == "CHN1":     
        for value in event.chanData[chan]["y"]:
          self.tree.c1y_val.push_back(value)
        for value in event.chanData[chan]["x"]:
          self.tree.c1x_val.push_back(value)
       

    self.tree.fill(reset=True)

