#!/usr/bin/env python
"""Usage:
    iiif_tools -f <path>

Options:
  -h --help     Show this screen.
  -f --file     File path to make manifest from
"""


import sys
from docopt import docopt
from maps_manifest import MapsIIIFManifest

if __name__=="__main__":
  options = docopt(__doc__)
  if "<path>" in options:
  	with open(options['<path>'], 'r') as dcxml:
	  	sys.stdout.write(str(MapsIIIFManifest(dcxml.read())))
  else:
  	dcxml = sys.stdin.read()
  	sys.stdout.write(str(MapsIIIFManifest(dcxml)))
