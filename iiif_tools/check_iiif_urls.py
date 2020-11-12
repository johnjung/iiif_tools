import json, requests, sys

# e.g.  https://iiif-collection-dev.lib.uchicago.edu/social-scientists-map-chicago.json

urls = {}

def add_url_status(u):
    if not u in urls:
        r = requests.get(u)
        urls[u] = r.status_code

        if r.status_code == 200:
            data = json.loads(r.text)
            for item in data['items']:
                if 'lib.uchicago.edu' in item['id']:
                    add_url_status(item['id'])

if __name__=='__main__':
    add_url_status(sys.argv[1])

    for k, v in urls.items():
        print('{} {}'.format(v, k))
