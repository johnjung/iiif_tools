# -*- coding: utf-8 -*-
import getpass
import json
import os
import re
import requests
import sys
import urllib.parse
import uuid
import xml.etree.ElementTree as ElementTree

from io import BytesIO
from metadata_converters.classes import SocSciMapsMarcXmlToDc
from pyiiif.pres_api.twodotone.records import Annotation, Canvas, ImageResource, Manifest, MetadataField, Sequence

from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000

class SocSciMapsIIIFManifest:
    def __init__(self, marc_str):
        self.dc = SocSciMapsMarcXmlToDc(marc_str)

    def identifier(self):
        c = re.sub('^.*\/', '', self.dc.identifier[0])
        return 'https://iiif-manifest.lib.uchicago.edu/maps/chisoc/{}/{}.json'.format(c, c)

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
        canvas.label = '[1]'

        annotation_id = 'https://www.lib.uchicago.edu/{}'.format(str(uuid.uuid4()))
        annotation = Annotation(annotation_id, canvas_id)

        identifier = self.dc.identifier[0].replace('http://pi.lib.uchicago.edu/1001/', '')

        img_path = '{}/tifs/{}.tif'.format(
            identifier,
            identifier.split('/').pop()
        )

        img = ImageResource(
            'https',
            'iiif-server.lib.uchicago.edu',
            '',
            urllib.parse.quote(img_path, safe=''),
            'image/tiff'
        )

        i = Image.open(BytesIO(
            requests.get(self.get_image_resource_url(img_path)).content
        ))

        img.set_height(i.size[0])
        img.set_width(i.size[1])
    
        annotation.resource = img
        canvas.images = [annotation]
        sequence.canvases = [canvas]
        manifest.sequences = [sequence]
    
        return str(manifest)
