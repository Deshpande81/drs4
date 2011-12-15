#!/usr/bin/env python

from ROOT import *
import numpy as np
import sys

class drs4Analyzer(object):
  
  def __init__(self, pause=False):
    self.data = {}
    self.pause = pause
    self.trap = KTrapezoidalFilter()
    self.trap.SetParams(30, 10, 50)

  def handleEvent(self, event):
    
    for chan in event.chanData.iterkeys():
      if event.chanData[chan]['misread'] == True:
        return  #skip this event and go to the next...
        
    for chan in event.chanData.iterkeys(): 
      if len(event.chanData[chan]['y']) > 0:
        
        if self.data.has_key(chan) == False:
          self.data[chan] = {}
          self.data[chan]['amp'] = []
          self.data[chan]['time'] = []
      
      trapOut = std.vector('double')()
      trapIn =  std.vector('double')()
      
      for i in range(len( event.chanData[chan]['y'] )):
        trapIn.push_back( event.chanData[chan]['y'][i] )
        trapOut.push_back(0.)
        
      print typeof(trapIn)
      
      self.trap.SetInputPulse(trapIn)
      self.trap.SetOutputPulse(trapOut)
      self.trap.RunProcess()
      trapOut = self.trap.GetOutputPulse()
      
      print trapOut
      print trapOut[0]
      print trapOut.size()
      
      go = raw_input()  # wait for user to go
      if go == 'q':
        sys.exit(0)
   