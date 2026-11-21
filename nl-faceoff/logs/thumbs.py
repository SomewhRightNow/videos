import sys, os, urllib.request, urllib.parse, time, io
from PIL import Image, ImageDraw
UA = {'User-Agent': 'cinecode-video-research/1.0'}
out = sys.argv[1]; names = sys.argv[2:]; ims = []
for n in names:
    u = 'https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote(n) + '?width=400'
    for k in range(5):
        try: b = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40).read(); break
        except Exception as e: time.sleep(3 + 4 * k); b = None
    if not b: print('fail', n); continue
    im = Image.open(io.BytesIO(b)).convert('RGB'); im.thumbnail((300, 300)); ims.append((n, im)); time.sleep(1)
sh = Image.new('RGB', (310 * len(ims), 320), (20, 20, 20))
for i, (n, im) in enumerate(ims):
    sh.paste(im, (i * 310, 18)); ImageDraw.Draw(sh).text((i * 310 + 3, 2), str(i), fill='yellow')
sh.save(out); print('ok', len(ims))
