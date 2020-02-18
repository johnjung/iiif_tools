#!/usr/bin/env python

"""Usage:
   soc_sci_maps_build_collection (--list-by-publication-date | --subject-overview | --subject=<subject>)

This command gets MARCXML from the social scientist maps IIIF_Files
directories and builds an IIIF Collection json document.
"""

import json, os, sys
from docopt import docopt
from metadata_converters import SocSciMapsMarcXmlToDc

def list_by_publication_date():
    collection = {
        '@context': 'http://iiif.io/api/presentation/context.json',
        '@id': 'http://iiif-collection.lib.uchicago.edu/maps/chisoc/chisoc.json',
        '@type': 'sc:Collection',
        'label': 'Maps Digital Collections',
        'description': 'The list of Maps collections from the University of Chicago Library',
        'viewingHint': 'individuals',
        'members': []
    }

    dc_list = []
    d = '/data/digital_collections/IIIF/IIIF_Files/maps/chisoc'

    # because dates appear in multiple formats which don't lend
    # themselves to sorting, this list has been manually sorted
    for i in (
        'G4104-C6-2N3E51-1908-S2',
        'G4104-C6-2L9-1920z-U5',
        'G4104-C6-2N15-1920z-U5',
        'G4104-C6-2H9-1920z-U5',
        'G4104-C6-2N6-1920z-U5',
        'G4104-C6-2W9-1920z-U5',
        'G4104-C6-2B7-1923-U5',
        'G4104-C6-2B8-1923-U5',
        'G4104-C6-2E15-1924-U5',
        'G4104-C6-2E6-1924-U5',
        'G4104-C6-2M2-1924-U5',
        'G4104-C6-2L3-1925-U5',
        'G4104-C6-2W8-1925-U5',
        'G4104-C6E1-1926-C5',
        'G4104-C6-2N3-1927-U5',
        'G4104-C6E625-1920-S5',
        'G4104-C6E625-1927-S5',
        'G4104-C6E625-1930-U5',
        'G4104-C6-2W9Q4-1930z-U5',
        'G4104-C6-1933-U5-a',
        'G4104-C6-1933-U5-b',
        'G4104-C6-1933-U5-c',
        'G4104-C6-1933-U5-d',
        'G4104-C6-1933-U5-g',
        'G4104-C6-1933-U5-h',
        'G4104-C6-1933-U5-i',
        'G4104-C6-1933-U5-j',
        'G4104-C6-1933-U5-k',
        'G4104-C6-1933-U5-l',
        'G4104-C6-1933-U5-m',
        'G4104-C6-1933-U5-e',
        'G4104-C6-1933-U5-f',
        'G4104-C6-1933-U5-n',
        'G4104-C6-1933-U5-o',
        'G4104-C6E625-1910-R4',
        'G4104-C6E625-1930-R4',
        'G4104-C6E625-1933-N2',
        'G4104-C6-1933-U5-p',
        'G4104-C6E625-1926-T5',
        'G4104-C6E1-1940-U55',
        'G4104-C6P3-1940-M3',
        'G4104-C6P3-1940z-P7',
        'G4104-C6P3-1943-M2',
        'G4104-C6P3-1943-M21',
        'G4104-C6-2H9E11-1956-T3',
    ):
        x = open('{0}/{1}/{1}.xml'.format(d, i))
        dc = SocSciMapsMarcXmlToDc(x.read())
        collection['members'].append({
            '@type': 'sc:Manifest',
            '@id': 'https://iiif-manifest.lib.uchicago.edu/maps/chisoc/{0}/{0}.json'.format(i),
            'viewingHint': 'multi-part',
            'label': dc.title[0]
        })
    return json.dumps(collection) + '\n'

def main():
    options = docopt(__doc__)

    if options['--list-by-publication-date']:
        sys.stdout.write(list_by_publication_date())

if __name__ == '__main__':
    main()
