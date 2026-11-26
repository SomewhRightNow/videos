# Live goal watcher (ESPN, no key): prints one line per NEW goal across leagues for a date; poll every 60 s.
# Usage: python3 goalwatch.py 20261126 uefa.europa.conf uefa.europa
import sys, json, time, urllib.request
date, leagues = sys.argv[1], sys.argv[2:]; seen = set(); first = True
def get(u):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=20))
while True:
    live = 0
    for L in leagues:
        try: sb = get(f'https://site.api.espn.com/apis/site/v2/sports/soccer/{L}/scoreboard?dates={date}')
        except Exception: continue
        for e in sb.get('events', []):
            st = e['status']['type']['state']
            if st == 'pre': continue
            if st == 'in': live += 1
            if st == 'post' and e['id'] in {s.split('|')[0] for s in seen} and not first: pass
            try: sm = get(f'https://site.api.espn.com/apis/site/v2/sports/soccer/{L}/summary?event={e["id"]}')
            except Exception: continue
            c = e['competitions'][0]; teams = ' vs '.join(x['team']['displayName'] for x in c['competitors'])
            for k in sm.get('keyEvents', []) or []:
                tx = k.get('type', {}).get('text', '')
                if 'Goal' not in tx and 'Own Goal' not in tx and 'Penalty - Scored' not in tx: continue
                key = f"{e['id']}|{k.get('id')}"
                if key in seen: continue
                seen.add(key)
                if not first: print(f"GOAL {L} {e['id']} {teams} | {k.get('clock', {}).get('displayValue')} | {k.get('text')}", flush=True)
    if first: print(f'WATCHING {len(seen)} earlier goals indexed', flush=True); first = False
    time.sleep(60)
