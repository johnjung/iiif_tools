#!/usr/bin/env python
"""Usage:
    iiif_tools -
"""


import sys
from docopt import docopt
from builders import MapsIIIFManifest

if __name__=="__main__":
  options = docopt(__doc__)

  if "-" in options:
    dcxml = sys.stdin.read()

  sys.stdout.write(str(MapsIIIFManifest(dcxml)))
