# fetch ORIGINAL files (full res) from upload.wikimedia.org, sequential, long backoff on 429
import hashlib, urllib.parse, subprocess, time, sys, os
UA = 'cinematic-film/1.0 (+https://github.com/Moh4696/open-3d-skills)'
os.makedirs('../film/assets/photos', exist_ok=True)
for line in open(sys.argv[1]):
    line = line.strip()
    if not line: continue
    key, n = line.split('|', 1)
    fn = n.replace(' ', '_'); h = hashlib.md5(fn.encode()).hexdigest(); q = urllib.parse.quote(fn)
    ext = os.path.splitext(fn)[1].lower()
    out = f'../film/assets/photos/{key}{ext}'
    if os.path.exists(out) and os.path.getsize(out) > 50000: print(key, 'have', flush=True); continue
    pext = '.png' if ext == '.png' else ''
    done = False
    for w in (3840, 1920, 1280):
        u = f'https://thumb.wikimedia.org/wikipedia/commons/thumb/{h[0]}/{h[:2]}/{q}/{w}px-{q}{pext}'
        for k in range(6):
            code = subprocess.run(['curl', '-s', '-A', UA, '-o', out, '-w', '%{http_code}', u], capture_output=True, text=True).stdout
            if code == '200': print(key, 'ok', w, os.path.getsize(out), flush=True); done = True; break
            if code in ('400', '404'): break
            print(key, 'retry', code, flush=True); time.sleep(20)
        if done: break
    if not done: print(key, 'FAILED', flush=True)
    time.sleep(5)
print('DONE', flush=True)
