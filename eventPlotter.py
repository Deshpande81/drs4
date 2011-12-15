#!/usr/bin/env python

import matplotlib.pyplot as plt
import numpy as np
import sys

class plotter(object):
  
  def __init__(self, pause=True):
    self.figObj = plt.figure()
    plt.ion()
    self.pause = pause
    
  def handleEvent(self, event):
    plt.cla()
    npArrs = {}
    for chan in event.chanData.iterkeys():
      if event.chanData[chan]['misread'] == True:
        return  #skip this event and go to the next... 
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
    