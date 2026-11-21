import sys, urllib.request, urllib.parse, time, os
UA = {'User-Agent': 'cinecode-video-research/1.0'}
for spec in sys.argv[1:]:
    key, name = spec.split('=', 1); out = f'assets/{key}.jpg'
    if os.path.exists(out): continue
    u = 'https://commons.wikimedia.org/wiki/Special:FilePath/' + urllib.parse.quote(name) + '?width=1920'
    for k in range(6):
        try: b = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90).read(); break
        except Exception as e: print('retry', key, e); time.sleep(5 + 6 * k); b = None
    if b: open(out, 'wb').write(b); print('ok', key, len(b))
    time.sleep(8)
