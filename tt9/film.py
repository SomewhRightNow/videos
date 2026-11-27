# TOP 6 'Embarrassing Mistakes' (TikTok @magicaleight_8 ZSsB4aAGT; Karius UCL final DROPPED: UEFA strike risk)
# was tt8, 720x1280, 51 s) re-ordered ('karıştırarak editle'),
# RANK LADDER: plate covers source title, opaque ladder covers source list, subscribe pill covers MAGICAL EIGHT mark.
# Music: Kevin MacLeod 'Movement Proposition' (CC BY 4.0) from 42 s instead of the source's song.
import subprocess
from PIL import Image, ImageDraw, ImageFont
W, H = 1440, 2560
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); RED = (215, 25, 35); PLATE = (12, 13, 18); GREY = (175, 178, 190); INK = (8, 8, 12)
# source segments
S = {'szob': (0.0, 7.1), 'marcal': (7.1, 13.6), 'ronaldo': (13.6, 23.2), 'gavran': (23.2, 31.0), 'maitland': (31.0, 38.7), 'zirkzee': (38.7, 43.9)}
ORDER = [(6, 'MARÇAL', 'marcal'), (5, 'GAVRAN', 'gavran'), (4, 'ZIRKZEE', 'zirkzee'), (3, 'MAITLAND', 'maitland'),
         (2, 'SZOBOSZLAI', 'szob'), (1, 'RONALDO', 'ronaldo')]
MUS, OFF = '/home/user/Filmler/_music/Raving Energy.mp3', 120
def overlay(k):
    rank, name, _ = ORDER[k]
    im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    px0, py0, px1, py1 = 24, 150, 1416, 600
    d.rounded_rectangle([px0 + 6, py0 + 10, px1 + 6, py1 + 10], 34, fill=(0, 0, 0, 110)); d.rounded_rectangle([px0, py0, px1, py1], 34, fill=PLATE + (255,))
    d.rectangle([px0 + 40, py1 - 6, px1 - 40, py1], fill=YEL)
    f = fB(120); a, b, c = 'MOST ', 'EMBARRASSING MISTAKES', ' EVER'
    while d.textlength(a + b + c, font=f) > px1 - px0 - 80: f = fB(f.size - 4)
    x = (W - d.textlength(a + b + c, font=f)) / 2; y = py0 + 150
    for s, col in ((a, WHITE), (b, YEL), (c, WHITE)): d.text((x, y), s, font=f, fill=col, anchor='ls'); x += d.textlength(s, font=f)
    bx0, by0 = px0 + 40, py0 + 200; bs = 200
    d.rounded_rectangle([bx0, by0, bx0 + bs, by0 + bs], 24, fill=(YEL if rank == 1 else RED))
    d.text((bx0 + bs / 2, by0 + bs / 2 + 6), f'#{rank}', font=fB(130), fill=(INK if rank == 1 else WHITE), anchor='mm')
    fn = fB(190)
    while d.textlength(name, font=fn) > px1 - bx0 - bs - 80: fn = fB(fn.size - 6)
    d.text((bx0 + bs + 40, by0 + bs / 2 + 8), name, font=fn, fill=WHITE, anchor='lm')
    sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = px1 - 40; tx0 = tx1 - sw - 70; ty0 = py1 - 4
    d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE); d.rectangle([tx0, ty0 - 6, tx1, ty0], fill=YEL)
    d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
    d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
    # ladder covering the source list (src x30-270, y650-1010 -> out x60-540, y1300-2020)
    lx0, ly0, rh = 30, 1290, 124
    for i, r in enumerate(range(1, 7)):
        y = ly0 + i * rh; shown = r >= rank
        nm = next(n for rr, n, _ in ORDER if rr == r)
        fr = fB(80); txt = nm if shown else ''
        w = 120 + (d.textlength(txt, font=fr) + 40 if shown else 0)
        col = YEL if r == rank else PLATE
        d.rectangle([lx0, y, lx0 + max(w + 10, 620), y + rh], fill=PLATE)
        d.rounded_rectangle([lx0 + 8, y + 8, lx0 + 104, y + rh - 8], 14, fill=(RED if r != 1 else YEL))
        d.text((lx0 + 56, y + rh / 2 + 3), str(r), font=fB(64), fill=(WHITE if r != 1 else INK), anchor='mm')
        if shown:
            if r == rank: d.rounded_rectangle([lx0 + 112, y + 8, lx0 + w, y + rh - 8], 14, fill=YEL)
            d.text((lx0 + 130, y + rh / 2 + 3), txt, font=fr, fill=(INK if r == rank else WHITE), anchor='lm')
    # cover strip so source rows never leak (fixed width = widest source row)
    w2, h2 = 900, 160; sx = (W - w2) / 2; sy = 2200
    d.rounded_rectangle([sx, sy, sx + w2, sy + h2], 80, fill=RED, outline=WHITE, width=4)
    f1 = fB(76); f3 = fB(48); t1, t2 = 'SUBSCRIBE', 'MORE TOP LISTS DAILY'; t1w = d.textlength(t1, font=f1); bx = sx + (w2 - t1w - 80) / 2; by = sy + 24
    d.ellipse([bx, by + 6, bx + 48, by + 54], fill=WHITE); d.rectangle([bx + 3, by + 31, bx + 45, by + 54], fill=WHITE); d.rectangle([bx - 5, by + 50, bx + 53, by + 58], fill=WHITE); d.ellipse([bx + 17, by + 56, bx + 31, by + 68], fill=WHITE)
    d.text((bx + 80, sy + 6), t1, font=f1, fill=WHITE); d.text((sx + (w2 - d.textlength(t2, font=f3)) / 2, sy + 96), t2, font=f3, fill=YEL)
    im.save(f'logs/ov{k}.png')
inputs = []; fc = []; total = 0; n = len(ORDER)
for k, (r, _nm, key) in enumerate(ORDER):
    a, b = S[key]; overlay(k); inputs += ['-ss', str(a), '-t', f'{b-a:.3f}', '-i', 'src/src.mp4']; total += b - a
    fc.append(f'[{k}:v]setpts=PTS-STARTPTS,scale=1440:2560:flags=lanczos[v{k}];[v{k}][{n+k}:v]overlay=0:0,fade=t=in:st=0:d=0.12:color=white[o{k}]')
fc.append(''.join(f'[o{k}]' for k in range(len(ORDER))) + f'concat=n={len(ORDER)}:v=1:a=0,format=yuv420p[fv]')
fc.append(f'[{2*n}:a]atrim=0:{total:.2f},afade=t=in:d=0.1,afade=t=out:st={total-1:.2f}:d=1,loudnorm=I=-14:TP=-2:LRA=11[fa]')
subprocess.run(['ffmpeg', '-y', '-v', 'error', *inputs, *sum([['-i', f'logs/ov{k}.png'] for k in range(n)], []), '-ss', str(OFF), '-i', MUS, '-filter_complex', ';'.join(fc), '-map', '[fv]', '-map', '[fa]', '-ar', '48000',
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', 'out/Embarrassing Mistakes.mp4'], check=True)
print('done', round(total, 2))
