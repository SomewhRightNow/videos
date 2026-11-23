# COUNTDOWN: 8 trivela (outside-of-the-boot) moments. Source: X @CuriosidadesEU 2124576036868465028 (1080x1920, 51 s): match footage band (y 458-1532) 0-49 s USED IN FULL;
# their title band, info band and end card cropped out. Own ranking + own template. Context = source labels (well-known matches).
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); YEL = (253, 215, 0); INK = (10, 10, 14); RED = (215, 25, 35)
NSRC = len(os.listdir('src/fa'))
RAW = {'burns': (0.2, 10.4), 'qir': (10.4, 18.9), 'cancelo': (18.9, 23.4), 'cuco': (23.4, 28.4), 'cisse': (28.4, 31.6), 'modric': (31.6, 38.7),
       'qbjk': (38.7, 45.0), 'mbappe': (45.0, 48.95)}
PLAY = [('cuco', 'CUCO MARTINA', 'SOUTHAMPTON vs ARSENAL  ·  2015/16'), ('burns', 'WES BURNS', 'IPSWICH vs COVENTRY  ·  2023/24'),
        ('mbappe', 'MBAPPÉ ➜ DANILO', 'PSG vs SAINT-ÉTIENNE  ·  2021/22'), ('cancelo', 'CANCELO ➜ HAALAND', 'MAN CITY vs DORTMUND  ·  2022/23'),
        ('cisse', 'PAPISS CISSÉ', 'CHELSEA vs NEWCASTLE  ·  2011/12'), ('qbjk', 'RICARDO QUARESMA', 'BEŞIKTAŞ vs FENERBAHÇE  ·  2017/18'),
        ('modric', 'MODRIĆ ➜ RODRYGO', 'REAL MADRID vs CHELSEA  ·  2021/22'), ('qir', 'RICARDO QUARESMA', 'PORTUGAL vs IRAN  ·  WORLD CUP 2018')]
SEG = []; t0 = 0
for k, n, c in PLAY: a, b = RAW[k]; SEG.append((t0, t0 + b - a, a, n, c)); t0 += b - a
CLIP = t0; TOTAL = CLIP + 3.0; VY = 420
_c = {}
def src(s):
    k = min(NSRC, max(1, int(round(s * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB'); b = (985, 0, 1080, 110)
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(12)), b[:2]); _c[k] = im
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def base(im):
    bg = im.resize((20, 20)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.22))
    bg.paste(im, (0, VY)); return bg
def frame(t):
    if t < CLIP:
        i = max(j for j, s in enumerate(SEG) if s[0] <= t); a, b, s0, name, ctx = SEG[i]; lt = t - a; rk = 8 - i
        img = base(src(s0 + lt)); d = ImageDraw.Draw(img)
        f = fB(44); s = 'TOP 8'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=RED); d.text((76, 115), s, font=f, fill=WHITE)
        if t < 3: tc(d, 195, 'THE ART OF', fB(90), WHITE, 7); tc(d, 280, 'THE TRIVELA', fB(130), YEL, 9)
        else: tc(d, 215, 'OUTSIDE OF THE BOOT', fB(104), WHITE, 8)
        # progress dots
        for j in (range(8) if t >= 3 else []):
            x = 360 + j * 46; d.ellipse([x, 360, x + 26, 386], fill=YEL if j <= i else (60, 60, 72))
        u = ease(lt / 0.35); ly = VY + 1074 + 50; x0 = 60 - int((1 - u) * 500)
        rs = f'#{rk}'; fr = fB(170); rw = d.textlength(rs, font=fr); d.text((x0, ly - 40), rs, font=fr, fill=YEL, stroke_width=6, stroke_fill=(0, 0, 0)); x0 += int(rw) + 30
        d.rectangle([x0, ly, x0 + 10, ly + 160], fill=WHITE)
        nf = fB(78)
        while d.textlength(name, font=nf) > W - x0 - 60: nf = fB(nf.size - 4)
        d.text((x0 + 34, ly - 6), name.replace('➜', '→'), font=nf, fill=WHITE); d.text((x0 + 36, ly + 100), ctx, font=fO(28), fill=(210, 210, 220))
        if 0 <= lt < 0.1 and i > 0: img = Image.blend(img, Image.new('RGB', (W, H), WHITE), 0.3 * (1 - lt / 0.1))
    else:
        lt = t - CLIP; img = base(src(RAW['qir'][1] - 0.05)).filter(ImageFilter.GaussianBlur(25)); img = Image.eval(img, lambda v: int(v * 0.3)); d = ImageDraw.Draw(img)
        a = ease(lt / 0.4); tc(d, 240 + int((1 - a) * 30), 'WHICH TRIVELA', fB(120), WHITE, 8); tc(d, 365 + int((1 - a) * 30), 'IS YOUR #1?', fB(150), YEL, 9)
        for j in range(8):
            k, n, c = PLAY[7 - j]; b = ease((lt - 0.07 * j) / 0.3); y = 640 + j * 112
            d.rounded_rectangle([120, y, W - 120, y + 96], 18, fill=(16, 16, 22), outline=(70, 70, 80), width=2)
            d.text((155, y + 8), f'{j + 1}', font=fB(76), fill=YEL); d.text((240 + int((1 - b) * 40), y + 12), n.replace('➜', '→'), font=fB(66), fill=WHITE)
    if t > TOTAL - 0.4: img = Image.eval(img, lambda x, q=(TOTAL - t) / 0.4: int(x * max(0, q)))
    return img
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(x).resize((360, 640)) for x in (1.5, 12.0, 25.0, 45.0, TOTAL - 1)]
        s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); print(TOTAL); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'out/video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
