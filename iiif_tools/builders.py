import json
import re
import requests
import sys
import xml.etree.ElementTree as ElementTree

from io import BytesIO
from pyiiif.pres_api.twodotone.records import Annotation, Canvas, ImageResource, Manifest, MetadataField, Sequence
from marc_tools.converters import MarcToDc


class MapIIIFManifest:
  def __init__(self, dc_str):
    self.dc = MarcToDc(dc_str)

  def identifier(self, dc):
    c = re.sub('^.*\/', '', dc.identifier)
    return 'https://iiif-manifest.lib.uchicago.edu/maps/{}/{}.json'.format(c, c)

  def __str__(self):
    manifest = Manifest(identifier(dc))
    manifest.type = "sc:Manifest"
    manifest.label = dc.title
    manifest.description = dc.description
    return str(manifest)

    '''
      metadata_list = []
      for label in ('Identifier', 'Title', 'Creator', 'Date', 'Description',
  		  'Rights', 'Language', 'Format', 'Type', 'Subject', 
                    'Print Call Number', 'Coverage', 'Relation'):
        e = getattr(marc_tool, 'get_{}'.format(label.replace(' ', '_').lower()))
        metadata_list.extend([MetadataField(label, v) for v in e()])
      manifest.set_metadata(metadata_list)
    '''
  
  
    ''' 
    sequence = Sequence("http://example.org/sequence/1")
  
    # and now to make a simple canvas
    canvas = Canvas("http://example.org/canvas/1")
    canvas.label = "A Canvas"
  
    # now to make an annotation for that canvas
    annotate = Annotation("http://example.org/annotation/1")
  
    # now to make an image resource to put in the canvas
    img = ImageResource("http://example.org/an_image.jpg")
  
    #  last but not least you have to put all the pieces together...
    annotate.resource = img
    canvas.images = [annotate]
    sequence.canvases = [canvas]
    manifest.sequences = [sequence]
  
    # and voila! you have a IIIF manifest record!
    print(json.dumps(manifest.to_dict()))
  
    break
    '''
