# EDIT: "Last-minute goals" — Provedel (Lazio 1-1 Atletico, 90+5, UCL 19.09.2023), Maguire (Liverpool 1-2 Man Utd, 84', 19.10.2025),
# Iniesta (Spain 1-0 Netherlands, 116', World Cup final 11.07.2010). Source: X @goaltimemedia 2124018443024212393 (fan compilation, 576x1024).
# Blurred: centre caption watermark + top-right corner. Real speed. Facts: ESPN/TSN, Sky/Premier League, UEFA/FIFA.
import os, subprocess, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont
os.chdir(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = 1080, 1920, 30
F = '/home/user/Filmler/fonts/'
fB = lambda s: ImageFont.truetype(F + 'BigShoulders-Bold.ttf', s)
fO = lambda s: ImageFont.truetype(F + 'Outfit-Bold.ttf', s)
WHITE = (255, 255, 255); GOLD = (240, 200, 90); RED = (210, 25, 30)
NSRC = len(os.listdir('src/fa')); SRC_END = NSRC / 30 - 0.05
NR = len(os.listdir('src/fr')); R_END = NR / 30 - 0.05
# Maguire part (20-42) removed after PL Content ID block; replaced by Ramos 92:48 (Dailymotion x1wpmhf, UCL final 2014)
SEGS = [('a', 0.0, 20.0), ('r', 0.0, R_END), ('a', 42.0, SRC_END)]
T0 = [0]
for _, a, b in SEGS: T0.append(T0[-1] + b - a)
TOTAL = T0[-1]
def s_of(t):
    for i, (k, a, b) in enumerate(SEGS):
        if t < T0[i + 1] or i == len(SEGS) - 1: return k, a + (t - T0[i])
PH = int(W * 652 / 576); PY = (H - PH) // 2 - 10
PARTS = [(0, 20, 'THE GOALKEEPER SCORED', "IVAN PROVEDEL  90+5'", 'LAZIO 1-1 ATLÉTICO  ·  CHAMPIONS LEAGUE  ·  2023'),
         (20, 20 + 11.75, 'THE 92:48 HEADER', "SERGIO RAMOS  92:48", 'REAL MADRID 1-1 ATLÉTICO  ·  UCL FINAL  ·  2014'),
         (20 + 11.75, 999, 'THE WORLD CUP WINNER', "ANDRÉS INIESTA  116'", 'SPAIN 1-0 NETHERLANDS  ·  WORLD CUP FINAL  ·  2010')]
_c = {}
def src_r(t):
    k = min(NR, max(1, int(round(t * 30)) + 1)); key = ('r', k)
    if key not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fr/f_{k:04d}.jpg').convert('RGB'); b = (im.width - 110, 0, im.width, 80)
        im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(10)), b[:2])
        _c[key] = im.resize((W, int(W * im.height / im.width)), Image.LANCZOS).filter(ImageFilter.UnsharpMask(1.6, 60, 2))
    return _c[key]
def src(t):
    k = min(NSRC, max(1, int(round(t * 30)) + 1))
    if k not in _c:
        if len(_c) > 40: _c.clear()
        im = Image.open(f'src/fa/f_{k:04d}.jpg').convert('RGB').crop((0, 186, 576, 838))
        for b in ((150, 308, 425, 342), (576 - 50, 0, 576, 60)): im.paste(im.crop(b).filter(ImageFilter.GaussianBlur(8)), b[:2])
        _c[k] = im.resize((W, PH), Image.LANCZOS).filter(ImageFilter.UnsharpMask(2, 70, 2))
    return _c[k]
def ease(u): u = max(0, min(1, u)); return 1 - (1 - u) ** 3
def tc(d, y, s, f, fill, stroke=7):
    w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=stroke, stroke_fill=(0, 0, 0))
def frame(t):
    kk, ss = s_of(t); im = src(ss) if kk == 'a' else src_r(ss)
    bg = im.resize((24, 25)).filter(ImageFilter.GaussianBlur(2)).resize((W, H), Image.BILINEAR); bg = Image.eval(bg, lambda v: int(v * 0.3))
    bg.paste(im, (0, PY + (PH - im.height) // 2)); d = ImageDraw.Draw(bg)
    j = max(i for i, p in enumerate(PARTS) if p[0] <= t); a0, a1, hl, name, line = PARTS[j]; lt = t - a0
    f = fB(44); s = 'LAST-MINUTE LEGENDS'; w = d.textlength(s, font=f); d.rectangle([60, 110, 60 + w + 32, 170], fill=RED); d.text((76, 115), s, font=f, fill=WHITE)
    tc(d, 200, f'{j + 1}/3  ·  {hl}', fB(80), WHITE)
    ly = PY + PH + 40; d.rectangle([60, ly, 72, ly + 150], fill=GOLD)
    d.text((96, ly - 4), name, font=fB(76), fill=WHITE); d.text((96, ly + 86), line, font=fO(30), fill=(215, 215, 225))
    if t > TOTAL - 4:
        a = ease((t - (TOTAL - 4)) / 0.5); tc(d, ly + 220 + int((1 - a) * 20), 'WHICH ONE WAS THE MOST DRAMATIC?', fB(66), GOLD, 6)
    if 0 <= lt < 0.12 and j > 0: bg = Image.blend(bg, Image.new('RGB', (W, H), WHITE), 0.35 * (1 - lt / 0.12))
    if t > TOTAL - 0.5: bg = Image.eval(bg, lambda x, q=(TOTAL - t) / 0.5: int(x * max(0, q)))
    return bg
if __name__ == '__main__':
    if len(sys.argv) > 1:
        ims = [frame(tt).resize((360, 640)) for tt in (5, 24, 26, 36, TOTAL - 1)]
        s = Image.new('RGB', (1800, 640)); [s.paste(im, (i * 360, 0)) for i, im in enumerate(ims)]; s.save('logs/stills.jpg'); sys.exit()
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', 'video.mp4'], stdin=subprocess.PIPE)
    for i in range(int(TOTAL * FPS)): p.stdin.write(frame(i / FPS).tobytes())
    p.stdin.close(); p.wait(); print('TOTAL', TOTAL)
