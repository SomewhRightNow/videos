# TOP 5 FREE KICKS: broadcast clips played in full (no zoom), blurred-fill vertical frame, rank lower-third, VO captions, end card.
import sys, json, subprocess, numpy as np, soundfile as sf
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
W, H, FPS = 1080, 1920, 30
FD = '/mnt/skills/examples/canvas-design/canvas-fonts/'; F_T = FD + 'BigShoulders-Bold.ttf'; F_MB = FD + 'GeistMono-Bold.ttf'
RED = (214, 28, 36); WH = (255, 255, 255); GOLD = (244, 196, 64); DIM = (205, 210, 220)
SEG = [('xbwd05y', 0.0, 7.48, 5, 'MARCOS LÓPEZ', 'RANDERS v FC COPENHAGEN · DANISH SUPERLIGA'),
       ('xbwcolu', 0.0, 10.04, 4, 'RAPHAEL VEIGA', 'PALMEIRAS v SPORTING CRISTAL · LIBERTADORES'),
       ('xbwdeum', 0.0, 8.20, 3, 'FEDE VALVERDE', 'ATLÉTICO v REAL MADRID · SPANISH SUPER CUP'),
       ('xbwdn5q', 1.0, 13.0, 2, 'JULIÁN ÁLVAREZ', 'BARCELONA 0–2 ATLÉTICO · CHAMPIONS LEAGUE'),
       ('xbwfgoi', 2.0, 10.6, 1, 'CRISTIANO RONALDO', 'AL NASSR 4–1 DAMAC · SAUDI TITLE DECIDER')]
END = 4.4
LINES = [l.strip() for l in open('logs/lines.txt') if l.strip()]
VO = [sf.info(f'audio/vo/v{i}.wav').duration for i in range(len(LINES))]
starts, t = [], 0.0
for s in SEG: starts.append(t); t += s[2] - s[1]
T_END = t; TOTAL = T_END + END
VO_AT = [st + 0.15 for st in starts] + [T_END + 0.25]
def chunks(i):  # 2-4 word caption chunks timed by character share
    words = LINES[i].split(); out, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) >= 3 or w[-1] in '.,:?!': out.append(' '.join(cur)); cur = []
    if cur: out.append(' '.join(cur))
    tot = sum(len(c) for c in out); t0 = VO_AT[i]; res = []
    for c in out:
        d = VO[i] * len(c) / tot; res.append((t0, t0 + d, c)); t0 += d
    return res
CAPS = [c for i in range(len(LINES)) for c in chunks(i)]
json.dump(dict(vo_at=VO_AT, total=TOTAL), open('logs/timing.json', 'w'))
def font(p, s): return ImageFont.truetype(p, s)
FT = {k: font(*v) for k, v in dict(rank=(F_T, 230), name=(F_T, 92), sub=(F_MB, 27), chip=(F_MB, 30), cap=(F_T, 84), end1=(F_T, 120), end2=(F_T, 64), brand=(F_MB, 24)).items()}
def src_reader(sid, a, b):
    vf = (f'fps={FPS},split[a][b];[a]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},boxblur=30:2,eq=brightness=-0.42[bg];'
          f'[b]scale={W}:-2:flags=lanczos[fg];[bg][fg]overlay=0:(H-h)/2')
    p = subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error', '-ss', f'{a:.3f}', '-t', f'{b - a:.3f}', '-i', f'src/{sid}.mp4', '-vf', vf,
                          '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    while True:
        buf = p.stdout.read(W * H * 3)
        if len(buf) < W * H * 3: break
        yield Image.frombuffer('RGB', (W, H), buf, 'raw', 'RGB', 0, 1)
def caption(d, t):
    for a, b, c in CAPS:
        if a <= t < b:
            d.text((W / 2, 1460), c.upper(), font=FT['cap'], fill=WH, anchor='mm', stroke_width=8, stroke_fill=(0, 0, 0)); return
def chrome(d):
    d.rounded_rectangle((W / 2 - 190, 120, W / 2 + 190, 176), 10, fill=RED)
    d.text((W / 2, 148), 'TOP 5 · FREE KICKS', font=FT['chip'], fill=WH, anchor='mm')
    d.text((W / 2, 1850), 'SOMEWHERE RIGHT NOW', font=FT['brand'], fill=(200, 204, 212), anchor='mm')
def lower(d, k, lt):
    _, _, _, rank, name, sub = SEG[k]; a = min(1, lt / 0.25); x = 60 - (1 - a) * 80
    d.text((x, 520), f'#{rank}', font=FT['rank'], fill=GOLD if rank == 1 else WH, anchor='ls', stroke_width=6, stroke_fill=(0, 0, 0))
    nx = x + (300 if rank != 1 else 270)
    d.text((nx, 430), name, font=FT['name'] if len(name) < 16 else font(F_T, 78), fill=WH, anchor='ls', stroke_width=5, stroke_fill=(0, 0, 0))
    d.text((nx + 4, 488), sub, font=FT['sub'] if len(sub) < 42 else font(F_MB, 23), fill=DIM, anchor='ls', stroke_width=3, stroke_fill=(0, 0, 0))
p = subprocess.Popen(['ffmpeg', '-nostdin', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                      '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
n = 0; last = None
for k, (sid, a, b, *_r) in enumerate(SEG):
    for j, im in enumerate(src_reader(sid, a, b)):
        t = n / FPS; clean = im; im = im.copy()
        if j < 3: im = Image.blend(im, Image.new('RGB', (W, H), WH), 0.5 * (1 - j / 3))  # flash cut
        d = ImageDraw.Draw(im); chrome(d); lower(d, k, j / FPS); caption(d, t)
        p.stdin.write(im.tobytes()); n += 1; last = im if False else None
        base = clean
    lastsrc = base
# end card: dimmed final frame of #1 (no new footage)
fz = ImageEnhance.Brightness(lastsrc).enhance(0.35)
for j in range(int(END * FPS)):
    t = n / FPS; im = fz.copy(); d = ImageDraw.Draw(im); chrome(d)
    a = min(1, j / 8)
    d.text((W / 2, 760), 'WHICH ONE IS', font=FT['end1'], fill=WH, anchor='mm', stroke_width=6, stroke_fill=(0, 0, 0))
    d.text((W / 2, 890), 'YOUR #1?', font=FT['end1'], fill=GOLD, anchor='mm', stroke_width=6, stroke_fill=(0, 0, 0))
    if j > 20:
        d.rounded_rectangle((150, 1040, W - 150, 1150), 55, fill=RED); d.text((W / 2, 1095), 'COMMENT 5, 4, 3, 2 OR 1', font=FT['end2'], fill=WH, anchor='mm')
    if j > 45: d.text((W / 2, 1240), 'FOLLOW FOR MORE TOP 5s', font=FT['end2'], fill=WH, anchor='mm', stroke_width=4, stroke_fill=(0, 0, 0))
    caption(d, t); p.stdin.write(im.tobytes()); n += 1
p.stdin.close(); p.wait(); print('frames', n, 'dur', n / FPS, 'expected', TOTAL)
