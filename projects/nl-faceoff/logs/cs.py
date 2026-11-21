import sys, json, urllib.request, urllib.parse, time
UA = {'User-Agent': 'cinecode-video-research/1.0 (contact: none)'}
def q(params):
    u = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(params)
    for k in range(5):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))
        except Exception as e: time.sleep(2 + 3 * k)
for term in sys.argv[1:]:
    r = q(dict(action='query', format='json', generator='search', gsrsearch=f'filetype:bitmap {term}', gsrnamespace=6, gsrlimit=12,
               prop='imageinfo', iiprop='url|size|extmetadata', iiurlwidth=1600))
    print('==', term)
    for p in sorted(r.get('query', {}).get('pages', {}).values(), key=lambda p: p.get('index', 0)):
        ii = p['imageinfo'][0]; md = ii.get('extmetadata', {})
        print(f"{ii['width']}x{ii['height']} | {md.get('LicenseShortName', {}).get('value', '?')} | {p['title'][5:][:90]}")
    time.sleep(1)
