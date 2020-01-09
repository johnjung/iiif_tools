#!/usr/bin/env python

"""Usage:
   cli_collection_browse <collection-url>

https://iiif-collection.lib.uchicago.edu/top.json
"""

import json, urllib.request, sys 
from docopt import docopt

# check to see if files exist at that location. 

def main():
    options = docopt(__doc__)

    sys.stdout.write('+ {}\n|\n'.format(options['<collection-url>']))
    
    u = urllib.request.urlopen(options['<collection-url>'])
    collection = json.loads(u.read().decode())
   
    m = 0 
    while m < len(collection['members']):
        if m < len(collection['members']) - 1:
            pipe_char = '|' 
        else:
            pipe_char = ' ' 

        try:
            urllib.request.urlopen(collection['members'][m]['@id'])
            error_message = ''
        except urllib.error.URLError:
            error_message = 'UNAVAILABLE '

        sys.stdout.write('|--- {}{}\n'.format(
            error_message,
            collection['members'][m]['label']
        ))  
        sys.stdout.write('{}    {}\n'.format(
            pipe_char, 
            collection['members'][m]['@id']
        ))  
        sys.stdout.write('{}    {}\n'.format(
            pipe_char, 
            collection['members'][m]['@type']
        ))  
        sys.stdout.write('{}    {}\n'.format(
            pipe_char, 
            collection['members'][m]['viewingHint']
        ))  
        sys.stdout.write('{}\n'.format(
            pipe_char
        ))  
        m += 1

if __name__=='__main__':
    main()
