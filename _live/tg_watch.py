# TELEGRAM İZLEYİCİ: herkese açık kanalların web önizlemesi (t.me/s/<kanal>, giriş yok) -> yeni VİDEO gönderilerini indirir,
# 6 karelik şerit çıkarır ve tek satır yazar. Claude şeride bakıp tribün mü / resmi kulüp mü / yayın mı karar verir.
# Kullanım: python3 tg_watch.py OUTDIR kanal1 kanal2 ...   (Monitor ile; 60 sn'de bir). --once: tek tur, eski gönderileri de listeler.
import sys, os, re, time, html, subprocess, urllib.request
args = [a for a in sys.argv[1:] if not a.startswith('--')]; once = '--once' in sys.argv
out, chans = args[0], args[1:]; os.makedirs(out, exist_ok=True)
seen = set(); first = not once
def fetch(c):
    req = urllib.request.Request(f'https://t.me/s/{c}', headers={'User-Agent': 'Mozilla/5.0'})
    return urllib.request.urlopen(req, timeout=20).read().decode('utf-8', 'ignore')
while True:
    for c in chans:
        try: page = fetch(c)
        except Exception: continue
        for blk in page.split('tgme_widget_message_wrap')[1:]:
            pid = re.search(r'data-post="([^"]+)"', blk); vid = re.search(r'<video[^>]*src="([^"]+)"', blk)
            if not pid or not vid: continue
            pid = pid.group(1)
            if pid in seen: continue
            seen.add(pid)
            if first: continue
            t = re.search(r'datetime="([^"]+)"', blk); txt = re.search(r'tgme_widget_message_text[^>]*>(.*?)</div>', blk, re.S)
            txt = html.unescape(re.sub('<[^>]+>', ' ', txt.group(1))).strip().replace('\n', ' ')[:120] if txt else ''
            fn = f"{out}/{pid.replace('/', '_')}.mp4"
            if subprocess.run(['curl', '-s', '-f', '-L', '-o', fn, html.unescape(vid.group(1))]).returncode: continue
            pr = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:format=duration', '-of', 'csv=p=0', fn], capture_output=True, text=True).stdout.split()
            dur = float(pr[-1]) if pr else 0
            subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', fn, '-vf', f'fps=6/{max(dur, 1):.2f},scale=160:-1,tile=6x1', '-frames:v', '1', fn[:-4] + '.jpg'])
            print(f"TG | {pid} | {t.group(1)[:16] if t else ''} | {pr[0] if pr else ''} | {dur:.0f}s | {txt} | {fn}", flush=True)
    if once: break
    if first: print(f'TG HAZIR: {len(seen)} eski gönderi atlandı, {len(chans)} kanal', flush=True); first = False
    time.sleep(60)
