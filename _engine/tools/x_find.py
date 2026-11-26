# Stand-footage finder for X (no login): feed it tweet URLs/IDs found with WebSearch (allowed_domains x.com/twitter.com,
# queries like '<player> goal tribün', '<player> from the stands', '<team> desde la grada', '<player> fan view').
# For each tweet with video: author, text, duration, best resolution, aspect; downloads it and writes a 6-frame strip so
# Claude can judge "stand footage?" (phone, crowd heads in foreground, shaky, no broadcast scorebug) at a glance.
# Usage: python3 x_find.py OUTDIR url_or_id [url_or_id ...]
import sys, os, re, json, subprocess, urllib.request
out = sys.argv[1]; os.makedirs(out, exist_ok=True)
rows = []
for arg in sys.argv[2:]:
    m = re.search(r'(\d{15,})', arg)
    if not m: continue
    tid = m.group(1)
    try:
        d = json.load(urllib.request.urlopen(f'https://cdn.syndication.twimg.com/tweet-result?id={tid}&token=a', timeout=20))
    except Exception as e:
        print('ERR', tid, e); continue
    vids = [x for x in d.get('mediaDetails', []) if x.get('type') == 'video']
    if not vids and d.get('quoted_tweet'): vids = [x for x in d['quoted_tweet'].get('mediaDetails', []) if x.get('type') == 'video']
    if not vids: continue
    v = vids[0]; vs = sorted([x for x in v['video_info']['variants'] if x.get('bitrate')], key=lambda x: x['bitrate'])
    if not vs: continue
    url = vs[-1]['url']; wh = re.search(r'/(\d+)x(\d+)/', url); w, h = (int(wh.group(1)), int(wh.group(2))) if wh else (0, 0)
    dur = v['video_info'].get('duration_millis', 0) / 1000
    fn = f'{out}/{tid}.mp4'
    if not os.path.exists(fn) and subprocess.run(['curl', '-s', '-f', '-o', fn, url]).returncode: print('DL-ERR', tid); continue
    subprocess.run(['ffmpeg', '-v', 'error', '-i', fn, '-vf', f'fps=6/{max(dur, 1):.2f},scale=160:-1,tile=6x1', '-frames:v', '1', f'{out}/{tid}.jpg', '-y'])
    rows.append((tid, d['user']['screen_name'], round(dur, 1), f'{w}x{h}', 'V' if h > w else 'H', d.get('text', '').replace('\n', ' ')[:90]))
for r in rows: print(*r, sep=' | ')
json.dump(rows, open(f'{out}/index.json', 'w'))
