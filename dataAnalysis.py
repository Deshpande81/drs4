#!/usr/bin/env python

from ROOT import *
import numpy as np
import sys
import matplotlib.pyplot as plt
import scipy.signal as sig


class drs4Analyzer(object):
  '''
    This class uses the digital pulse processing tools found in the KData software package
    Please email adam.cox@kit.edu for access to KData tools if you wish to use these.
    However, you could also look into using the scipy pulse processing tools. 
  '''
  def __init__(self, outputFile, pause=False):
    self.data = {}
    self.file = TFile(outputFile,'recreate')
    self.pause = pause
    self.trap = KTrapezoidalFilter()
    self.trap.SetParams(25, 10, 60)
    self.bas = KBaselineRemoval()
    # self.pdproto = KPeakDetectorProto()
    #     self.pdproto.SetPolarity(-1)
    #     self.pdproto.SetDecayTimeConstant(30)
    #     self.pdproto.AddFilteringProcess(10, 0, 0.5,  1,  1, true,   true, false)
    #     self.pdproto.AddFilteringProcess(5, 0, 1.2, 1, 0, false, true, true)
    #     self.pdproto.AddFilteringProcess(3, 0, 1.5, 1, 0, false, true,  true)
        #self.pdproto.AddFilteringProcess(2, 0, 2.0, 1, 0, false, true,  true)
    (b,a) = sig.iirfilter(2,[0.05, 0.2], btype='bandpass')
    self.iir2 = KIIRFourthOrder(a[1], a[2], a[3], a[4], b[0], b[1], b[2], b[3], b[4])
    plt.ion()
    
    
  def write(self):
    self.file.cd()
    for chan in data:
      data[chan]['tree'].Write()
      
  def close(self):
    self.file.Close()
    
  def handleEvent(self, event):
    
    for chan in event.chanData.iterkeys():
      if event.chanData[chan]['misread'] == True:
        return  #skip this event and go to the next...
      
      if(len(event.chanData[chan]['y'])) > 0:
        a = np.array(event.chanData[chan]['y'])
        if np.min(a) < -499.5:
          #print 'saturating pulse found', event.event, event.eventTime
          return  #the pulse saturated the range
        
    if int(event.event) % 100 == 0:
      print 'event', event.event, event.eventTime
    for chan in event.chanData.iterkeys(): 
      if len(event.chanData[chan]['y']) > 0:
        
        if self.data.has_key(chan) == False:
          #print 'creating data storage for channel', chan
          self.data[chan] = {}
          self.data[chan]['ampSingle'] = np.zeros(1, dtype=float) #use these to hold the current data for trees
          self.data[chan]['timeSingle'] = np.zeros(1, dtype=float)
          self.file.cd()
          self.data[chan]['tree'] = TTree(chan,chan)
          self.data[chan]['tree'].Branch('a', self.data[chan]['ampSingle'], 'a/D')
          self.data[chan]['tree'].Branch('t', self.data[chan]['timeSingle'], 't/D')
          self.data[chan]['amp'] = []
          self.data[chan]['time'] = []
      
        trapIn =  std.vector('double')()
        for i in range(len( event.chanData[chan]['y'] )):
          trapIn.push_back( event.chanData[chan]['y'][i] )
        
        #Baseline Removal  
        self.bas.SetInputPulse(trapIn)
        #print 'baseline removal', 
        self.bas.RunProcess()
        
        #Trapezoidal Filter
        self.trap.SetInputPulse(self.bas.GetOutputPulse(), self.bas.GetOutputPulseSize())
        #print 'trapezoidal filter', 
        self.trap.RunProcess()
        trapOut = np.zeros(self.trap.GetOutputPulseSize())
        for i in range(self.trap.GetOutputPulseSize()):
          trapOut[i] = self.trap.GetOutputPulse()[i]
          
        #Bandpass Filter
        self.iir2.SetInputPulse(self.bas.GetOutputPulse(), self.bas.GetOutputPulseSize())
        #print 'iir2 filter', 
        self.iir2.RunProcess()
        iirOut = np.zeros(self.iir2.GetOutputPulseSize())
        for i in range(self.iir2.GetOutputPulseSize()):
          iirOut[i] = self.iir2.GetOutputPulse()[i]
          
          
        #use the bandpass result to find the pulse peak
        minPos = np.argmin(iirOut)
        peakTime = event.chanData[chan]['x'][minPos]
        startPos = minPos + 2*self.trap.GetRiseTime()
        if startPos < len(event.chanData[chan]['x'])-1:
          startTime = event.chanData[chan]['x'][startPos]
          endPos = minPos + 2*self.trap.GetRiseTime() + self.trap.GetFlatTopWidth()/2
          if endPos < len(event.chanData[chan]['x']) -1:
            endTime = event.chanData[chan]['x'][endPos]
            mean = np.mean( trapOut[ startPos: endPos] )
            #print minPos, peakTime, startPos, endPos, startTime, endTime, mean 
            self.data[chan]['time'].append( peakTime )
            self.data[chan]['amp'].append( mean )
            self.data[chan]['ampSingle'][0] = mean
            self.data[chan]['timeSingle'][0] = peakTime
            #print 'filling', self.data[chan]['ampSingle'][0], self.data[chan]['timeSingle'][0]
            self.file.cd()
            self.data[chan]['tree'].Fill()
            #self.file.Write(self.file.GetName(), self.file.kOverwrite)
            #print 'entries', self.data[chan]['tree'].GetEntries()
            
          else:
            pass
            #print 'pulse end position too large. assume no good pulse.', endPos, '>', len(event.chanData[chan]['x'])-1
        else:
          pass
          #print 'pulse start position too large. assume no good pulse.', startPos, '>', len(event.chanData[chan]['x'])-1
          
        
        #from the pulse peak position, use the trap filter output to estimate the amplitude
        
        
        # #PeakDetector
        #         temp = std.vector('double')(self.trap.GetOutputPulseSize(), 0.0)
        #         for i in range(temp.size()):
        #           temp[i] = self.trap.GetOutputPulse()[i]
        #           
        #         self.pdproto.SetInputPulse(temp)
        #         print 'peak detector', self.pdproto.RunProcess()
        #         rem_peaks = self.pdproto.GetRemainingPeaks()
        #         print "Number of peaks: ",  rem_peaks.size()
        #         for i in range(rem_peaks.size()):
        #           print "Peak at ",  event.chanData[chan]['x'][int(rem_peaks[i][0])],  " between ",  event.chanData[chan]['x'][int(rem_peaks[i][1])],  " and ",  event.chanData[chan]['x'][int(rem_peaks[i][2])]
                  
      
        if self.pause:
          plt.subplot(3,1,1)
          plt.cla()
          plt.plot( np.array(event.chanData[chan]['x']), np.array(trapIn))   
          plt.title('Event %s, %s' % (event.event, event.eventTime))
      
          plt.subplot(3,1,2)
          plt.cla()
          plt.plot( np.array(event.chanData[chan]['x']), trapOut)   
          plt.show() 
          
          plt.subplot(3,1,3)
          plt.cla()
          plt.plot( np.array(event.chanData[chan]['x']), iirOut)   
          plt.show() 
      
      
          go = raw_input()  # wait for user to go
          if go == 'q':
            sys.exit(0)
   