#!/usr/bin/env python

"""Usage:
   soc_sci_maps_build_manfest <digital_record_id>

Pipe a MarcXML string into this command to produce a IIIF manifest file for the
Social Scientists Maps Collection.
"""

import csv, io, json, os, paramiko, re, sys
import xml.etree.ElementTree as ElementTree
from classes import SocSciMapsIIIFManifest
from docopt import docopt
from pymarc import MARCReader

# switch it so this takes a bib number.

def main():
    options = docopt(__doc__)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        os.environ['SOLR_ACCESS_DOMAIN'],
        username=os.environ['SOLR_ACCESS_USERNAME'],
        password=os.environ['SOLR_ACCESS_PASSWORD']
    )

    # request the digital record
    url = 'http://vfsolr.uchicago.edu:8080/solr/biblio/select?q=id:{}'.format(str(options['<digital_record_id>']))
    _, ssh_stdout, _ = ssh.exec_command('curl "{}"'.format(url))
    data = json.loads(ssh_stdout.read())
    fullrecord = data['response']['docs'][0]['fullrecord']

    with io.BytesIO(fullrecord.encode('utf-8')) as fh:
        reader = MARCReader(fh)
        for record in reader:
            digital_record = record

    # get an oclc number for the print record
    oclc_num = digital_record['776']['w'].replace('(OCoLC)', '')

    # request the print record
    url = 'http://vfsolr.uchicago.edu:8080/solr/biblio/select?q=oclc_num:{}'.format(str(oclc_num))
    _, ssh_stdout, _ = ssh.exec_command('curl "{}"'.format(url))
    data = json.loads(ssh_stdout.read())
    fullrecord = data['response']['docs'][0]['fullrecord']

    with io.BytesIO(fullrecord.encode('utf-8')) as fh:
        reader = MARCReader(fh)
        for record in reader:
            print_record = record

    sys.stdout.write(str(SocSciMapsIIIFManifest(digital_record, print_record)))

if __name__ == '__main__':
    main()
