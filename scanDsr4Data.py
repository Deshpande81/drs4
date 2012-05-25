#!/usr/bin/env python
import drs4Event,eventPlotter, rootify
from xml.sax import make_parser, ContentHandler
import sys


if __name__ == '__main__':
       p = make_parser()
       outputfile = sys.argv[1].split('.xml')[0]+'.root'
       print outputfile
       rootConversion = rootify.rootifier(outputfile, False)
       p.setContentHandler( drs4Event.drs4Event(  rootConversion ) )
       p.parse(sys.argv[1])
       data.write()
       data.close()
       
