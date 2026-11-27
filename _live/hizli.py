# HIZLI TESLİM (canlı gol tribün klibi, Deniz Gül şablonu): link -> indir -> şablon -> kontrol -> up-<ad> dalı (raw URL).
# Kullanım: python3 hizli.py <x/tiktok linki> <ad> "ÜST SATIR (İSİM · DK')" "ALT SATIR (SKOR)" [--label "FROM THE STANDS"] [--push]
# Dikey kaynak tam ekran; yatay/kare kaynak koyu zeminde ortada. Orijinal ses, -14 LUFS (2 geçiş). Çıktı: /home/user/Filmler/live/<ad>/<ad>.mp4
import sys, os, re, json, subprocess, argparse
from PIL import Image, ImageDraw, ImageFont
ap = argparse.ArgumentParser(); ap.add_argument('url'); ap.add_argument('name'); ap.add_argument('top'); ap.add_argument('bottom')
ap.add_argument('--label', default='FROM THE STANDS'); ap.add_argument('--push', action='store_true'); ap.add_argument('--ss', default=None); ap.add_argument('--to', default=None)
A = ap.parse_args()
R = '/home/user/Filmler'; D = f'{R}/live/{A.name}'; os.makedirs(D, exist_ok=True); src = f'{D}/src.mp4'
if not os.path.exists(src):
    m = re.search(r'(?:x|twitter)\.com/.+/status/(\d+)', A.url)
    if m:
        subprocess.run(['python3', f'{R}/_engine/tools/x_find.py', D, m.group(1)], check=True); os.rename(f'{D}/{m.group(1)}.mp4', src)
    else:
        subprocess.run(['yt-dlp', '-q', '--no-warnings', '-f', 'mp4/best', '-o', src, A.url], check=True)
pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of', 'json', src], capture_output=True, text=True).stdout)['streams'][0]
w0, h0 = pr['width'], pr['height']; W, H = 1440, 2560; vertical = h0 / w0 > 1.5
vh = H if vertical else round(W * h0 / w0 / 2) * 2; VY = 0 if vertical else max(600, (H - vh) // 2 - 60)
F = f'{R}/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); RED = (215, 25, 35); PLATE = (12, 13, 18)
im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
d.rounded_rectangle([24, 150, W - 24, 520], 34, fill=PLATE + (235 if vertical else 255,))
d.text((W / 2, 205), A.label, font=fO(40), fill=(190, 192, 200), anchor='mm')
f = fB(160)
while d.textlength(A.top, font=f) > W - 120: f = fB(f.size - 4)
d.text((W / 2, 335), A.top, font=f, fill=WHITE, anchor='mm')
f2 = fB(96)
while d.textlength(A.bottom, font=f2) > W - 120: f2 = fB(f2.size - 4)
d.text((W / 2, 455), A.bottom, font=f2, fill=WHITE, anchor='mm')
sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = W - 64; tx0 = tx1 - sw - 70; ty0 = 540 if vertical else VY + vh + 40
d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE + (230,))
d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
pw, ph = 900, 160; sx = (W - pw) / 2; sy = 2370 if vertical else 2240
d.rounded_rectangle([sx, sy, sx + pw, sy + ph], 80, fill=RED, outline=WHITE, width=4)
f1 = fB(76); f3 = fB(48); t1, t2 = 'SUBSCRIBE', 'NEVER MISS A GOAL'; t1w = d.textlength(t1, font=f1); bx = sx + (pw - t1w - 80) / 2; by = sy + 24
d.ellipse([bx, by + 6, bx + 48, by + 54], fill=WHITE); d.rectangle([bx + 3, by + 31, bx + 45, by + 54], fill=WHITE); d.rectangle([bx - 5, by + 50, bx + 53, by + 58], fill=WHITE); d.ellipse([bx + 17, by + 56, bx + 31, by + 68], fill=WHITE)
d.text((bx + 80, sy + 6), t1, font=f1, fill=WHITE); d.text((sx + (pw - d.textlength(t2, font=f3)) / 2, sy + 96), t2, font=f3, fill=WHITE)
im.save(f'{D}/ov.png')
trim = (['-ss', A.ss] if A.ss else []) + (['-to', A.to] if A.to else [])
# loudness pass 1
lj = subprocess.run(['ffmpeg', '-hide_banner', *trim, '-i', src, '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-'], capture_output=True, text=True).stderr
mj = json.loads(lj[lj.rfind('{'):lj.rfind('}') + 1])
ln = f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={mj['input_i']}:measured_TP={mj['input_tp']}:measured_LRA={mj['input_lra']}:measured_thresh={mj['input_thresh']}:offset={mj['target_offset']}:linear=true"
vf = (f'[0:v]scale={W}:{H}:flags=lanczos[v];[v][1:v]overlay=0:0,format=yuv420p[o]' if vertical else
      f'color=c=0x0b0c10:s={W}x{H}:r=30[bg];[0:v]scale={W}:{vh}:flags=lanczos,unsharp=5:5:0.5[v];[bg][v]overlay=0:{VY}:shortest=1[b];[b][1:v]overlay=0:0,format=yuv420p[o]')
out = f'{D}/{A.name}.mp4'
subprocess.run(['ffmpeg', '-y', '-v', 'error', *trim, '-i', src, '-i', f'{D}/ov.png', '-filter_complex', vf, '-map', '[o]', '-map', '0:a', '-af', ln, '-ar', '48000',
                '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', out], check=True)
chk = subprocess.run(['python3', f'{R}/_refs/ffmpeg-skill/scripts/check.py', out, '--platform', 'youtube-shorts'], capture_output=True, text=True).stdout
print('\n'.join(l for l in chk.splitlines() if 'FAIL' in l or 'checks' in l or 'loudness' in l))
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', '3', '-i', out, '-frames:v', '1', '-vf', 'scale=540:-1', f'{D}/preview.jpg'])
if A.push:
    T = f'/tmp/up-{A.name}'; subprocess.run(['rm', '-rf', T]); os.makedirs(T)
    fn = f'{A.name}.mp4'; subprocess.run(['cp', out, f'{T}/{fn}'], check=True)
    remote = subprocess.run(['git', '-C', '/home/user/videos', 'remote', 'get-url', 'origin'], capture_output=True, text=True).stdout.strip()
    for c in (['git', 'init', '-q', '-b', f'up-{A.name}'], ['git', 'add', '.'], ['git', '-c', 'user.name=Somewhere Right Now', '-c', 'user.email=noreply@anthropic.com', 'commit', '-qm', f'Upload: {A.name}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01DiJM6j5npbMAK7HBQMwxKP'],
              ['git', 'remote', 'add', 'origin', remote]):
        subprocess.run(c, cwd=T, check=True)
    for _ in range(4):
        if subprocess.run(['git', 'push', '-q', '-f', 'origin', f'up-{A.name}'], cwd=T, capture_output=True).returncode == 0: break
    print(f'RAW https://raw.githubusercontent.com/SomewhRightNow/videos/up-{A.name}/{fn}')
print('OUT', out)
