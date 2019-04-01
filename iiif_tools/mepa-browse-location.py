import csv
import json
import re
from unidecode import unidecode

# return ascii chars, no ampersands, dashes instead of spaces. 
def safe(s):
    if isinstance(s, list):
        return '-'.join([safe(e) for e in s])
    else:
        return unidecode(s).replace('&', 'and').replace(' ', '-').lower()

# 1A = https://iiif-manifest.lib.uchicago.edu/mepa/001/001.json
def mepa_url(s):
    nums = re.findall(r'\d+', s)
    return 'https://iiif-manifest.lib.uchicago.edu/mepa/' + nums[0].zfill(3) + '/' + nums[0].zfill(3) + '.json'

def mepa_title(s):
    s = s.replace(', recto', '')
    s = s.replace(', Recto', '')
    s = s.replace(', verso', '')
    s = s.replace(', Verso', '')
    return s.strip()

locations = {}
member_data = {}

with open('MEPA Bridge Export.txt', 'r') as f:
    r = csv.reader(f, delimiter="\t")
    next(r)
    for row in r:
        location = row[12].split(';')[0].replace(' [creation]', '').split(', ')
        title = mepa_title(row[3])
        if location:
            location_filename = 'mepa-browse-location-' + safe(location) + '.json'
            url = mepa_url(row[12].split(';')[1].split(',')[4].split(' ')[6])
    
            if not location_filename in locations:
                locations[' - '.join(location)] = set()
            locations[' - '.join(location)].add(url)

            member_data[url] = {
                'label': title,
                '@id': url,
                '@type': 'sc:Collection',
                'viewingHint': 'multi-part'
            }

for location, members in locations.items():
    location_filename = 'mepa-browse-location-' + safe(location.split(' - ')) + '.json'
    collection = {
        "label": location,
        "@id": "https://iiif-collection.lib.uchicago.edu/mepa/" + location_filename,
        "@context": "https://iiif.io/api/presentation/2/context.json",
        "@type": "sc:Collection",
        "description": "The Middle East Photograph Archive consists of over 400 photographic prints dating primarily to the second half of the nineteenth century. At this time, the spread of the art of photography and the influx of Europeans into the lands of the Middle East led to the creation of a large number of photographs produced by professional photographers. During these decades, the versatility of photography was enhanced through the development of a variety of chemical techniques, enabling photographers to produce images in relatively large numbers, intended chiefly to satisfy the tourism trade burgeoning in the Middle East and the European thirst for images of the Orient. The archive is particularly strong in photographs of nineteenth-century Cairo. Europeans were attracted to Egypt by its Pharaonic monuments, but once there, visitors came to appreciate Cairo as the largest and best-preserved medieval metropolis in the world. The scores of Islamic monuments built between the ninth and fifteenth centuries in and around Cairo provided a huge number of subjects for photography.\nThese early photographs stand now as important documents of the history of photography. However, the significance of these artifacts is enriched by their utility as historical documents of the architectural and social history of the Middle East. Photographers chose as subjects the monuments of the Middle East\u2019s medieval and ancient past, as well as scenes of daily life. Since the nineteenth century, many of these monuments have been altered through architectural restoration, or their contexts have been radically transformed by the inevitable modernization witnessed in the twentieth century. In some cases, and particularly in those scenes depicting social life, the images are the only surviving records of the Middle East\u2019s history.\nThe collection was first scanned and made available on the Library\u2019s website in 1996 at what is today considered low resolution. The collection was re-digitized in 2014 in color and at a higher resolution in order to create preservation-quality master files, and to make the collection easier to navigate for both general and advanced users. Color is particularly important, allowing more accurate viewing of the varied tonality of the many albumen prints as well as the results of some of the more creative photographic experiments. The Middle East Photograph Archive re-digitization project was made possible in 2014 through the Library\u2019s Mary and Samuel Somit Preservation Internship.",
        "attribution": "University of Chicago Library",
        "viewingHint": "individuals",
        "members": []
    }
    for member in members:
        collection['members'].append(member_data[member])

    with open(location_filename, 'w') as f:
        f.write(json.dumps(collection, indent=4))
        f.close()

