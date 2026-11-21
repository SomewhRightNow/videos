# Dailymotion clip finder: dm_find.py YYYY-MM-DD "query1" "query2" ... -> lists recent football clips (id, secs, uploader, best format, title)
import sys, json, urllib.request, urllib.parse, datetime
since = int(datetime.datetime.fromisoformat(sys.argv[1]).timestamp())
KEEP = ('highlight', 'goal', 'gol', ' vs ', ' v ', '-', 'resumen', 'golazo', 'all goals')
for q in sys.argv[2:]:
    u = 'https://api.dailymotion.com/videos?' + urllib.parse.urlencode(dict(search=q, created_after=since, limit=15,
        fields='id,title,duration,owner.screenname,available_formats,created_time'))
    try: d = json.load(urllib.request.urlopen(u, timeout=30))
    except Exception as e: print('ERR', q, e); continue
    print('==', q)
    for v in d.get('list', []):
        t = v['title'].lower()
        if not any(k in t for k in KEEP) or v['duration'] > 1200: continue
        f = (v.get('available_formats') or ['?'])[-1]
        print(f"  {v['id']} {v['duration']:>4}s {datetime.date.fromtimestamp(v['created_time'])} {v['owner.screenname'][:18]:18} {f:10} | {v['title'][:80]}")
