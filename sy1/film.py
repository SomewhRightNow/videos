# 'Goals you rarely see' compilation (X @sykn1977 2125875349468651659, 576x720 LOW RES, 60.3 s) FULL, countdown #12 -> #1 in source order,
# plate + rank badge (RANK LADDER-lite: no names, source gives none for most), subscribe pill, signature.
# Music: Kevin MacLeod 'Volatile Reaction' (CC BY 4.0) from 37 s instead of the source audio.
import subprocess
from PIL import Image, ImageDraw, ImageFont
W, H = 1440, 2560; VW, VH = 1440, 1800; VY = 600
F = '/home/user/Filmler/fonts/'; fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s); fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); RED = (215, 25, 35); PLATE = (12, 13, 18); GREY = (175, 178, 190); BG = (9, 10, 14); INK = (8, 8, 12)
CUTS = [0, 7.0, 12.5, 15.95, 20.83, 26.0, 30.0, 36.3, 42.93, 49.9, 54.37, 60.3]
G = list(zip(CUTS[:-1], CUTS[1:]))  # G0..G10 in source order
NAMES = {1: 'PLÉA', 2: 'RODRIGO', 7: 'VARDY'}
ORDER = [8, 10, 3, 5, 6, 9, 2, 4, 0, 7, 1]  # our countdown #11 -> #1 (most spectacular last)
SEG = [G[i] for i in ORDER]; N = len(SEG)
def ov(k):
    rank = N - k; im = Image.new('RGBA', (W, H)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, VY], fill=BG); d.rectangle([0, VY + VH, W, H], fill=BG)
    px0, py0, px1, py1 = 24, 140, 1416, 540
    d.rounded_rectangle([px0, py0, px1, py1], 34, fill=PLATE); d.rectangle([px0 + 40, py1 - 6, px1 - 40, py1], fill=YEL)
    f = fB(150); a, b = 'GOALS YOU ', 'RARELY SEE'
    x = px0 + 40; d.text((x, py0 + 170), a, font=f, fill=WHITE, anchor='ls'); d.text((x + d.textlength(a, font=f), py0 + 170), b, font=f, fill=YEL, anchor='ls')
    bs = 150; bx0, by0 = px0 + 40, py0 + 200
    d.rounded_rectangle([bx0, by0, bx0 + bs, by0 + bs], 20, fill=(YEL if rank == 1 else RED))
    d.text((bx0 + bs / 2, by0 + bs / 2 + 4), f'#{rank}', font=fB(100), fill=(INK if rank == 1 else WHITE), anchor='mm')
    nm = NAMES.get(ORDER[k])
    if nm: d.text((bx0 + bs + 34, by0 + bs / 2 + 6), nm, font=fB(130), fill=WHITE, anchor='lm')
    else: d.text((bx0 + bs + 34, by0 + bs / 2 + 4), 'THE BEST ONE IS LAST' if rank > 1 else 'SAVED THE BEST FOR LAST', font=fB(84), fill=GREY, anchor='lm')
    sg = '@somewhrightnow'; fs = fO(26); sw = d.textlength(sg, font=fs); tx1 = px1 - 40; tx0 = tx1 - sw - 70; ty0 = py1 - 4
    d.rounded_rectangle([tx0, ty0 - 20, tx1, ty0 + 46], 20, fill=PLATE); d.rectangle([tx0, ty0 - 6, tx1, ty0], fill=YEL)
    d.rounded_rectangle([tx0 + 16, ty0 + 10, tx0 + 46, ty0 + 32], 7, fill=RED); d.polygon([(tx0 + 27, ty0 + 15), (tx0 + 27, ty0 + 27), (tx0 + 37, ty0 + 21)], fill=WHITE)
    d.text((tx0 + 56, ty0 + 6), sg, font=fs, fill=(225, 226, 232))
    w2, h2 = 900, 130; sx = (W - w2) / 2; sy = 2410
    d.rounded_rectangle([sx, sy, sx + w2, sy + h2], 65, fill=RED, outline=WHITE, width=4)
    f1 = fB(66); f3 = fB(40); t1, t2 = 'SUBSCRIBE', 'MORE TOP LISTS DAILY'; t1w = d.textlength(t1, font=f1); bx = sx + (w2 - t1w - 70) / 2; by = sy + 16
    d.ellipse([bx, by + 6, bx + 42, by + 48], fill=WHITE); d.rectangle([bx + 3, by + 28, bx + 39, by + 48], fill=WHITE); d.rectangle([bx - 4, by + 44, bx + 46, by + 51], fill=WHITE)
    d.text((bx + 70, sy + 4), t1, font=f1, fill=WHITE); d.text((sx + (w2 - d.textlength(t2, font=f3)) / 2, sy + 80), t2, font=f3, fill=YEL)
    im.save(f'logs/ov{k}.png')
for k in range(N): ov(k)
ins = sum([['-ss', str(a), '-t', f'{b-a:.3f}', '-i', 'src/src.mp4'] for a, b in SEG], []) + sum([['-i', f'logs/ov{k}.png'] for k in range(N)], []) + ['-ss', '37', '-i', '/home/user/Filmler/_music/Volatile Reaction.mp3']
fc = [f'[{k}:v]fps=30,setpts=PTS-STARTPTS,scale={VW}:{VH}:flags=lanczos,pad={W}:{H}:0:{VY}[p{k}];[p{k}][{N+k}:v]overlay=0:0,fade=t=in:d=0.12:color=white[v{k}]' for k in range(N)]
fc.append(''.join(f'[v{k}]' for k in range(N)) + f'concat=n={N}:v=1:a=0,format=yuv420p[o];[{2*N}:a]atrim=0:60.3,afade=t=in:d=0.1,afade=t=out:st=59.3:d=1,loudnorm=I=-14:TP=-2:LRA=11[a]')
subprocess.run(['ffmpeg', '-y', '-v', 'error', *ins, '-filter_complex', ';'.join(fc), '-map', '[o]', '-map', '[a]', '-ar', '48000', '-shortest',
                '-c:v', 'libx264', '-preset', 'slow', '-crf', '16', '-maxrate', '45M', '-bufsize', '90M', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', 'out/Goals You Rarely See.mp4'], check=True)
print('done')
