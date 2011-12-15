#!/usr/bin/env python

from ROOT import KTrapezoidalFilter
import sys

class drs4Analyzer(object):
  
  def __init__(self, pause=True):
    self.energy = {}
    
  def handleEvent(self, event):
    
    for chan in event.chanData.iterkeys():
      if event.chanData[chan]['misread'] == True:
        return  #skip this event and go to the next...
        
    for chan in event.chanData.iterkeys(): 
      if len(event.chanData[chan]['x']) > 0:
        print 'plotting', chan
        plt.plot( np.array(event.chanData[chan]['x']),  np.array(event.chanData[chan]['y']), label = chan)
    
    plt.title('Event %s, %s' % (event.event, event.eventTime))
    plt.show()
    
    if self.pause == True:
      print 'hit enter to go to next event. q to quit'
      go = raw_input()
      if go == 'q':
        sys.exit(1)
