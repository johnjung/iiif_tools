import csv
import re
import xml.etree.ElementTree as ElementTree

class MvolMetadata:
  """helper functions to make collection and manifest files for iiif. 

  Args:
    directory (str): e.g. /Volumes/webdav/...

  """

  def __init__(self, directory):
    self.directory = directory
    self.struct = None
    self.mets = None

  def get_page(self, n):
    """Get a page number from structural metadata.

    Args:
      n(int): object number

    Returns:
      str: page number for this object.
  
    """

    if not self.struct:
      for entry in os.listdir(self.directory):
        if entry.endswith('struct.txt'):
          self.struct = []
          with open(self.directory + '/' + entry, 'r') as f:
            next(f)
            reader = csv.reader(f, delimiter='\t')
            for object, page, milestone in reader:
              self.struct.append([object, page, milestone])
      assert self.struct != None
 
    return self.struct[n][1]

  def get_width(self, n):
    """Get image width. 

    Args:
      n(int): object number

    Returns:
      int: image width
  
    """

    if not self.mets:
      self._load_mets()
      assert self.mets != None

    # get width here. 
    /mets/amdSec/techMD/mdWrap/xmlData

    /mix:mix
      /mix:BasicImageInformation
        /mix:BasicImageCharacteristics
          /mix:imageWidth
    
  def get_height(self, n):
    """Get image height. 

    Args:
      n(int): object number

    Returns:
      int: image height
  
    """

    if not self.mets:
      self._load_mets()
      assert self.mets != None

    # get height here. 

    def _load_mets(self):
      for entry in os.listdir(self.directory):
        if entry.endswith('mets.xml'):
          self.mets = ElementTree.parse(self.directory + '/' + entry)


