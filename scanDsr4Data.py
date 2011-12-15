#!/usr/bin/env python
import drs4Event,eventPlotter, dataAnalysis
from xml.sax import make_parser, ContentHandler
import sys


if __name__ == '__main__':
       p = make_parser()
       data = dataAnalysis.drs4Analyzer(sys.argv[1].strip('.xml')[0]+'.root', False)
       p.setContentHandler( drs4Event.drs4Event(  data ) )
       p.parse(sys.argv[1])
       data.file.cd()
       data.file.Write()
       data.file.Close()
       