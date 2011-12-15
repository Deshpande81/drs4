#!/usr/bin/env python
import drs4Event,eventPlotter, dataAnalysis
from xml.sax import make_parser, ContentHandler
import sys


if __name__ == '__main__':
       p = make_parser()
       outputfile = sys.argv[1].split('.xml')[0]+'.root'
       print outputfile
       data = dataAnalysis.drs4Analyzer(outputfile, False)
       p.setContentHandler( drs4Event.drs4Event(  data ) )
       p.parse(sys.argv[1])
       data.write()
       data.close()
       