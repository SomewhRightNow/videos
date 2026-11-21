# Openverse search -> json + contact sheet (free licences only: cc0, by, by-sa, pdm)
import json, subprocess, sys, io, urllib.parse, time
from PIL import Image, ImageDraw
out = sys.argv[1]; res = {}
for q in sys.argv[2:]:
    u = 'https://api.openverse.org/v1/images/?' + urllib.parse.urlencode(dict(q=q, license='by,by-sa,cc0,pdm', page_size=20))
    r = subprocess.run(['curl', '-s', '-A', 'Mozilla/5.0 (film research)', u], capture_output=True).stdout
    try: d = json.loads(r)
    except Exception: print(q, 'ERR', r[:120]); continue
    res[q] = [dict(title=x.get('title'), url=x.get('url'), thumb=x.get('thumbnail'), w=x.get('width'), h=x.get('height'), lic=f"{x.get('license')} {x.get('license_version')}",
                   creator=x.get('creator'), src=x.get('foreign_landing_url'), prov=x.get('provider')) for x in d.get('results', [])]
    print(q, len(res[q]), flush=True); time.sleep(1)
json.dump(res, open(out + '.json', 'w'), indent=1)
tiles = []
for q, L in res.items():
    for x in L:
        if not x['thumb'] or not x['w'] or x['w'] < 1600: continue
        b = subprocess.run(['curl', '-sL', '-A', 'Mozilla/5.0', x['thumb']], capture_output=True).stdout
        try: im = Image.open(io.BytesIO(b)).convert('RGB')
        except Exception: continue
        im.thumbnail((300, 300)); t = Image.new('RGB', (300, 330), (20, 20, 20)); t.paste(im, ((300 - im.width) // 2, 0))
        i = len(tiles); x['idx'] = i
        ImageDraw.Draw(t).text((3, 302), f"{i} {x['w']}x{x['h']} {x['lic']}", fill=(255, 255, 0)); ImageDraw.Draw(t).text((3, 316), (x['title'] or '')[:46], fill=(200, 200, 200)); tiles.append(t)
json.dump(res, open(out + '.json', 'w'), indent=1)
c = 8; r = (len(tiles) + c - 1) // c; s = Image.new('RGB', (2400, 330 * max(1, r)))
for i, t in enumerate(tiles): s.paste(t, ((i % c) * 300, (i // c) * 330))
s.save(out + '.jpg', quality=82); print('tiles', len(tiles))
