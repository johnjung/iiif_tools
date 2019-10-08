# -*- coding: utf-8 -*-
import json
import re
import requests
import sys
import urllib.parse
import uuid
import xml.etree.ElementTree as ElementTree

from io import BytesIO
from pyiiif.pres_api.twodotone.records import Annotation, Canvas, ImageResource, Manifest, MetadataField, Sequence
from metadata_converters.classes import MarcToDc

class MapsIIIFManifest:
    def __init__(self, marc_str):
        self.dc = MarcToDc(marc_str)

    def identifier(self):
        c = re.sub('^.*\/', '', self.dc.identifier[0])
        return 'https://iiif-manifest.lib.uchicago.edu/maps/{}/{}.json'.format(c, c)

    def get_image_resource_url(self, path):
        """Return the URL for something served up via the imageserver. 
     
        :param path - a string, path to this thing under IIIF_Files. e.g., /maps/...
        must start with a slash. 
        """
        return 'https://iiif-server.lib.uchicago.edu/{}/full/full/0/default.jpg'.format(urllib.parse.quote(path, safe=''))

    def __str__(self):
        manifest = Manifest(self.identifier())
        manifest.type = "sc:Manifest"
        manifest.label = self.dc.title[0]
        manifest.description = self.dc.description[0]
    
        metadata = []
        metadata.append(MetadataField('Identifier', self.identifier()))
        for l in ('Coverage', 'Creator', 'Description', 'Extent', 'Format',
                  'Medium', 'Relation', 'Subject', 'Title', 'Type'):
            metadata.extend([MetadataField(l, v) for v in getattr(self.dc, l.lower())])
        manifest.set_metadata(metadata)
    
        sequence_id = 'https://www.lib.uchicago.edu/{}'.format(str(uuid.uuid4()))
        sequence = Sequence(sequence_id)
    
        canvas_id = 'https://www.lib.uchicago.edu/{}'.format(str(uuid.uuid4()))
        # should be the http(s) URI where JSON representation is published. 
        canvas = Canvas(canvas_id)
        # does this need a label? 

        annotation_id = 'https://www.lib.uchicago.edu/{}'.format(str(uuid.uuid4()))
        annotation = Annotation(annotation_id, canvas_id)
        #img_url = self.get_image_resource_url('/maps/G4104-C6E625-1926-T5/tifs/G4104-C6E625-1926-T5.TIF')
        img = ImageResource(
            'https',
            'iiif-server.lib.uchicago.edu',
            '',
            urllib.parse.quote('maps/G4104-C6-2B7-1923-U5/tifs/G4104-C6-2B7-1923-U5.tif', safe=''),
            'image/tiff'
        )
    
        annotation.resource = img
        canvas.images = [annotation]
        sequence.canvases = [canvas]
        manifest.sequences = [sequence]
    
        return str(manifest)
