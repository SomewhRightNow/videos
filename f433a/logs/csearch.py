# Polite Commons search (shared IP is rate-limited): one request at a time, honours 429 with long waits.
import json, subprocess, time, urllib.parse, sys
UA = 'cinematic-film/1.0 (+https://github.com/Moh4696/open-3d-skills)'
def get(u):
    for k in range(30):
        r = subprocess.run(['curl', '-s', '-A', UA, '-w', '\n%{http_code}', u], capture_output=True).stdout
        body, code = r.rsplit(b'\n', 1)
        if code == b'200': return json.loads(body)
        time.sleep(60)
    return {}
Q = sys.argv[2:]; out = {}
for q in Q:
    p = dict(action='query', format='json', generator='search', gsrsearch=q, gsrnamespace=6, gsrlimit=50, prop='imageinfo',
             iiprop='url|size|extmetadata', iiurlwidth=400, iiextmetadatafilter='LicenseShortName|Artist')
    r = get('https://commons.wikimedia.org/w/api.php?' + urllib.parse.urlencode(p))
    res = []
    for pg in (r.get('query', {}).get('pages', {}) or {}).values():
        ii = pg.get('imageinfo', [{}])[0]; em = ii.get('extmetadata', {})
        res.append(dict(title=pg['title'], w=ii.get('width'), h=ii.get('height'), thumb=ii.get('thumburl'), url=ii.get('url'),
                        lic=em.get('LicenseShortName', {}).get('value'), artist=em.get('Artist', {}).get('value')))
    out[q] = res; print(q, len(res), flush=True)
    json.dump(out, open(sys.argv[1], 'w'), indent=1); time.sleep(8)
