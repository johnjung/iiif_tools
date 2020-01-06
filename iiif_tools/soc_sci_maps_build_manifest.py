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
    root = ElementTree.fromstring(sys.stdin.read())
    if root.tag == '{http://www.loc.gov/MARC21/slim}collection':
        sys.stdout.write(
            str(
                SocSciMapsIIIFManifest(
                    ElementTree.tostring(root, encoding='utf-8')
                )
            )
        )
    else:
        raise NotImplementedError

if __name__ == '__main__':
    main()
