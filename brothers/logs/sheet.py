import json, sys, subprocess, io, time
from PIL import Image, ImageDraw
d = json.load(open('cs.json')); q = sys.argv[1]; out = sys.argv[2]
items = [x for x in d[q] if x.get('thumb') and (x['lic'] or '').upper().startswith(('CC', 'PUBLIC', 'PD'))]
tiles = []
for i, x in enumerate(items[:36]):
    b = b''
    for k in range(6):
        r = subprocess.run(['curl', '-s', '-A', 'cinematic-film/1.0 (+https://github.com/Moh4696/open-3d-skills)', '-w', '\n%{http_code}', x['thumb'].replace('thumb.wikimedia.org', 'upload.wikimedia.org')], capture_output=True).stdout
        b, code = r.rsplit(b'\n', 1)
        if code == b'200': break
        time.sleep(4 * (k + 1))
    time.sleep(1.0)
    try: im = Image.open(io.BytesIO(b)).convert('RGB')
    except Exception: continue
    im.thumbnail((300, 300)); t = Image.new('RGB', (300, 320), (20, 20, 20)); t.paste(im, ((300 - im.width) // 2, 0))
    ImageDraw.Draw(t).text((4, 303), f"{i} {x['w']}x{x['h']} {x['lic']}", fill=(255, 255, 0)); tiles.append(t)
    print(i, x['w'], x['h'], x['lic'], x['title'][5:100])
c = 6; r = (len(tiles) + c - 1) // c; s = Image.new('RGB', (1800, 320 * max(1, r)))
for i, t in enumerate(tiles): s.paste(t, ((i % c) * 300, (i // c) * 300 + (i // c) * 20))
s.save(out, quality=85)
