# -*- coding: utf-8 -*-
import json
import os
import requests
import sqlite3
import urllib.parse
import uuid

from io import BytesIO
from metadata_converters.classes import SocSciMapsMarcXmlToDc

from PIL import Image
Image.MAX_IMAGE_PIXELS = 1000000000

def get_ark_from_original_identifier(identifier):
    conn = sqlite3.connect('/data/s4/jej/ark_data.db')
    c = conn.cursor()
    c.execute("SELECT ark FROM arks WHERE original_identifier = '%s'" % identifier)
    return c.fetchone()[0]

def get_original_identifier_from_ark(ark):
    conn = sqlite3.connect('/data/s4/jej/ark_data.db')
    c = conn.cursor()
    c.execute("SELECT original_identifier FROM arks WHERE ark = '%s'" % ark)
    return c.fetchone()[0]

def get_digital_objects_from_ark(ark):
    '''Returns a list of page objects, 
        e.g. ['00000001', '00000002', '00000003']'''
    noid = ark.split('/')[-1]
    inventory_path = '/data/digital_collections/ark_data/{}/inventory.json'.format(
        os.sep.join([noid[i:i+2] for i in range(0, len(noid), 2)])
    )
    with open(inventory_path) as f:
        data = json.load(f)

    objects = []
    for file_hash in data['versions'][data['head']]['state'].values():
        for f in file_hash:
            if f.endswith('/file.tif'):
                objects.append(f.split('/')[0])

    return sorted(objects)

class IIIFManifest:
    def __init__(self, identifier, ark, title, summary, required_statement):
        self.identifier = identifier
        self.ark = ark
        self.title = title
        self.summary = summary
        self.required_statement = required_statement
        self.image_sizes = []

        self.logo_url = 'https://www.lib.uchicago.edu/static/base/images/color-logo.png'
        with BytesIO(
            requests.get(self.logo_url).content
        ) as f:
            img = Image.open(f)
        self.logo_size = img.size
        self.logo_mime_type = 'image/png'

    def _get_manifest_url(self):
       return 'https://iiif-manifest.lib.uchicago.edu/{}/{}/{}.json'.format(
           self.identifier.split('-')[0],
           self.identifier.split('-')[1],
           self.identifier
       )

    def _get_provider(self):
        return [
            {
                'id': 'https://www.lib.uchicago.edu/about/thelibrary/',
                'type': 'Agent',
                'label': { 'en': [ 'University of Chicago Library' ] },
                'homepage': [
                    {
                        'id': 'https://www.lib.uchicago.edu/',
                        'type': 'Text',
                        'label': { 'en': [ 'University of Chicago Library Homepage' ] },
                        'format': 'text/html'
                     }
                ],
                'logo': [
                     {
                         'id': self.logo_url,
                         'type': 'Image',
                         'format': self.logo_mime_type,
                         'height': self.logo_size[1],
                         'width': self.logo_size[0]
                     }
                 ]
             }
         ]

    def _get_thumbnail(self, n, width):
        return [
            {
                'id': '{}/full/{},/0/default.jpg'.format(
                    self._get_imageserver_url(n),
                    width
                ),
                'service': [
                    {
                        '@id': self._get_imageserver_url(n),
                        '@type': 'ImageService2',
                        'profile': 'http://iiif.io/api/image/2/level2.json'
                    }
                ],
                'type': 'Image'
            }
        ]

    def _get_canvases(self):
        canvases = []
        for n in range(len(self.image_sizes)):
            canvas_id = 'https://{}'.format(str(uuid.uuid4()))
            canvases.append({
                'height': self._get_height(n),
                'id': canvas_id,
                'items': [ self._get_annotation_page(n, canvas_id) ],
                'label': { 'en': [ 'Image {:03d}'.format(n+1) ] },
                'thumbnail': self._get_thumbnail(n, 200),
                'type': 'Canvas',
                'width': self._get_width(n)
            })
        return canvases

    def _get_annotation_page(self, n, canvas_id):
        annotation_id = 'https://{}'.format(str(uuid.uuid4()))
        return {
            'id': annotation_id,
            'type': 'AnnotationPage',
            'items': [
                {
                    'id': annotation_id,
                    'type': 'Annotation',
                    'motivation': 'Painting',
                    'target': canvas_id,
                    'body': {
                        'format': 'image/jpeg',
                        'height': self._get_height(0),
                        'id': 'https://{}'.format(str(uuid.uuid4())),
                        'service': [
                            {
                                '@id': self._get_imageserver_url(n),
                                '@type': 'ImageService2',
                                'profile': 'http://iiif.io/api/image/2/level2.json'
                            }
                        ],
                        'type': 'Image',
                        'width': self._get_width(0)
                    }
                }
            ]
        }

    def data(self):
        if len(self.image_sizes) > 1:
            behavior = 'paged'
        else:
            behavior = 'non-paged'
        manifest = {
            '@context': [
                'http://iiif.io/api/presentation/3/context.json',
                'http://iiif.io/api/image/2/context.json'
            ],
            'behavior': [ behavior ],
            'id': self._get_manifest_url(),
            'items': self._get_canvases(),
            'type': 'Manifest',
            'metadata': self._get_metadata(),
            'provider': self._get_provider(),
            'label': { 'en': [ self.title ] },
            'requiredStatement': {
                'label': { 'en': [ 'Attribution' ] },
                'value': { 'en': [ self.required_statement ] }
            },
            'rights': 'http://creativecommons.org/licenses/by-nc/4.0/',
            'summary': {
                'en': [
                    self.summary
                ]
            },
            'thumbnail': self._get_thumbnail(0, 500)
        }
        if len(self.image_sizes) > 1:
            manifest['viewingDirection'] = 'left-to-right'
        return manifest

    def _get_width(self, n):
        return self.image_sizes[n][0]
            
    def _get_height(self, n):
        return self.image_sizes[n][1]

    def _get_imageserver_url(self, n):
        if len(self.image_sizes) == 1:
            return 'https://iiif-server.lib.uchicago.edu/{}'.format(
                urllib.parse.quote(self.ark, safe='')
            )
        else:
            return 'https://iiif-server.lib.uchicago.edu/{}'.format(
                urllib.parse.quote(
                    '{}/{:08}'.format(self.ark, n+1),
                    safe=''
                )
            )

    def _get_imageserver_url_thumb(self, max_size):
        thumbnail_size = [round(1.0 * max_size / max(self.image_sizes[0] * d))
                          for d in self.image_sizes[0]]

        return '{}/full/{},{}/0/default.jpg'.format( 
            self._get_imageserver_url(0),
            thumbnail_size[0],
            thumbnail_size[1]
        )
