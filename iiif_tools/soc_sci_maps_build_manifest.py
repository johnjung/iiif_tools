#!/usr/bin/env python

"""Usage:
   soc_sci_maps_build_manfest -

Pipe a MarcXML string into this command to produce a IIIF manifest file for the
Social Scientists Maps Collection.
"""

import csv, json, os, re, sys
import xml.etree.ElementTree as ElementTree
from .classes import SocSciMapsIIIFManifest
from docopt import docopt

def main():
    sys.stdout.write(
        str(
            SocSciMapsIIIFManifest(
                '<collection>{}</collection>'.format(sys.stdin.read())
            )
        )
    )

if __name__ == '__main__':
    main()
