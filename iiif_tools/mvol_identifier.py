import re

class MvolIdentifier:
  """helper functions to make collection and manifest files for iiif. 

  Args:
    identifier (str): e.g. mvol-0004-1930, mvol-0004-1930-01, mvol-0004-1930-0106

  """

  def __init__(self, identifier):
    self.identifier = identifier

  def collection_url(self):
    """Build a uchicago IIIF collection URL for an mvol identifier. 
    Takes identifiers like mvol-0004-1930. 
   
    Returns:
      str: An iiif-collection url, e.g. http://iiif-collection.lib.uchicago.edu/mvol/0004/mvol-0004-1930.json

    """

    pieces = self.identifier.split("-")
    if re.match(r"^mvol-\d{4}-\d{4}$", self.identifier) or re.match(r"^mvol-\d{4}-\d{4}-\d{2}$", self.identifier):
      return "http://iiif-collection.lib.uchicago.edu/" + "/".join(pieces[:2]) + "/" + self.identifier + ".json"
    else:
      raise ValueError
  
  def manifest_url(self):
    """Build a uchicago IIIF manifest URL for an mvol identifier. 
    Takes identifiers like mvol-0004-1930-0103
  
    Returns:
      str: An iiif-collection url, e.g. https://iiif-manifest.lib.uchicago.edu/mvol/0004/1930/0103/mvol-0004-1930-0103.json
   
    """
  
    pieces = self.identifier.split("-")
    if re.match(r"^mvol-\d{4}-\d{4}-\d{4}$", self.identifier):
      return "https://iiif-manifest.lib.uchicago.edu/" + "/".join(pieces) + "/" + self.identifier + ".json"
    else:
      return ValueError

  def sequence_url(self):
    """Build a uchicago IIIF sequence URL for an mvol identifier. 
    Takes identifiers like mvol-0004-1930-0103
  
    Returns:
      str: An iiif-collection url, e.g. https://iiif-manifest.lib.uchicago.edu/mvol/0004/1930/0103/mvol-0004-1930-0103.json
   
    """

    pieces = self.identifier.split("-")
    if re.match(r"^mvol-\d{4}-\d{4}-\d{4}$", self.identifier):
      return "https://iiif-manifest.lib.uchicago.edu/" + "/".join(pieces) + "/" + self.identifier + ".json"
    else:
      return ValueError
  
  def get_year(self):
    """Get the year from an mvol identifier. 
    
    Returns:
      str: a year, e.g. 1930
   
    """
  
    return self.identifier.split("-")[2]
  
  def get_month(self):
    """Get the month from an mvol identifier. 
    Takes identifiers in the form mvol-0004-1930-01 or mvol-0004-1930-0106
    
    Returns:
      str: a month, e.g. 01
   
    """

    if re.match(r"^mvol-\d{4}-\d{4}-\d{2,4}$", self.identifier):
      return self.identifier.split("-")[3][:2]
    else:
      raise NotImplementedError
  
  def get_date(self):
    """Get the month from an mvol identifier. 
   
    Returns:
      str: a date, e.g. 06
   
    """
  
    return self.identifier.split("-")[3][2:]
  
  def get_year_month_date(self):
    """Get the year-month-date from an identifier. 
   
    Returns:
      str: a date, e.g. 1930-01-06
   
    """
  
    return self.get_year() + '-' + self.get_month() + '-' + self.get_date()
  
