# download 800px previews from upload.wikimedia.org (md5 path), politely; then contact sheet
import hashlib, urllib.parse, subprocess, time, sys, io, os
from PIL import Image, ImageDraw
UA = 'cinematic-film/1.0 (+https://github.com/Moh4696/open-3d-skills)'
names = [l.strip() for l in open(sys.argv[1]) if l.strip()]
os.makedirs('prev', exist_ok=True); tiles = []
for i, n in enumerate(names):
    fn = n.replace(' ', '_'); h = hashlib.md5(fn.encode()).hexdigest(); q = urllib.parse.quote(fn)
    ext = '.png' if fn.lower().endswith('.png') else ''
    u = f'https://upload.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/800px-{q}{ext}'
    out = f'prev/{i:02d}.jpg'
    if not os.path.exists(out):
        for k in range(8):
            r = subprocess.run(['curl', '-s', '-A', UA, '-w', '\n%{http_code}', u], capture_output=True).stdout
            b, code = r.rsplit(b'\n', 1)
            if code == b'200': Image.open(io.BytesIO(b)).convert('RGB').save(out, quality=88); break
            time.sleep(6 * (k + 1))
        time.sleep(2)
    print(i, os.path.exists(out), n, flush=True)
    if os.path.exists(out):
        im = Image.open(out); im.thumbnail((300, 300)); t = Image.new('RGB', (300, 320), (20, 20, 20)); t.paste(im, ((300 - im.width) // 2, 0))
        ImageDraw.Draw(t).text((4, 303), f'{i} {n[:44]}', fill=(255, 255, 0)); tiles.append(t)
c = 6; r = (len(tiles) + c - 1) // c; s = Image.new('RGB', (1800, 320 * max(1, r)))
for i, t in enumerate(tiles): s.paste(t, ((i % c) * 300, (i // c) * 320))
s.save(sys.argv[2], quality=85)
