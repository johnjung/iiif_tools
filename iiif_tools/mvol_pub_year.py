import argparse
import csv
import getpass
import json
import os
import owncloud
import re
import requests
import sys
import urllib

from io import StringIO


def get_identifier_from_path(path):
    pieces = path.split('/')

    if path[-1:] == '/':
        pieces.pop()

    while pieces[0] != 'mvol':
        pieces.pop(0)
    return '-'.join(pieces)


def get_ocr_url(identifier):
    return 'https://digcollretriever.lib.uchicago.edu/projects/' + identifier + '/ocr?jpg_width=1000&jpg_height=800&min_year=1900&max_year=1941'


def get_image_url(identifier_and_object_number):
    """ e.g. mvol-0004-1931-0106_0001
        https://iiif-server.lib.uchicago.edu/0/0/0/1/1931.tif/full/1000,800/0/default.jpg
    """
    pieces = identifier_and_object_number.split('-')
    last_chunk = pieces.pop()
    pieces = pieces + last_chunk.split('_')
    return 'https://iiif-server.lib.uchicago.edu/' + '/'.join(pieces[0:4]) + '/TIFF/' + identifier_and_object_number + '.tif/full/1000,800/0/default.jpg'


def get_image_info_url(identifier_and_object_number):
    pieces = re.split('[-_]', identifier_and_object_number)
    url_encoded_part = urllib.parse.quote(
        '/'.join(pieces) + '/TIFF/' + identifier_and_object_number + '.tif')
    return 'https://iiif-server.lib.uchicago.edu/' + url_encoded_part + '/info.json'

# IIIF_Files/mvol/0004/1931/
# IIIF_Files/mvol/0004/1931/mvol-0004-1931-0106.struct.txt


def get_struct_txt_path(path):
    return path + '/' + get_identifier_from_path(path) + '.struct.txt'


def get_page_numbers(oc, struct_txt_path):
    file_str = oc.get_file_contents(struct_txt_path).decode('utf-8')

    page_numbers = []
    f = StringIO(file_str)
    r = csv.reader(f, delimiter='\t')
    for row in r:
        if row[0] == 'object':
            continue
        page_numbers.append(row[1])
    return page_numbers


if __name__ == '__main__':
    """ Produce an input file for a year's worth of mvol data.
        This checks to be sure that files are available via specific URLs, and it produces an input file for the OCR building script. 
    """

    pubs = []

    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="WebDAV username.")
    parser.add_argument("directory", help="e.g. IIIF_Files/mvol/0004/1931")
    args = parser.parse_args()

    try:
        oc = owncloud.Client(os.environ['WEBDAV_CLIENT'])
    except KeyError:
        sys.stderr.write("WEBDAV_CLIENT environmental variable not set.\n")
        sys.exit()

    password = getpass.getpass('WebDAV password: ')
    oc.login(args.username, password)

    for date_folder in oc.list(args.directory):

        if not date_folder.file_type == 'dir':
            continue

        if not re.match('^.*[/]\d{4}[/]$', date_folder.path):
            continue

        identifier = get_identifier_from_path(date_folder.path)

        ocr_url = get_ocr_url(identifier)

        r = requests.head(ocr_url)
        ocr_url_status = r.status_code
        try:
            assert ocr_url_status == 200
        except AssertionError:
            print(ocr_url)
            raise

        pub = {
            'identifier': identifier,
            'ocr': {
                'url': ocr_url,
                'status': ocr_url_status
            },
            'pages': []
        }

        page_numbers = get_page_numbers(
            oc, get_struct_txt_path(date_folder.path))

        n = 0
        for image_file in oc.list(date_folder.path + '/TIFF'):
            identifier_and_object_number = image_file.path.split(
                '/').pop().split('.')[0]
            image_url = get_image_url(identifier_and_object_number)

            r = requests.head(image_url)
            image_url_status = r.status_code
            try:
                assert image_url_status == 200
            except AssertionError:
                print(image_url)
                raise

            image_info_url = get_image_info_url(identifier_and_object_number)

            r = requests.head(image_url)
            image_info_url_status = r.status_code
            try:
                assert image_info_url_status == 200
            except AssertionError:
                print(image_info_url)
                raise

            pub['pages'].append({
                'image': {
                    'url': image_url,
                    'status': image_url_status
                },
                'info': {
                    'url': image_info_url,
                    'status': image_info_url_status
                },
                'page_number': page_numbers[n]
            })
            n = n + 1

        pubs.append(pub)

print(json.dumps(pubs, indent=4, sort_keys=True))
