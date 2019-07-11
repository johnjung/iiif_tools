#!/usr/bin/env python
"""Usage:
    iiif_tools -
    iiif_tools -f <path>

Options:
  -h --help     Show this screen.
  -f --file     File path to make manifest from
  -             Take input from the terminal
"""


import sys
from docopt import docopt
from maps_manifest import MapsIIIFManifest

if __name__=="__main__":
  options = docopt(__doc__)

  if options['--file']:
  	with open(options['<path>'], 'r') as file:
  		dcxml = file.read()
  elif options['-']:
  	dcxml = sys.stdin.read()
  else:
  	sys.exit()
  sys.stdout.write(str(MapsIIIFManifest(dcxml)))
  sys.exit()