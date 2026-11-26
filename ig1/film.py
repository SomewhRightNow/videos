# ARDA GULER ROCKETS countdown #5 -> #1 (IG reel @aardagulerfans DfzrCeitlZ6, 1080x1920 letterboxed, 60.9 s), all goals used,
# reversed so the Bayern free kick is #1; creator's skull-emoji freeze frames cut out; source caption covered by our chip.
# Music: Kevin MacLeod 'Raving Energy' (CC BY 4.0) from 71 s instead of the source audio.
import subprocess
from PIL import Image, ImageDraw, ImageFont
W, H = 1440, 2560; VY = 540; CROP = (0, 240, 1080, 1440)
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); RED = (215, 25, 35); PLATE = (12, 13, 18); GREY = (175, 178, 190); BG = (9, 10, 14); INK = (8, 8, 12)
EMO = [(11.2, 12.8), (16.9, 18.7), (28.3, 30.0), (34.0, 35.7), (39.7, 41.4), (45.5, 46.9), (51.3, 53.1), (55.95, 58.5)]
GOALS = [(0, 18.7), (18.7, 30.0), (30.0, 38.5), (38.5, 49.45), (49.45, 60.9)]
def parts(a, b):
    out, t = [], a
    for e0, e1 in EMO:
        if e1 <= t or e0 >= b: continue
        if e0 > t: out.append((t, e0))
        t = max(t, e1)
    if t < b: out.append((t, b))
    return out
ORDER = [4, 3, 2, 1, 0]  # #5..#1
def ov(k, cap=False):
    rank = 5 - k; im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, VY], fill=BG); d.rectangle([0, VY + 1920, W, H], fill=BG)
    px0, py0, px1, py1 = 24, 110, 1416, 500
    d.rounded_rectangle([px0, py0, px1, py1], 34, fill=PLATE); d.rectangle([px0 + 40, py1 - 6, px1 - 40, py1], fill=YEL)
    f = fB(150); a, b = 'ARDA GÜLER ', 'ROCKETS'
    d.text((px0 + 40, py0 + 165), a, font=f, fill=WHITE, anchor='ls'); d.text((px0 + 40 + d.textlength(a, font=f), py0 + 165), b, font=f, fill=YEL, anchor='ls')
    bs = 150; bx0, by0 = px0 + 40, py0 + 195
    d.rounded_rectangle([bx0, by0, bx0 + bs, by0 + bs], 20, fill=(YEL if rank == 1 else RED))
    d.text((bx0 + bs / 2, by0 + bs / 2 + 4), f'#{rank}', font=fB(100), fill=(INK if rank == 1 else WHITE), anchor='mm')
    d.text((bx0 + bs + 34, by0 + bs / 2 + 4), 'THE BEST ONE IS LAST' if rank > 1 else 'SAVED THE BEST FOR LAST', font=fB(84), fill=GREY if rank > 1 else YEL, anchor='lm')
    sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = px1 - 40; tx0 = tx1 - sw - 70; ty0 = py1 - 4
    d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE); d.rectangle([tx0, ty0 - 6, tx1, ty0], fill=YEL)
    d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
    d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
    if cap:  # covers the creator's caption (src ~y960 -> out ~1500)
        d.rounded_rectangle([370, 1440, 1070, 1560], 26, fill=PLATE); d.text((720, 1502), 'WATCH THE LEFT FOOT', font=fB(70), fill=WHITE, anchor='mm')
    w2, h2 = 900, 130; sx = (W - w2) / 2; sy = 2410
    d.rounded_rectangle([sx, sy, sx + w2, sy + h2], 65, fill=RED, outline=WHITE, width=4)
    f1 = fB(66); f3 = fB(40); t1, t2 = 'SUBSCRIBE', 'MORE TOP LISTS DAILY'; t1w = d.textlength(t1, font=f1); bx = sx + (w2 - t1w - 70) / 2; by = sy + 16
    d.ellipse([bx, by + 6, bx + 42, by + 48], fill=WHITE); d.rectangle([bx + 3, by + 28, bx + 39, by + 48], fill=WHITE); d.rectangle([bx - 4, by + 44, bx + 46, by + 51], fill=WHITE)
    d.text((bx + 70, sy + 4), t1, font=f1, fill=WHITE); d.text((sx + (w2 - d.textlength(t2, font=f3)) / 2, sy + 80), t2, font=f3, fill=YEL)
    name = f'logs/ov{k}{"c" if cap else ""}.png'; im.save(name); return name
SEGS = []
for k, g in enumerate(ORDER):
    for a, b in parts(*GOALS[g]):
        if g == 0 and a < 5 < b: SEGS += [(a, 5.0, ov(k, cap=True)), (5.0, b, ov(k))]
        else: SEGS.append((a, b, ov(k)))
SEGS = [(a, min(b, 5.0), o) if False else (a, b, o) for a, b, o in SEGS]
ins, fc = [], []
for i, (a, b, o) in enumerate(SEGS): ins += ['-ss', str(a), '-t', f'{b-a:.3f}', '-i', 'src/src.mp4', '-i', o]
for i, (a, b, o) in enumerate(SEGS):
    fc.append(f'[{2*i}:v]fps=30,setpts=PTS-STARTPTS,crop={CROP[2]}:{CROP[3]}:{CROP[0]}:{CROP[1]},scale=1440:1920:flags=lanczos,pad={W}:{H}:0:{VY}[p{i}];[p{i}][{2*i+1}:v]overlay=0:0[v{i}]')
n = len(SEGS); total = sum(b - a for a, b, _ in SEGS)
fc.append(''.join(f'[v{i}]' for i in range(n)) + f'concat=n={n}:v=1:a=0,format=yuv420p[o];[{2*n}:a]atrim=0:{total:.2f},afade=t=in:d=0.1,afade=t=out:st={total-1:.2f}:d=1,loudnorm=I=-14:TP=-2:LRA=11[a]')
subprocess.run(['ffmpeg', '-y', '-v', 'error', *ins, '-ss', '71', '-i', '/home/user/Filmler/_music/Raving Energy.mp3', '-filter_complex', ';'.join(fc), '-map', '[o]', '-map', '[a]', '-ar', '48000',
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', 'out/Arda Guler Rockets.mp4'], check=True)
print('done', round(total, 2), len(SEGS))
