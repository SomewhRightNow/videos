import sys, json, urllib.request, urllib.parse, time, os
UA = {'User-Agent': 'cinecode-video-research/1.0'}
def get(u):
    for k in range(6):
        try: return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90).read()
        except Exception as e: print('retry', e, flush=True); time.sleep(6 + 8 * k)
for spec in sys.argv[1:]:
    key, name = spec.split('=', 1); out = f'assets/{key}.jpg'
    if os.path.exists(out): continue
    api = 'https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(dict(action='query', format='json', titles='File:' + name, prop='imageinfo', iiprop='url|size', iiurlwidth=1920))
    d = json.loads(get(api)); ii = list(d['query']['pages'].values())[0]['imageinfo'][0]
    u = ii.get('thumburl') if ii['width'] > 1920 else ii['url']
    b = get(u.split('?')[0])
    if b: open(out, 'wb').write(b); print('ok', key, len(b), flush=True)
    time.sleep(3)
