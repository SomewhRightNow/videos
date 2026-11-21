# Commons search -> contact sheet of thumbnails with index numbers. usage: thumbs.py out.jpg limit "query"...
import sys, json, subprocess, io, urllib.parse
from PIL import Image, ImageDraw, ImageFont
out, lim, qs = sys.argv[1], int(sys.argv[2]), sys.argv[3:]
import time
UA = 'cinematic-film/1.0 (+https://github.com/Moh4696/open-3d-skills)'
def get(u):
    for k in range(8):
        r = subprocess.run(['curl', '-s', '-A', UA, '-w', '\n%{http_code}', u], capture_output=True).stdout
        body, code = r.rsplit(b'\n', 1)
        if code == b'200': return body
        time.sleep(5 * (k + 1))
    return b''
def api(params):
    return json.loads(get('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(params)) or b'{}')
items = []
for q in qs:
    if q.startswith('Category:'):
        p = dict(action='query', format='json', generator='categorymembers', gcmtitle=q, gcmtype='file', gcmlimit=lim, prop='imageinfo', iiprop='url|size', iiurlwidth=300)
    else:
        p = dict(action='query', format='json', generator='search', gsrsearch=q, gsrnamespace=6, gsrlimit=lim, prop='imageinfo', iiprop='url|size', iiurlwidth=300)
    r = api(p)
    for pg in (r.get('query', {}).get('pages', {}) or {}).values():
        ii = pg.get('imageinfo', [{}])[0]
        if 'thumburl' in ii: items.append((pg['title'], ii['thumburl'], ii.get('width'), ii.get('height')))
tiles = []
f = ImageFont.load_default()
for i, (t, u, w, h) in enumerate(items):
    b = get(u); time.sleep(0.5)
    try: im = Image.open(io.BytesIO(b)).convert('RGB')
    except Exception: continue
    im.thumbnail((300, 300)); tile = Image.new('RGB', (300, 320), (20, 20, 20)); tile.paste(im, ((300 - im.width) // 2, 0))
    ImageDraw.Draw(tile).text((4, 302), f'{i} {w}x{h}', fill=(255, 255, 0), font=f); tiles.append(tile)
    print(i, w, h, t)
c = 6; r = (len(tiles) + c - 1) // c
s = Image.new('RGB', (300 * c, 320 * max(r, 1)))
for i, tl in enumerate(tiles): s.paste(tl, ((i % c) * 300, (i // c) * 320))
s.save(out, quality=85)
