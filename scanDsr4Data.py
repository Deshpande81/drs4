#!/usr/bin/env python
import drs4Event
from xml.sax import make_parser, ContentHandler
import sys
import eventPlotter


if __name__ == '__main__':
       p = make_parser()
       p.setContentHandler(drs4Event.drs4Event( eventPlotter.plotter() ))
       p.parse(sys.argv[1])
       