import argparse
import getpass
import json
import os
import owncloud
import re
import sys

from mvol_identifier import MvolIdentifier

class IIIFCollectionYear:
  """Make a collection for a year of Campus Publications (mvol) data. 
     e.g. https://iiif-collection.lib.uchicago.edu/mvol/0004/mvol-0004-1930.json
  
  """

  def __init__(self, oc, title, identifier, description, attribution, directory):
    self.oc = oc
    self.title = title
    self.identifier = identifier
    self.description = description
    self.attribution = attribution
    self.directory = directory

    self.mvolidentifier = MvolIdentifier(self.identifier)
    self.year = self.mvolidentifier.get_year()

  def data(self):
    collection = {
      'label': '%s, %s' % (self.title, '-'.join(self.identifier.split('-')[2:])),
      '@id': self.mvolidentifier.collection_url(),
      '@context': 'https://iiif.io/api/presentation/2/context.json',
      '@type': 'sc:Collection',
      'description': self.description,
      'attribution': self.attribution,
      'viewingHint': 'multi-part',
      'members': []
    }

    months = set()
    for entry in self.oc.list(self.directory):
      if not entry.file_type == 'dir':
        continue

      pieces = entry.path.split('/')
      if entry.path[-1:] == '/':
        pieces.pop()

      entry_filename = pieces.pop()

      if re.match(r"^[0-9]{4}$", entry_filename):
        months.add(entry_filename[:2])

    for month in sorted(list(months)):
      month_mvolidentifier = MvolIdentifier(self.identifier + '-' + month)
      collection['members'].append({
        'label': '%s, %s-%s' % (self.title, self.year, month),
        '@id': month_mvolidentifier.collection_url(),
        '@type': 'sc:Collection',
        'viewingHint': 'multi-part'
      })

    return collection

if __name__ == '__main__':

  def mvol_year(s):
    r = re.compile(r"mvol-\d{4}-\d{4}")
    if not r.match(s):
      raise argparse.ArgumentTypeError
    return s

  parser = argparse.ArgumentParser()
  parser.add_argument("username", help="WebDAV username.")
  parser.add_argument("identifier", help="e.g. mvol-0004-1931", type=mvol_year)
  parser.add_argument("directory", help="e.g. /IIIF_Files/...")
  args = parser.parse_args()

  try:
    oc = owncloud.Client(os.environ['WEBDAV_CLIENT'])
  except KeyError:
    sys.stderr.write("WEBDAV_CLIENT environmental variable not set.\n")
    sys.exit()

  password = getpass.getpass('WebDAV password: ')
  oc.login(args.username, password)

  if args.identifier.startswith('mvol-0004'):
    title = 'Daily Maroon'
    description = 'A newspaper produced by students of the University of Chicago. Published 1900-1942 and continued by the Chicago Maroon.'
  else:
    raise NotImplementedError

  print(
    json.dumps(
      IIIFCollectionYear(
        oc,
        title,
        args.identifier,
        description,
        'University of Chicago',
        args.directory).data(),
      indent=4,
      sort_keys=True))
