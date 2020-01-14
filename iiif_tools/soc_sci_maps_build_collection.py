#!/usr/bin/env python

"""Usage:
   soc_sci_maps_build_collection

This command gets MARCXML from the social scientist maps IIIF_Files
directories and builds an IIIF Collection json document.
"""

import json, os, sys
from metadata_converters import SocSciMapsMarcXmlToDc

def main():
    collection = {
        '@context': 'http://iiif.io/api/presentation/context.json',
        '@id': 'http://iiif-collection.lib.uchicago.edu/maps/chisoc/chisoc.json',
        '@type': 'sc:Collection',
        'label': 'Maps Digital Collections',
        'description': 'The list of Maps collections from the University  of Chicago Library',
        'viewingHint': 'individuals',
        'members': []
    }

    d = '/data/digital_collections/IIIF/IIIF_Files/maps/chisoc'
    for f in os.scandir(d):
        x = open('{0}/{1}/{1}.xml'.format(d, f.name))
        dc = SocSciMapsMarcXmlToDc(x.read())
        
        collection['members'].append({
            '@type': 'sc:Manifest',
            '@id': 'https://iiif-manifest.lib.uchicago.edu/maps/chisoc/{0}/{0}.json'.format(f.name),
            'viewingHint': 'multi-part',
            'label': dc.title[0]
        })

    sys.stdout.write(json.dumps(collection) + '\n')

if __name__ == '__main__':
    main()
