#!/usr/bin/env python
from xml.sax import ContentHandler

class drs4Event(ContentHandler):

    def __init__(self, delegate):
        ContentHandler.__init__(self)
        self.currentTag = ''
        self.currentChannel = ''
        self.event = ''
        self.horizontalUnit = ''
        self.verticalUnit = ''
        self.eventTime = ''
        self.chanData = {}
        self.chanData['CHN1'] = {}
        self.chanData['CHN2'] = {}
        self.chanData['CHN3'] = {}
        self.chanData['CHN4'] = {}
        self.numEvents = 0
        self.delegate = delegate

    def startElement(self, tag, attributes):
        self.currentTag = tag
        # print 'start', tag
        if tag == 'Event':
            self.numEvents += 1
            self.chanData['CHN1']['x'] = []
            self.chanData['CHN2']['x'] = []
            self.chanData['CHN3']['x'] = []
            self.chanData['CHN4']['x'] = []
            self.chanData['CHN1']['y'] = []
            self.chanData['CHN2']['y'] = []
            self.chanData['CHN3']['y'] = []
            self.chanData['CHN4']['y'] = []
            self.chanData['CHN1']['misread'] = False
            self.chanData['CHN2']['misread'] = False
            self.chanData['CHN3']['misread'] = False
            self.chanData['CHN4']['misread'] = False
            
        elif tag.startswith('CHN'):
            #print 'set current channel', tag
            self.currentChannel = tag

    def endElement(self, tag):
        self.currentTag = False
        # print 'end', tag
        if tag == 'Event':
            self.delegate.handleEvent(self)
            
        elif tag.startswith('CHN'):
            self.currentChannel = ''
        
        
    def characters(self, data):

        # print 'current tag', self.currentTag
        #         print 'data chunk', data
        
        if self.currentTag == 'Serial':
          self.event = data

        if self.currentTag == 'Time':
          self.eventTime = data #could parse this with datetime if wanted to get absolute time for each data point. but its not necessary yet
        
        if self.currentTag == 'HUnit':
          self.horizontalUnit = data
        
        if self.currentTag == 'VUnit':
          self.verticalUnit = data
          
        if self.currentTag == 'Data':
          try:
            ad = [ float(data.split(',')[0]),  float(data.split(',')[1]) ]
            self.chanData[self.currentChannel]['x'].append( ad[0] )
            self.chanData[self.currentChannel]['y'].append( ad[1] )
          except Exception:
            
            self.chanData[self.currentChannel]['misread'] = True
            # print self.currentChannel
            #             print 'data', data
            #             print len(self.chanData[self.currentChannel]['x']), len(self.chanData[self.currentChannel]['y'])
            #             print 'previous point', self.chanData[self.currentChannel]['x'][ len(self.chanData[self.currentChannel]['x']) -1 ], self.chanData[self.currentChannel]['y'][ len(self.chanData[self.currentChannel]['y']) -1 ]
            #             print self.event
            #             print self.eventTime
            #             print self.numEvents
            #print [ float(data.split(',')[0]),  float(data.split(',')[1]) ]
            pass

    def startDocument(self):
        pass

    def endDocument(self):
        print 'the number of files in the document were: ' + str(self.numEvents)