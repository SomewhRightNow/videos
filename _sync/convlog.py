# Appends the plain-text conversation (user messages + Claude replies, no tool output) to konusmalar/YYYY-MM-DD.md
# so every Claude account sharing this workspace can read what was discussed. Emails are redacted.
# usage: convlog.py [transcript.jsonl]   (Stop hook passes the hook JSON on stdin with transcript_path)
import sys, json, os, re, datetime
D = '/home/user/Filmler/konusmalar'; ST = os.path.expanduser('~/.cache/srn_convlog.json')
EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
SYS = re.compile(r'<(system-reminder|task-notification|local-command[\w-]*|command-[\w-]+)>.*?</\1>', re.S)
path = sys.argv[1] if len(sys.argv) > 1 else None
if not path:
    try: path = json.load(sys.stdin).get('transcript_path')
    except Exception: path = None
if not path or not os.path.exists(path): sys.exit(0)
state = {}
try: state = json.load(open(ST))
except Exception: pass
off = state.get(path, 0); size = os.path.getsize(path)
if off > size: off = 0
os.makedirs(D, exist_ok=True); out = {}
with open(path, 'rb') as f:
    f.seek(off)
    for raw in f:
        off += len(raw)
        try: d = json.loads(raw)
        except Exception: continue
        if d.get('type') not in ('user', 'assistant') or d.get('isMeta') or d.get('isSidechain'): continue
        m = d.get('message') or {}; c = m.get('content'); texts = []
        if isinstance(c, str): texts = [c]
        elif isinstance(c, list): texts = [b.get('text', '') for b in c if b.get('type') == 'text']
        txt = SYS.sub('', '\n'.join(texts)).strip()
        if not txt or txt.startswith('<') or 'SYSTEM NOTIFICATION' in txt[:200]: continue
        txt = EMAIL.sub('[email]', txt)
        ts = str(d.get('timestamp') or datetime.datetime.utcnow().isoformat())
        day, hm = ts[:10], ts[11:16]
        who = 'Kullanıcı' if d['type'] == 'user' else 'Claude'
        out.setdefault(day, []).append(f'**[{hm} UTC] {who}:** {txt}\n')
for day, rows in out.items():
    with open(f'{D}/{day}.md', 'a', encoding='utf-8') as g: g.write('\n'.join(rows) + '\n')
state[path] = off; os.makedirs(os.path.dirname(ST), exist_ok=True); json.dump(state, open(ST, 'w'))
