import io
import json
import unittest
import urllib.request
import os

from mvol_collection_year import IIIFCollectionYear
from mvol_collection_month import IIIFCollectionMonth
from mvol_manifest import IIIFManifest
from mvol_validator import _validate_dc_xml_file, _validate_mets_xml_file, _validate_file_notempty, _validate_struct_txt_file

from pathlib import Path

def ordered(obj):
  if isinstance(obj, dict):
    return sorted((k, ordered(v)) for k, v in obj.items())
  if isinstance(obj, list):
    return sorted(ordered(x) for x in obj)
  else:
    return obj

class TestIIIFTools(unittest.TestCase):

  '''
  def test_iiif_collection_year(self): 
    url = 'http://iiif-collection.lib.uchicago.edu/mvol/0004/mvol-0004-1930.json'
    live_data = json.load(urllib.request.urlopen(url))
    test_data = IIIFCollectionYear(
      'Daily Maroon',
      'mvol-0004-1930',
      'A newspaper produced by students of the University of Chicago. Published 1900-1942 and continued by the Chicago Maroon.',
      'University of Chicago',
      '/Volumes/webdav/IIIF_Files/mvol/0004/1930'
    ).data()
    self.assertTrue(ordered(live_data) == ordered(test_data))

  def test_iiif_collection_month(self):
    url = 'http://iiif-collection.lib.uchicago.edu/mvol/0004/mvol-0004-1930-01.json'
    live_data = json.load(urllib.request.urlopen(url))
    test_data = IIIFCollectionMonth(
      'Daily Maroon',
      'mvol-0004-1930-01',
      'A newspaper produced by students of the University of Chicago. Published 1900-1942 and continued by the Chicago Maroon.',
      'University of Chicago',
      '/Volumes/webdav/IIIF_Files/mvol/0004/1930'
    ).data()
    self.assertTrue(ordered(live_data) == ordered(test_data))

  def test_iiif_manifest(self):
    url = 'http://iiif-manifest.lib.uchicago.edu/mvol/0004/1929/0103/mvol-0004-1929-0103.json'
    live_data = json.load(urllib.request.urlopen(url))
    test_data = IIIFManifest(
      'Daily Maroon',
      'mvol-0004-1929-0103',
      'A newspaper produced by students of the University of Chicago. Published 1900-1942 and continued by the Chicago Maroon.',
      'University of Chicago Library',
      '/Volumes/webdav/IIIF_Files/mvol/0004/1929'
    ).data()
    self.assertTrue(ordered(live_data) == ordered(test_data))
  '''


if __name__ == '__main__':
  unittest.main()
