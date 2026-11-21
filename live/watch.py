# Live match watcher (ESPN public feed). usage: watch.py <league> <event_id>  -> prints one line per important event, exits at full time.
import json, sys, time, urllib.request, os
LG, EV = sys.argv[1], sys.argv[2]; SEEN = f'/home/user/Filmler/_live/seen_{EV}.json'
seen = set(json.load(open(SEEN))) if os.path.exists(SEEN) else set()
SKIP = ('substitution', 'yellow card', 'kickoff', 'start 2nd half', 'start delay', 'end delay')
def score(d):
    cs = d['header']['competitions'][0]['competitors']; return ' '.join(f"{c['team']['abbreviation']} {c.get('score','?')}" for c in cs)
while True:
    try:
        d = json.load(urllib.request.urlopen(f'https://site.api.espn.com/apis/site/v2/sports/soccer/{LG}/summary?event={EV}', timeout=20))
        for k in d.get('keyEvents', []):
            kid = str(k.get('id')); typ = (k.get('type', {}).get('text') or '').strip()
            if kid in seen: continue
            seen.add(kid); json.dump(sorted(seen), open(SEEN, 'w'))
            inj = 'injur' in (k.get('text') or '').lower() and typ.lower().startswith('substitution')
            if not inj and (typ.lower() in SKIP or typ.lower().startswith('yellow')): continue
            if inj: typ = 'INJURY SUB'
            print(f"[{k.get('clock',{}).get('displayValue','')}] {typ}: {k.get('text','')[:220]} | {score(d)}", flush=True)
        st = d['header']['competitions'][0]['status']['type']
        if st.get('completed'): print(f'FULL TIME | {score(d)}', flush=True); break
    except Exception as e:
        pass
    time.sleep(30)
