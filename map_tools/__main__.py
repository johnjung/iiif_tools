#!/usr/bin/env python
"""Usage:
    map_tools -
"""


import sys
from docopt import docopt
from builders import MapIIIFManifest

if __name__=="__main__":
  options = docopt(__doc__)

  if "-" in options:o
    dcxml = sys.stdin.read()

  sys.stdout.write(str(MapIIIFManifest(dcxml)))
